import os
import traceback
from kion_pgvectorstore.config import initialize_config, Config

class DotenvFinder:
    """
    A class to find and load the .env file for the Kion Vectorstore application.
    This class is designed"""

    def __init__(self, env_setup_directory):
        self.env_setup_directory = env_setup_directory

    # find .env file
    def feed_dotenv_file(self):
        """
        Searches for the .env file in the specified directory and initializes the configuration.
        If the .env file is not found, it raises an error.
        """
        try:
            # Check if the directory exists
            if not os.path.exists(self.env_setup_directory):
                raise FileNotFoundError(f"The specified directory does not exist: {self.env_setup_directory}")

            # Find the .env file
            env_file_path = os.path.join(self.env_setup_directory, '.env')
            if not os.path.isfile(env_file_path):
                raise FileNotFoundError(f".env file not found in the specified directory: {self.env_setup_directory}")

        except Exception as e:
            print(f"Error finding .env file: {e}")
            traceback.print_exc()
            return
        
        # Initialize the configuration using the found .env file
      
        initialize_config(dotenv_path=env_file_path)
        print(f"Configuration initialized successfully from: {env_file_path}")
        print(f"-- Printing values from the .env file: {env_file_path} --")
        print(f"Using OpenAI API Key: {Config.OPENAI_API_KEY}")
        print(f"Using connection string: {Config.CONNECTION_STRING}")