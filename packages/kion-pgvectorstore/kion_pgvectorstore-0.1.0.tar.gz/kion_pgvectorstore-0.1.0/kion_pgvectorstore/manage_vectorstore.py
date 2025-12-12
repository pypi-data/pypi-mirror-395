import os
import re
import traceback
from io import BytesIO
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from sqlalchemy import create_engine, text
from werkzeug.utils import secure_filename

import tiktoken
try:
    from pypdf import PdfReader
except ImportError:  # Fallback if only PyPDF2 is installed
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None  # PDF token counting will not be available

from kion_pgvectorstore.config import Config
from kion_pgvectorstore.pgvector_plugin import PGVectorPlugin
from kion_pgvectorstore.file_loader import FileLoader
from kion_pgvectorstore.text_file_loader import KionTextFileLoader
from kion_pgvectorstore.pdf_file_loader import KionPDFFileLoader
from kion_pgvectorstore.pdf_image_loader import KionPDFImageFileLoader

from kion_pgvectorstore.embeddings import SimpleOpenAIEmbeddings
from kion_pgvectorstore.llm import SimpleChatOpenAI

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'

app = Flask(__name__, static_folder=str(STATIC_DIR))
CORS(app)

def get_embeddings():
    print(f"Config loaded: {Config._is_loaded}")
    return SimpleOpenAIEmbeddings(api_key=Config.OPENAI_API_KEY, model=Config.OPENAI_EMBEDDING_MODEL)

def get_db(embeddings):
    return PGVectorPlugin(embedding_model=embeddings)

def get_llm_instance():
    return SimpleChatOpenAI(model=Config.OPENAI_MODEL, temperature=0.7, api_key=Config.OPENAI_API_KEY)

# Prompt Template
RAG_PROMPT_TEMPLATE = (
        "You are a helpful assistant. Your role is to provide extremely detailed, step-by-step, "
        "and beginner-friendly tutorials based on questions about uploaded documents."
        "\n\n"
        "Please format your answer with an empty line between each step for clarity."
        "\n\n"
        "Use ONLY the following context, which has been extracted from one or more documents, "
        "to answer the question as accurately and specifically as possible"
        "\n"
        "(Do not use your internal knowledge. If the context is empty simply let the user know that you do not have enough information to answer their question.):"
        "\n\n--- CONTEXT ---\n{context}\n--- END CONTEXT ---\n\n"
        "Question: {question}\n\n"
        "Helpful Answer:"
    )

# GUI Routes
@app.route("/")
def home():
    return send_from_directory(str(STATIC_DIR), "file_loader_gui.html")

@app.route("/file_loader_gui.html")
def page_loader():
    return send_from_directory(str(STATIC_DIR), "file_loader_gui.html")

@app.route("/file_remover_gui.html")
def page_remover():
    return send_from_directory(str(STATIC_DIR), "file_remover_gui.html")

@app.route("/chat.html")
def page_chat():
    return send_from_directory(str(STATIC_DIR), "chat.html")

@app.route('/api/list_collections', methods=['GET'])
def list_collections():
    try:
        vector_db = get_db(get_embeddings())
        collections = vector_db.list_collections()
        return jsonify(collections=collections)
    except Exception as e:
        print(f"Error fetching collections: {e}")
        return jsonify(error=str(e), collections=[]), 500

