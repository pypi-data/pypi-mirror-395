# kion_pgvectorstore

License: MIT

Overview
kion_pgvectorstore is a Python library and GUI application for managing vector stores in PostgreSQL (with pgvector).
It lets you upload ONLY PDFs or .txt files, organize them into collections, perform semantic search, and query them via an OpenAI-powered chat UI.
You can also delete files or whole collections from a simple web interface.

Features
- Upload PDFs and text files
- Organize documents into named collections
- OpenAI-powered semantic search across selected collections
- Delete individual files or entire empty collections
- Use functions programmatically in Python
- Simple Flask-based web UI

Prerequisites
- Python 3.8+
- PostgreSQL installed locally or reachable on your network
- pgvector extension enabled in your database
  See: https://github.com/pgvector/pgvector

Quick Start
1) Install the package
   pip install kion-pgvectorstore

2) Create a .env file (once per project) using the CLI
   env-init --path "<-your folder name->" 
      - This folder is MANDATORY as it will store your .env file: 
         (*Not entering a folder name or storing the .env file directly in the project folder will result in errors*)
      - Enter *ONLY* the name of the folder (*DO NOT ENTER A PATH*)
      - To overwrite existing .env, simply add the --force flag:
         *e.g. env-init --path "env" --force*

3) Fill in your .env
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   PGHOST=localhost
   PGUSER=postgres
   PGPASSWORD=yourpassword
   PGDATABASE=yourdb
   PGPORT=5432

4) Launch the web app
   - Locate the *"app.py"* in the folder where you store your .env file
   - Run the *"app.py"* file
   The app will open http://127.0.0.1:5000/ in your browser.

Using the Web UI
- File Loader tab: upload .txt or .pdf files to a collection (set chunk size/overlap)
- Remove Files tab: select a collection, list files, and delete
- Chat tab: pick collections and ask questions; the assistant answers using only your documents

Programmatic Use - Use as library
  Initialize config once in your Python script, then use the plugin:
  from kion_pgvectorstore.pgvector_plugin import PGVectorPlugin
  from kion_pgvectorstore.config import Config
  from kion_pgvectorstore.file_loader import FileLoader
  from kion_pgvectorstore.text_file_loader import KionTextFileLoader
  from kion_pgvectorstore.pdf_file_loader import KionPDFFileLoader

  initialize_config(".env")
  embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY from .env file

  Example Usage:
   db = PGVectorPlugin(embedding_model=embeddings)
   print(db.list_collections())

Notes
- This package ships a .env template inside the package. The env-init CLI copies it to your project.
- Static HTML files are served from within the installed package; you do not need to copy them.

Troubleshooting
- If you see "Configuration has not been initialized", ensure your .env exists and initialize_config has been called (the web app does this automatically).
- Ensure the pgvector extension is installed in your database
- The kion_pg tables are created on first insert.

License
MIT © 2025 Kion Consulting
