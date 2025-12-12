from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="kion-pgvectorstore",
    version="0.1.0",
    description="Kion Consulting Postgres vector database file management library for LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kion Consulting",
    author_email="thoriso@kion.co.za",
    url="https://github.com/yourusername/kion_pgvectorstore",
    project_urls={ 
        "Bug Tracker": "https://github.com/Thoriso-Molefe/kion_pgvectorstore/issues",
        "Documentation": "https://github.com/Thoriso-Molefe/kion_pgvectorstore",
    },
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-cors",
        "python-dotenv",
        "openai",
        "tiktoken",
        "sqlalchemy",
        "psycopg2-binary",
        "pgvector",
        "numpy",
        "sentence-transformers",
        "Pillow",
        "PyMuPDF",
        "pypdf",
        "PyPDF2",
        "importlib-resources",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "kionrag-env-init = kion_pgvectorstore.cli_init_env:main",
        ],
    },
)