@app.route('/api/load_vectorstore', methods=['POST'])
def upload():
    vector_db : PGVectorPlugin = get_db(get_embeddings())
    try:
        num_files = int(request.form.get("num_files", 1))
    except (ValueError, TypeError):
        num_files = 1

    results = []
    for i in range(num_files):
        # Retrieve each file's details
        uploaded_file = request.files.get(f'file_{i}')
        if not uploaded_file:
            results.append({"error": f"No file uploaded for group {i+1}."})
            continue

        # Sanitize filename and build paths
        submitted_name = uploaded_file.filename or ""
        file_name = re.sub(r'\s+', '_', submitted_name)
        file_name = secure_filename(file_name)  # extra safety

        # Per-file settings
        try:
            chunk_size = int(request.form.get(f'chunk_size_{i}', 2000))
            chunk_overlap = int(request.form.get(f'chunk_overlap_{i}', 750))
        except (ValueError, TypeError):
            results.append({"error": f"Invalid numeric values in group {i+1}."})
            continue
        collection_name = request.form.get(f'collection_name_{i}', '').strip()

        # Validate
        if not collection_name:
            results.append({"error": f"Collection name is required in group {i+1}."})
            continue
        if chunk_size < 10 or chunk_size > 8000:
            results.append({"error": f"Chunk Size in group {i+1} must be between 10 and 8000."})
            continue
        if chunk_overlap < 0:
            results.append({"error": f"Chunk Overlap in group {i+1} must be >= 0."})
            continue
        if chunk_overlap > int(0.5 * chunk_size):
            results.append({"error": f"Chunk Overlap in group {i+1} exceeds the maximum Overlap Size for chunk_size={chunk_size}."})
            continue
        lower_name = file_name.lower()
        if not (lower_name.endswith('.txt') or lower_name.endswith('.pdf')):
            results.append({"error": f"Unsupported file type in group {i+1}. Please provide a .txt or .pdf file."})
            continue

        print(f"Processing file group {i+1}: file_name: {file_name}, chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, collection_name={collection_name}")
        try:
            # File path
            file_dir = re.sub(r'\s+', '_', f"data/{collection_name}/")
            os.makedirs(file_dir, exist_ok=True)
            file_path = os.path.join(file_dir, file_name)
            uploaded_file.save(file_path)
            print(f"Saved uploaded file to: {file_path}")

            # Process the file based on its type
            file_loader : FileLoader = None
            image_loader : KionPDFImageFileLoader = None
            if lower_name.endswith('.txt'):
                file_loader = KionTextFileLoader(
                    file_path=file_path,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                image_loader = KionPDFImageFileLoader(file_dir)
            elif lower_name.endswith('.pdf'):
                file_loader = KionPDFFileLoader(
                    file_path=file_path,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                image_loader = KionPDFImageFileLoader(file_dir)
                print(f"File loader created for: {file_path}")

            loaded_documents = file_loader.call_file_loader()
            documents = file_loader.split_data(loaded_documents=loaded_documents, collection_name=collection_name)

            #store the embedding ids
            embedding_ids = vector_db.add_documents(documents, collection_name)

            # PDF Image Extraction
            loaded_images = image_loader.load_pdf_images()
            # Store image embeddings and blobs, linking each image to its most relevant text chunk
            try:
                if loaded_images:
                    image_embedding_ids = vector_db.add_image_documents(
                        image_documents=loaded_images,
                        collection_name=collection_name,
                        candidate_embedding_ids=embedding_ids
                    )
                    print(f"Stored {len(image_embedding_ids)} image embeddings for file {file_name}.")
                else:
                    print("No images detected in PDF.")
            except Exception as e:
                print(f"Warning: could not store image embeddings for {file_name}: {e}")


            print(f"Completed: file_name={file_name}, chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, collection_name={collection_name}")
            results.append({
                "message": "File successfully processed and stored.",
                "file_name": file_name,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "collection_name": collection_name
            })
        except Exception as e:
            print(f"Error during file processing: {e}")
            results.append({"error": f"Failed to process file '{file_name}': {str(e)}"})


    return jsonify(results=results), 200

@app.route('/api/calc_tokens', methods=['POST'])
def calc_tokens():
    """Calculate the average number of tokens per page for a single uploaded file.

    This endpoint is used by the "Tokens" button in the upload GUI.
    It does NOT store anything in the vectorstore; it only inspects the file
    in-memory and reports token statistics back to the browser.
    """
    uploaded_file = request.files.get('file')
    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"error": "No file uploaded. Please choose a file first."}), 400

    submitted_name = uploaded_file.filename
    safe_name = re.sub(r'\s+', '_', submitted_name)
    safe_name = secure_filename(safe_name)
    lower_name = safe_name.lower()

    if not (lower_name.endswith('.txt') or lower_name.endswith('.pdf')):
        return jsonify({"error": "Unsupported file type. Please select a .pdf or .txt file."}), 400

    # Prepare tokenizer
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception as e:
        return jsonify({"error": f"Tokenization backend is not available: {e}"}), 500

    try:
        raw_bytes = uploaded_file.read() or b""
        if not raw_bytes:
            # Empty file – nothing to count
            return jsonify({
                "file_name": submitted_name,
                "pages": 0,
                "total_tokens": 0,
                "average_tokens_per_page": 0
            }), 200

        total_tokens = 0
        num_pages = 0

        if lower_name.endswith('.pdf'):
            if PdfReader is None:
                return jsonify({"error": "PDF support is not available on the server. Please install 'pypdf' or 'PyPDF2'."}), 500

            # Read the PDF from memory
            pdf_stream = BytesIO(raw_bytes)
            try:
                reader = PdfReader(pdf_stream)
            except Exception as e:
                return jsonify({"error": f"Could not read PDF file: {e}"}), 400

            page_token_counts = []

            for page in getattr(reader, 'pages', []):
                try:
                    text = page.extract_text() or ""
                except Exception:
                    text = ""
                # Count tokens for this page
                if text:
                    tokens = encoding.encode(text, disallowed_special=())
                    page_token_counts.append(len(tokens))
                else:
                    page_token_counts.append(0)

            num_pages = len(page_token_counts)
            total_tokens = int(sum(page_token_counts))

        else:
            # TXT file – treat the whole document as a single logical "page"
            text = raw_bytes.decode('utf-8', errors='ignore')
            tokens = encoding.encode(text, disallowed_special=())
            total_tokens = len(tokens)
            num_pages = 1 if total_tokens > 0 else 0

        average_tokens = int(round(total_tokens / num_pages)) if num_pages > 0 else 0

        return jsonify({
            "file_name": submitted_name,
            "pages": num_pages,
            "total_tokens": total_tokens,
            "average_tokens_per_page": average_tokens
        }), 200
    except Exception as e:
        print(f"Error while calculating tokens: {e}")
        return jsonify({"error": f"Failed to calculate tokens: {e}"}), 500

