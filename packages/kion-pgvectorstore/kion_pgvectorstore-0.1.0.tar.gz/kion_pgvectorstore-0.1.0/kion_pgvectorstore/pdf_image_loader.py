import os
import fitz
from kion_pgvectorstore.document import Document
# from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer

# import boto3
# from botocore.exceptions import ClientError

class KionPDFImageFileLoader:

    def __init__(self, directory):
        self.directory = directory
        self.clip_model = SentenceTransformer("clip-ViT-B-32")

        # self.aws_s3_bucket = aws_s3_bucket
        # self.aws_region = aws_region
        # if aws_s3_bucket and aws_region:
        #     self.s3_client = boto3.client("s3", region_name=aws_region)
        #     try:
        #         self.s3_client.head_bucket(Bucket=aws_s3_bucket)
        #     except ClientError as e:
        #         print(f"Bucket {aws_s3_bucket} does not exist or is inaccessible. Please create it.")

    def load_pdf_images(self):
        image_output_folder = os.path.join(self.directory, "extracted_pdf_images")
        print(f"Creating image output folder from {self.directory} if it doesn't exist...")
        os.makedirs(image_output_folder, exist_ok=True)
        print(f"Image output folder: {image_output_folder}")

        pdf_loaded_images : list[Document] = []

        for filename in os.listdir(self.directory):
            pdf_path = os.path.join(self.directory, filename).replace("\\","/")
            if not os.path.isfile(pdf_path) or not filename.lower().endswith('.pdf'):
                continue

            doc = fitz.open(pdf_path)
            for page_index in range(len(doc)):
                page = doc.load_page(page_index)
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    if img_index>0:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image['image']
                        image_ext = base_image['ext']

                        base_name = os.path.splitext(filename)[0]
                        image_filename = f"{base_name}_page{page_index + 1}_img{img_index + 1}.{image_ext}"
                        image_path = os.path.join(image_output_folder, image_filename).replace("\\","/")
                        print(f"Printing Image path name: {image_path}")
                        
                        print(image_path)

                        # Save locally
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)

                        # --------- YOUR TEXT CONTEXT CODE -----
                        rects = [block for block in page.get_text("dict")["blocks"] if block["type"] == 1]
                        this_rect = None
                        for rect in rects:
                            image_info = rect.get("image", None)
                            if isinstance(image_info, dict) and image_info.get("xref", None) == xref:
                                this_rect = fitz.Rect(rect['bbox'])
                                break
                        text_blocks = [block for block in page.get_text("dict")["blocks"] if block["type"] == 0]
                        surrounding_texts = []
                        if this_rect:
                            for tblock in text_blocks:
                                trect = fitz.Rect(tblock['bbox'])
                                if abs(trect.y1 - this_rect.y0) < 50 or abs(this_rect.y1 - trect.y0) < 50:
                                    if trect.x1 > this_rect.x0 and trect.x0 < this_rect.x1:
                                        block_text = tblock.get('lines', [])
                                        for line in block_text:
                                            for span in line['spans']:
                                                surrounding_texts.append(span.get('text', '').strip())
                            if surrounding_texts:
                                surrounding_text = " ".join(surrounding_texts)
                            else:
                                surrounding_text = page.get_text()
                        else:
                            surrounding_text = page.get_text()

                        page_content = (surrounding_text)
                        # image_path = image_path.replace("src/","")
                        metadata={
                                "source": pdf_path,
                                "source_file": filename,
                                "page": page_index + 1,
                                "image_index": img_index + 1,
                                "image_ext": image_ext,
                                "image_filename": image_filename,
                                "image_path": image_path,
                            }

                        img_doc = Document(page_content=str(page_content), metadata=dict(metadata))
                        
                        pdf_loaded_images.append(img_doc)
        print(f"Number of PDF Images loaded = {len(pdf_loaded_images)}")            
        return pdf_loaded_images