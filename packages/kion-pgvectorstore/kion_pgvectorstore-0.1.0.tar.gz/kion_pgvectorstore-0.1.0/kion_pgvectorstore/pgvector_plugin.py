import ast
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
import os
from sqlalchemy import create_engine, text
from kion_pgvectorstore.config import Config
from kion_pgvectorstore.embeddings import SimpleOpenAIEmbeddings
from kion_pgvectorstore.document import Document
from pgvector.sqlalchemy import Vector
import io
from PIL import Image

# Optional heavy imports only used when image support is invoked
try:
    from sentence_transformers import SentenceTransformer
    from PIL import Image
    _HAS_CLIP = True
except Exception:
    _HAS_CLIP = False


def ensure_float_vector(vec):
    # If already a numpy array, return as is
    if isinstance(vec, np.ndarray):
        return vec.astype(np.float64)
    # If it's a list or tuple
    if isinstance(vec, (list, tuple)):
        return np.array(vec, dtype=np.float64)
    # If it's a string (DB returns a string)
    if isinstance(vec, str):
        # Parse the string representation of the list
        return np.array(ast.literal_eval(vec), dtype=np.float64)
    raise ValueError(f"Vector has unsupported type {type(vec)}: {vec}")

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1, dtype=np.float64)
    v2 = np.array(vec2, dtype=np.float64)
    if np.all(v1 == 0) or np.all(v2 == 0):
        return 0.0
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