@app.route('/api/list_files', methods=['GET'])

def list_files():
    collection_name = request.args.get('collection_name')
    if not collection_name:
        return jsonify({"error": "collection_name required"}), 400

    try:
        engine = create_engine(Config.CONNECTION_STRING)
        with engine.connect() as conn:
            # Find collection uuid
            res = conn.execute(
                text("SELECT uuid FROM kion_pg_collection WHERE name = :name"),
                {"name": collection_name}
            ).fetchone()
            if not res:
                return jsonify({"files": []})

            collection_uuid = res[0]
            files_res = conn.execute(
                text("""
                    SELECT DISTINCT cmetadata->>'file_name' AS file_name
                    FROM kion_pg_embedding
                    WHERE collection_id = :uuid AND cmetadata->>'file_name' IS NOT NULL
                    ORDER BY file_name
                """), {"uuid": str(collection_uuid)}
            )
            files = [row[0] for row in files_res.fetchall()]
        return jsonify({"files": files})
    except Exception as e:
        print(f"Error listing files for {collection_name}: {e}")
        return jsonify(error=str(e), files=[]), 500

@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    collection_name = request.form.get('collection_name')
    file_name = request.form.get('file_name')
    if not (collection_name and file_name):
        return jsonify({"error": "Both collection_name and file_name are required."}), 400
    
    vector_db = get_db(get_embeddings())
    try:
        with vector_db.engine.begin() as conn:
            # Find the UUID for the collection name
            collection_id_query = text(
                "SELECT uuid FROM kion_pg_collection WHERE name = :collection_name"
            )
            res = conn.execute(collection_id_query, {"collection_name": collection_name}).fetchone()
            if not res:
                return jsonify({"error": f"Collection '{collection_name}' not found."}), 404
            collection_uuid = res[0]

            # Delete all chunks from that file in the collection
            delete_query = text("""
                DELETE FROM kion_pg_embedding
                WHERE collection_id = :collection_uuid
                AND cmetadata->>'file_name' = :file_name
            """)
            result = conn.execute(delete_query, {
                "collection_uuid": str(collection_uuid),
                "file_name": file_name
            })

        # Delete local file if exists
        try:
            file_dir = re.sub(r'\s+', '_', f"data/{collection_name}/")
            file_path = os.path.join(file_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted local file: {file_path}")
            else:
                print(f"Local file not found for deletion: {file_path}")
        except Exception as local_err:
            print(f"Error deleting local file: {local_err}")

        return jsonify({
            "status": "deleted",
            "collection_name": collection_name,
            "file_name": file_name,
            "rows_affected": result.rowcount
        }), 200
    except Exception as e:
        print(f"Error deleting file {file_name} from {collection_name}: {e}")
        return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500
    
@app.route('/api/delete_collection', methods=['POST'])
def delete_collection():
    collection_name = request.form.get("collection_name")
    if not collection_name:
        return jsonify({"error": "collection_name is required."}), 400
    
    vector_db = get_db(get_embeddings())
    try:
        vector_db.delete_collection(collection_name)
        
        # Delete local folder if exists
        try:
            folder_path = re.sub(r'\s+', '_', f"data/{collection_name}/")
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                import shutil
                shutil.rmtree(folder_path)
                print(f"Deleted local folder: {folder_path}")
            else:
                print(f"Local folder not found for deletion: {folder_path}")
        except Exception as local_err:
            print(f"Error deleting local collection folder: {local_err}")

        return jsonify({"status": "deleted", "collection_name": collection_name})
    except Exception as e:
        print(f"Error deleting collection {collection_name}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/query_rag', methods=["POST"])
def query_rag():
    vector_db_plugin = get_db(get_embeddings())
    llm = get_llm_instance()
    if not vector_db_plugin or not llm:
        return jsonify({"error": "Backend services not initialized."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    collection_names = data.get("collection_names")
    user_query = data.get("query")
    k = int(data.get("k", 5))
    temperature = float(data.get("temperature", 0.7))

    if not collection_names or not isinstance(collection_names, list) or len(collection_names) == 0:
        return jsonify({"error": "A list of 'collection_names' is required"}), 400
    if not user_query:
        return jsonify({"error": "'query' is required"}), 400

    try:
        # Aggregate all docs+scores
        all_doc_scores = []
        for collection_name in collection_names:
            results = vector_db_plugin.similarity_search_with_scores(
                collection_name=collection_name,
                query=user_query,
                k=k)
            all_doc_scores.extend([
                (doc, score, collection_name)
                for doc, score in results
            ])

        if not all_doc_scores:
            return jsonify({
                "answer": "I could not find any relevant information in the selected collections to answer your question.",
                "sources": []
            })

        # Sort by descending score (higher is more similar in PGVector)
        all_doc_scores.sort(key=lambda t: t[1], reverse=True)

        # Take top k
        top_doc_scores = all_doc_scores[:k]

        print(f"\n\nEXAMPLE DOC: {top_doc_scores}\n\n")

        # Gather embedding IDs for image lookup (if present in doc)
        embedding_ids = []
        for doc, score, coll in top_doc_scores:
            try:
                if isinstance(doc, dict) and 'id' in doc and doc['id'] is not None:
                    embedding_ids.append(int(doc['id']))
            except Exception:
                pass

        # Fetch related images for these embeddings
        images_by_embedding = {}
        try:
            images_by_embedding = vector_db_plugin.get_images_for_embedding_ids(embedding_ids, max_images_per_embedding=3)
        except Exception as e:
            print(f"Warning: could not fetch images for embeddings {embedding_ids}: {e}")
            sources_text = "\n\n".join(
            f"Source from '{doc['metadata'].get('file_name', 'Unknown')}':\n{doc['page_content']}"
            for doc, score, coll in top_doc_scores)
        
        sources_text = "\n\n".join(
            f"Source from '{doc['metadata'].get('file_name', 'Unknown')}':\n{doc['page_content']}"
            for doc, score, coll in top_doc_scores)
        llm.temperature = temperature

        formatted_prompt = RAG_PROMPT_TEMPLATE.format(
            context=sources_text,
            question=user_query
        )

        print("Sending prompt to LLM...")
        resp = llm.invoke(formatted_prompt)
        answer = resp.content

        source_chunks = []
        for doc, score, coll in top_doc_scores:
            images_payload = []
            try:
                emb_id = int(doc.get('id')) if isinstance(doc, dict) and doc.get('id') is not None else None
            except Exception:
                emb_id = None
            if emb_id is not None and emb_id in images_by_embedding:
                for img in images_by_embedding[emb_id]:
                    try:
                        b64 = None
                        if img.get("image_bytes") is not None:
                            b64 = "data:" + (img.get("mime_type") or "image/png") + ";base64," + __import__("base64").b64encode(img["image_bytes"]).decode("utf-8")
                        images_payload.append({
                            "blob_id": img.get("blob_id"),
                            "image_embedding_id": img.get("image_embedding_id"),
                            "mime_type": img.get("mime_type"),
                            "image_filename": img.get("image_filename"),
                            "image_path": img.get("image_path"),
                            "data_uri": b64,
                            "image_meta": img.get("image_meta")
                        })
                    except Exception as _:
                        pass
            source_chunks.append({
                "id": doc.get("id") if isinstance(doc, dict) else None,
                "page_content": doc['page_content'],
                "metadata": doc['metadata'],
                "score": score,
                "collection_name": coll,
                "images": images_payload
            })

        return jsonify({
            "answer": answer,
            "sources": source_chunks
        })

    except Exception as e:
        print(f"An error occurred during the RAG query:")
        print(traceback.format_exc())
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
