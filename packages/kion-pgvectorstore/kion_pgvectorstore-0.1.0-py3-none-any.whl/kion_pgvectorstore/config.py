import os
from dotenv import load_dotenv, find_dotenv

class Config:
    """
    A container for all application settings. 
    
    The attributes are populated by the initialize_config() function.
    Do not instantiate this class directly. Access its attributes as class
    attributes, e.g., `Config.OPENAI_MODEL`.
    """
    # This flag will be used to check if the config has been loaded.
    _is_loaded = False

    # Define attributes with None as a default before they are loaded.
    # OpenAI Parameters
    OPENAI_API_KEY = None
    OPENAI_MODEL = None
    OPENAI_EMBEDDING_MODEL = None

    # DB Parameters
    PGHOST = None
    PGUSER = None
    PGPASSWORD = None
    PGDATABASE = None
    PGPORT = None

    # The connection string will be built after loading the other variables.
    CONNECTION_STRING = None

def initialize_config(dotenv_path=None):
    """
    Loads configuration from a .env file into the Config class.

    This function must be called once at the beginning of the user's application
    before any other library components are used.

    Args:
        dotenv_path (str, optional): The absolute or relative path to the .env file.
                                     If None, it will search for a .env file in the
                                     current and parent directories.
    """
    # Prevent the configuration from being loaded more than once.
    if Config._is_loaded:
        return

    if dotenv_path:
        # If a specific path is provided, use it.
        # Check if the file exists before trying to load it.
        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"The specified .env file was not found at: {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        # If no path is given, search for a .env file automatically.
        # find_dotenv() looks in the current directory and then parent directories.
        env_file_path = find_dotenv()
        if not env_file_path:
            print("Warning: .env file not found. Using default values or OS environment variables.")
        load_dotenv(dotenv_path=env_file_path)

        # TEMPORARY DEBUG: See what the environment looks like after loading
        print("--- DEBUG START ---")
        print(f"PGUSER from env: {os.getenv('PGUSER')}")
        print(f"PGPASSWORD from env: {os.getenv('PGPASSWORD')}")
        print(f"PGDATABASE from env: {os.getenv('PGDATABASE')}")
        print("--- DEBUG END ---")    

    # --- Load settings from environment into the Config class ---
    
    # OpenAI Parameters
    Config.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    Config.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    Config.OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

    # DB Parameters
    Config.PGHOST = os.getenv("PGHOST", "localhost")
    Config.PGUSER = os.getenv("PGUSER", "postgres")
    Config.PGPASSWORD = os.getenv("PGPASSWORD")
    Config.PGDATABASE = os.getenv("PGDATABASE")
    Config.PGPORT = os.getenv("PGPORT", "5432")

    # --- Build the connection string after loading the components ---
    # We must check that essential DB components are present.
    if not all([Config.PGUSER, Config.PGPASSWORD, Config.PGHOST, Config.PGPORT, Config.PGDATABASE]):
         print("Warning: One or more required database environment variables (PGUSER, PGPASSWORD, etc.) are missing.")
         Config.CONNECTION_STRING = None
    else:
        Config.CONNECTION_STRING = (
            f"postgresql+psycopg2://{Config.PGUSER}:{Config.PGPASSWORD}@"
            f"{Config.PGHOST}:{Config.PGPORT}/{Config.PGDATABASE}"
        )
    
    # Set the flag to indicate that the configuration is now loaded.
    Config._is_loaded = True