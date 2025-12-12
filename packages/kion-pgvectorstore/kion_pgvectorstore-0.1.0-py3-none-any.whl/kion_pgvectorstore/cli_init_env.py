import argparse
from kion_pgvectorstore.setup_config import create_env_file

def main():
    """
    The main function for the env-init command-line tool.
    """
    parser = argparse.ArgumentParser(
        prog="env-init",
        description=(
            "Kion Vectorstore Initializer: Create an initial .env and helper files "
            "for your project in the chosen directory."
        ),
    )

    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Directory where files will be created. Defaults to the current directory.",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwrite of existing files if they already exist.",
    )

    args = parser.parse_args()
    create_env_file(destination_dir=args.path, force=args.force)

if __name__ == "__main__":
    main()