class PGVectorPlugin:
    # Accept 'embedding_model' as a required argument
    def __init__(self, embedding_model):
        # Ensure the configuration is loaded before proceeding
        if not Config._is_loaded:
            raise RuntimeError(
                "Configuration has not been initialized. "
                "Please call kion_pgvectorstore.initialize_config() at the start of your application."
            )

        # Check param: embedding_model provided
        if embedding_model is None:
            raise ValueError("An embedding_model instance must be provided to PGVectorPlugin.")

        # Store params as the instance variables
        self.embedding_ids = []
        self.embedding_model = embedding_model
        self.connection_string = Config.CONNECTION_STRING
        print(f"Using connection string: {self.connection_string}")

        if not self.connection_string:
            raise ValueError(
                "Database CONNECTION_STRING could not be built. "
                "Please ensure all database settings are defined in your .env file."
            )

        self.engine = create_engine(self.connection_string)

        # Ensure core tables exist (collections table)
        with self.engine.begin() as conn:
            # Enable vector extension
            try:
                conn.execute(text("""
                 CREATE EXTENSION IF NOT EXISTS vector;             
                 CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                """))
            except Exception as e:
                # Extension creation might require superuser; continue if already available
                print(f"Warning: could not ensure 'vector' extension: {e}")
            # Create collections table if not exists
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS kion_pg_collection (
                    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name TEXT UNIQUE NOT NULL
                );
            """))

            # Create embeddings table if not exists, default to 1536 dims.
            # If you use a different embedding size, create the table manually to match that size.
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS kion_pg_embedding (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                collection_id UUID NOT NULL REFERENCES kion_pg_collection(uuid) ON DELETE CASCADE,
                embedding VECTOR(1536),
                document TEXT,
                cmetadata JSONB
            );             
            """))

            # Image embeddings table (CLIP ViT-B-32 produces 512-d vectors)
            # Links to the textual embedding row via embedding_id
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS kion_pg_image_embedding (
                    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    embedding VECTOR(512) NOT NULL,
                    embedding_id BIGINT NOT NULL REFERENCES kion_pg_embedding(id) ON DELETE CASCADE,
                    cmetadata JSONB
                );
            """))

            # Raw image bytes table; links to kion_pg_image_embedding
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS kion_pg_image_blob (
                    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    image_embedding_id BIGINT NOT NULL REFERENCES kion_pg_image_embedding(id) ON DELETE CASCADE,
                    image_bytes BYTEA NOT NULL,
                    mime_type TEXT,
                    image_filename TEXT,
                    image_path TEXT
                );
            """))

    def list_collections(self):
        with self.engine.connect() as conn:
            res = conn.execute(text("SELECT name FROM kion_pg_collection ORDER BY name;"))
            return [row[0] for row in res.fetchall()]

    def add_documents(self, documents: list[Document], collection_name):
        print(f"Documents passed to the add_documents function: {len(documents)}")

        embedding_ids = []

        with self.engine.begin() as conn:
            # Get collection uuid or create collection if not exists
            res = conn.execute(
                text("SELECT uuid FROM kion_pg_collection WHERE name = :name"),
                {"name": collection_name}
            ).fetchone()
            print(f"Checking if collection named {collection_name} exists: res= {res}")
            if not res:
                # Create collection
                print(f"connection string {self.engine.url}")
                create_res = conn.execute(
                    text("INSERT INTO kion_pg_collection (name) VALUES (:name) RETURNING uuid"),
                    {"name": collection_name}
                ).fetchone()
                collection_uuid = create_res[0]
                print(f"Checking if collection name is created: {collection_name}")
            else:
                collection_uuid = res[0]
                print(f"Checking if collection name is succesfully fetched: {collection_name}")

            print(f"Collection uuid= {collection_uuid}")

            print("Extracting Document text and metadata\n\n")
            document_texts = [
                doc.page_content if hasattr(doc, "page_content") else doc.get("page_content", "")
                for doc in documents
            ]
            document_metas = [
                doc.metadata if hasattr(doc, "metadata") else doc.get("metadata", {})
                for doc in documents
            ]

            # Get vectors
            simple_embedding_model : SimpleOpenAIEmbeddings = self.embedding_model
            vectors = simple_embedding_model.embed_documents(document_texts)

            # Now insert each document+vector in the embedding table
            for content, meta, vector in zip(document_texts, document_metas, vectors):
                # Ensure meta is a JSON string and vector is a list of floats
                try:
                    # Get embedding ID of last inserted row
                    embedding_id = None
                    create_res = conn.execute(
                        text("""
                             INSERT INTO kion_pg_embedding
                                (collection_id, cmetadata, document, embedding) 
                             VALUES
                                (:collection_id, :cmetadata, :document, :embedding) 
                             RETURNING id"""),
                        {
                            "collection_id": collection_uuid,
                            "cmetadata": json.dumps(meta),
                            "document": content,
                            "embedding": list(vector) if hasattr(vector, 'tolist') else vector
                        }
                    ).fetchone()
                    embedding_id = create_res[0]
                    embedding_ids.append(embedding_id)
                except Exception as e:
                    print("INSERT ERROR:", e)
                    print(f"Failed document: {content}, metadata: {meta}, vector: {vector}")

        print(f"Added {len(documents)} documents to collection '{collection_name}'")
        print(f"Embedding IDs: {embedding_ids}")

        #Now embed vectors
        return embedding_ids

    def list_files(self, collection_name):
        with self.engine.connect() as conn:
            res = conn.execute(
                text("SELECT uuid FROM kion_pg_collection WHERE name = :name"),
                {"name": collection_name}
            ).fetchone()
            if not res:
                return []
            collection_uuid = res[0]
            files_res = conn.execute(
                text("""
                    SELECT DISTINCT cmetadata->>'file_name' AS file_name
                    FROM kion_pg_embedding
                    WHERE collection_id = :uuid AND cmetadata->>'file_name' IS NOT NULL
                    ORDER BY file_name
                    """), {"uuid": str(collection_uuid)}
            )
            return [row[0] for row in files_res.fetchall()]

    def delete_file(self, collection_name, file_name):
        with self.engine.begin() as conn:
            res = conn.execute(
                text("SELECT uuid FROM kion_pg_collection WHERE name = :name"),
                {"name": collection_name}
            ).fetchone()
            if not res:
                raise ValueError(f"Collection '{collection_name}' not found.")
            collection_uuid = res[0]
            result = conn.execute(
                text("""
                    DELETE FROM kion_pg_embedding
                    WHERE collection_id = :collection_uuid
                    AND cmetadata->>'file_name' = :file_name
                """),
                {"collection_uuid": str(collection_uuid), "file_name": file_name}
            )
            return result.rowcount

    def delete_collection(self, collection_name):
        with self.engine.begin() as conn:
            res = conn.execute(
                text("SELECT uuid FROM kion_pg_collection WHERE name = :name"),
                {"name": collection_name}
            ).fetchone()
            if not res:
                raise ValueError(f"Collection '{collection_name}' not found.")
            collection_uuid = res[0]
            # Remove all embeddings first
            conn.execute(
                text("DELETE FROM kion_pg_embedding WHERE collection_id = :uuid"),
                {"uuid": str(collection_uuid)}
            )
            # Remove the collection itself
            conn.execute(
                text("DELETE FROM kion_pg_collection WHERE uuid = :uuid"),
                {"uuid": str(collection_uuid)}
            )

    def similarity_search_with_scores(self, collection_name, query, k=5):
        # Find collection
        with self.engine.connect() as conn:
            res = conn.execute(
                text("SELECT uuid FROM kion_pg_collection WHERE name = :name"),
                {"name": collection_name}
            ).fetchone()
            if not res:
                return []

            collection_uuid = res[0]

            # Get all embeddings + docs from that collection
            rows = conn.execute(
                text("""
                    SELECT id, document, embedding, cmetadata
                    FROM kion_pg_embedding
                    WHERE collection_id = :uuid
                """),
                {"uuid": str(collection_uuid)}
            ).fetchall()

            embedding_ids = []
            documents = []
            vectors = []
            metadatas = []
            
            for row in rows:
                # row: (id, document, embedding, cmetadata)
                embedding_ids.append(int(row[0]))
                documents.append(row[1])
                vectors.append(row[2])
                metadatas.append(row[3])

            # Embed the query
            simple_embedding_model : SimpleOpenAIEmbeddings = self.embedding_model
            query_vec = simple_embedding_model.embed_query(query)#The query is a list of float

            # Compute similarities
            # First turn the list of string into a list of floats the perform the similarity search
            scores = [cosine_similarity(query_vec, ensure_float_vector(vec)) for vec in vectors]
            # Get top-K by score (descending)
            top = sorted(zip(embedding_ids, documents, metadatas, scores), key=lambda x: x[3], reverse=True)[:k]
            # Return as (doc-dict, score)
            return [
                (
                    {
                        'id': int(eid),
                        'page_content': doc,
                        'metadata': meta,
                    }, float(score)
                )
                for eid, doc, meta, score in top
            ]

    def add_image_documents(self, image_documents: List[Document], collection_name: str, candidate_embedding_ids: List[int]) -> List[int]:
        """Stores image embeddings and image blobs, linking each image to the most relevant
        textual embedding row in kion_pg_embedding.

        - image_documents: List of Document objects where
            - page_content contains surrounding text for the image
            - metadata contains keys: source_file, page, image_index, image_ext, image_filename, image_path
        - collection_name: The collection being processed (for logging/metadata purposes)
        - candidate_embedding_ids: The embedding IDs returned by add_documents for this same file load.
          We will select among those IDs to find the best parent row per image.

        Returns a list of newly created kion_pg_image_embedding.id values.
        """
        if not image_documents:
            print("No image documents to store.")
            return []

        if not candidate_embedding_ids:
            print("No candidate text embedding IDs provided. Cannot link images to text chunks.")
            return []

        if not _HAS_CLIP:
            raise RuntimeError("SentenceTransformer/Pillow not installed. Cannot compute image embeddings.")

        clip_model = SentenceTransformer("clip-ViT-B-32")

        # Build a convenience string for IN clause
        id_list_str = ",".join(str(i) for i in candidate_embedding_ids)

        inserted_image_embedding_ids : List[int] = []

        with self.engine.begin() as conn:
            # Pull the candidate text chunk rows (id, embedding, metadata)
            rows = conn.execute(
                text(f"""
                    SELECT id, embedding, cmetadata, document
                    FROM kion_pg_embedding
                    WHERE id IN ({id_list_str})
                """)
            ).fetchall()

            # Group candidate chunks by (file_name, page)
            # Also keep a simple id->(embedding, meta, doc) map
            candidate_by_file_page : Dict[Tuple[str, int], List[Dict]] = {}
            id_to_row : Dict[int, Dict] = {}
            for rid, embv, meta, doc_text in rows:
                # meta is JSON already via SQLAlchemy/psycopg2
                file_name = None
                page = None
                try:
                    file_name = meta.get("file_name") or meta.get("source_file") or (meta.get("source") and os.path.basename(meta.get("source")))
                except Exception:
                    pass
                try:
                    page = int(meta.get("page")) if meta and meta.get("page") is not None else None
                except Exception:
                    page = None
                rec = {
                    "id": rid,
                    "embedding": ensure_float_vector(embv),
                    "meta": meta,
                    "document": doc_text or "",
                }
                id_to_row[rid] = rec
                if file_name is not None and page is not None:
                    candidate_by_file_page.setdefault((file_name, page), []).append(rec)

            # Helper: choose best text chunk for an image using cosine similarity with the image's surrounding text
            def select_best_parent_id(img_file_name: str, img_page: Optional[int], img_surrounding_text: str) -> Optional[int]:
                # First look only among rows that match file_name and page
                candidates = candidate_by_file_page.get((img_file_name, img_page), [])
                # Fallback: if nothing, allow any row with matching file_name
                if not candidates:
                    # Gather by file only
                    candidates = [r for (fname, pg), lst in candidate_by_file_page.items() if fname == img_file_name for r in lst]
                if not candidates:
                    # Last fallback: any candidate at all
                    candidates = list(id_to_row.values())
                if not candidates:
                    return None
                # Embed the image surrounding text once
                try:
                    text_vec = self.embedding_model.embed_query(img_surrounding_text or "")
                except Exception:
                    text_vec = np.zeros(1536, dtype=np.float64)
                # Score against each candidate's precomputed vector
                best_id = None
                best_score = -1.0
                for rec in candidates:
                    score = cosine_similarity(text_vec, rec["embedding"])
                    if score > best_score:
                        best_score = score
                        best_id = rec["id"]
                return best_id

            # Process each image doc
            for img_doc in image_documents:
                meta = img_doc.metadata or {}
                img_file_name= meta.get("image_filename")
                img_page = None
                try:
                    img_page = int(meta.get("page")) if meta.get("page") is not None else None
                except Exception:
                    pass
                img_path = meta.get("image_path")
                img_ext = meta.get("image_ext") or ""
                img_filename = meta.get("image_filename")
                # Determine mime_type from ext
                mime_type = None
                if img_ext:
                    lower = img_ext.lower()
                    if lower in ("jpg", "jpeg"):
                        mime_type = "image/jpeg"
                    elif lower == "png":
                        mime_type = "image/png"
                    elif lower == "gif":
                        mime_type = "image/gif"
                    elif lower in ("tif", "tiff"):
                        mime_type = "image/tiff"
                    elif lower == "bmp":
                        mime_type = "image/bmp"
                    else:
                        mime_type = f"image/{lower}"

                # Read bytes
                if not img_path or not os.path.exists(img_path):
                    print(f"Warning: image path not found or does not exist: {img_path}")
                    # Skip storing if bytes unavailable
                    continue
                try:
                    with open(img_path, "rb") as f:
                        img_bytes = f.read()
                except Exception as e:
                    print(f"Warning: could not read image bytes for {img_path}: {e}")
                    continue

                # Compute CLIP embedding
                try:
                    pil_img = Image.open(img_path).convert("RGB")
                    img_vec = clip_model.encode(pil_img, convert_to_numpy=True, normalize_embeddings=True)
                    if hasattr(img_vec, "tolist"):
                        img_vec = img_vec.tolist()
                except Exception as e:
                    print(f"Warning: could not compute CLIP embedding for {img_path}: {e}")
                    continue

                # Choose the best parent embedding id
                parent_id = select_best_parent_id(img_file_name, img_page, img_doc.page_content)
                if parent_id is None:
                    print(f"Warning: could not find a parent embedding id for image {img_filename}; skipping.")
                    continue

                # Insert into image embedding and blob tables
                try:
                    create_res = conn.execute(
                        text("""
                            INSERT INTO kion_pg_image_embedding (embedding, embedding_id, cmetadata)
                            VALUES (:embedding, :embedding_id, :cmetadata)
                            RETURNING id
                        """),
                        {
                            "embedding": img_vec,
                            "embedding_id": int(parent_id),
                            "cmetadata": json.dumps({
                                **meta,
                                "collection_name": collection_name,
                                "surrounding_text_snippet": (img_doc.page_content[:600] if isinstance(img_doc.page_content, str) else "")
                            })
                        }
                    ).fetchone()
                    image_embedding_id = int(create_res[0])
                    print(f"Inserted image embedding id {image_embedding_id} for image {img_filename}")
                    inserted_image_embedding_ids.append(image_embedding_id)

                    conn.execute(
                        text("""
                            INSERT INTO kion_pg_image_blob (image_embedding_id, image_bytes, mime_type, image_filename, image_path)
                            VALUES (:image_embedding_id, :image_bytes, :mime_type, :image_filename, :image_path)
                        """),
                        {
                            "image_embedding_id": image_embedding_id,
                            "image_bytes": img_bytes,
                            "mime_type": mime_type,
                            "image_filename": img_filename,
                            "image_path": img_path,
                        }
                    )
                except Exception as e:
                    print(f"INSERT IMAGE ERROR for {img_filename}: {e}")

        print(f"Added {len(inserted_image_embedding_ids)} image embeddings for collection '{collection_name}'.")
        return inserted_image_embedding_ids

    def get_images_for_embedding_ids(self, embedding_ids: List[int], max_images_per_embedding: int = 3) -> Dict[int, List[Dict]]:
        """Fetch image blobs linked to the given textual embedding IDs.

        Returns a dict mapping embedding_id -> list of image dicts with keys:
            - blob_id
            - image_embedding_id
            - mime_type
            - image_filename
            - image_path
            - image_bytes (raw bytes)
        """
        if not embedding_ids:
            return {}
        # Sanitize and build IN list
        safe_ids = [int(e) for e in embedding_ids if e is not None]
        if not safe_ids:
            return {}
        id_list_str = ",".join(str(i) for i in safe_ids)
        out: Dict[int, List[Dict]] = {}
        with self.engine.connect() as conn:
            rows = conn.execute(
                text(f"""
                    SELECT ie.embedding_id,
                           ib.id AS blob_id,
                           ie.id AS image_embedding_id,
                           ib.mime_type,
                           ib.image_filename,
                           ib.image_path,
                           ib.image_bytes,
                           ie.cmetadata
                    FROM kion_pg_image_embedding AS ie
                    JOIN kion_pg_image_blob AS ib
                      ON ib.image_embedding_id = ie.id
                    WHERE ie.embedding_id IN ({id_list_str})
                    ORDER BY ie.embedding_id, ib.id
                """)
            ).fetchall()
            for embedding_id, blob_id, image_embedding_id, mime_type, image_filename, image_path, image_bytes, image_meta in rows:
                lst = out.setdefault(int(embedding_id), [])
                if max_images_per_embedding is not None and len(lst) >= int(max_images_per_embedding):
                    # Skip extra images per embedding_id
                    continue
                lst.append({
                    "blob_id": int(blob_id),
                    "image_embedding_id": int(image_embedding_id),
                    "mime_type": mime_type,
                    "image_filename": image_filename,
                    "image_path": image_path,
                    "image_bytes": image_bytes,
                "image_meta": image_meta,
                })
        return out