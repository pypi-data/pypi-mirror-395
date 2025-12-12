import os
import time
import threading
import webbrowser
from pathlib import Path

from kion_pgvectorstore.manage_vectorstore import app
from kion_pgvectorstore.dotenv_finder import DotenvFinder

def get_dotenv_folder():
    # Find set up environment folder (make recursive later)
    env_setup_folder = Path(__file__).resolve().parent 
    # Make sure the .env file is there
    for env_file in env_setup_folder.rglob('.env'):
        return env_file.parent.relative_to(env_setup_folder.parent)
    raise FileNotFoundError("Could not find .env under project root!")

def open_browser():
    time.sleep(1)  # Wait for server to start
    webbrowser.open_new("http://127.0.0.1:5000/")


def main():
    """Main entry point for the application. Initializes the environment and runs the Flask app."""
    # Get the folder name where the .env file was saved during set up
    env_setup_directory = get_dotenv_folder()
    print(f"env_setup_directory: {env_setup_directory}")

    dot_env_finder = DotenvFinder(env_setup_directory=env_setup_directory)
    dot_env_finder.feed_dotenv_file()

    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        threading.Thread(target=open_browser).start()
    app.run(debug=True)

if __name__ == '__main__':
    main()