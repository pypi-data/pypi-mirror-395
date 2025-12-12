*kion_pgvectorstore*

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

kion_pgvectorstore is a Python library and GUI application for managing vector stores in PostgreSQL databases, built with LangChain. It empowers users to upload, organize, search, and manage PDF or .txt documents as collections, query them with an integrated OpenAI chat completion bot, and manipulate documents or collections flexibly—all through a simple web application.

FEATURES
    Upload PDFs & Text Files:
    Easily add data from PDFs or .txt files into your vector store.

Collection Management:
    Group documents into custom-named collections (e.g., by topic).

OpenAI-Powered Search:
    Query your stored documents with natural language questions and filter search scope by selecting collections.

Flexible Deletion:
    Delete individual files or clear out entire collections (if empty), all from an intuitive interface.

Utility Functions:
    Use library functions directly in your Python code (see internal Kion Teams documentation for details).

PREREQUISITES
    Before installing kion_pgvectorstore, ensure you have:

    1. Python: Version 3.8 or higher.
    2. PostgreSQL: Installed on your local machine.
    3. pgvector Extension: Installed on your PostgreSQL database. (PGVector Installation Guide:     https://github.com/pgvector/pgvector)

INSTALLATION
Install the package and Initialize your environment variables:
    In the terminal type:
    1. pip install kion_pgvectorstore
    2. kionrag-env-init --path "<your-path-here>" 
            (generates a .env template without overwriting any existing one, unless forced):
            To force overwrite an existing .env file, add the --force flag: 
                                            kionrag-env-init --path "<your-path-here>" --force
            For more help: kionrag-env-init --help

CONFIGURE YOUR .env FILE:
    Fill in your custom values as required for database connection, OpenAI keys, etc.

Launch the GUI:
    Navigate to the directory containing static/app.py and run: python static/app.py
        - This will start the web application for interacting with your vector store.

USAGE
Document Management:
    Upload: Add PDF or .txt files to collections.
    Group: Organize files by topics or any category, creating and selecting collections.
    Search: Use the OpenAI chatbot to query your database. You can select one or more collections to target for your questions.
    Delete:
    Select a collection by dropdown.
    View all files in that collection.
    Delete individual files, or delete the collection (only possible if empty).
    Library Functions
    Programmatic utility functions for developers are available.

Documentation: See the internal Kion Teams channel for full documentation.
Support & Documentation
Function Documentation: Internal Kion Teams channel.

Issues & Bugs:
    - To fix: If you accidentally add duplicate files to a collection, deleting one will delete all.

Acknowledgements
-Built with LangChain
-Utilizes PostgreSQL and pgvector
-OpenAI chat completion integration

Happy building! If you have any questions or need help, consult your internal Kion support resources.

*This project is intended for internal use. External dissemination or open-source release may require review.*