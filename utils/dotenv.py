from os import getenv
from pathlib import Path
from dotenv import load_dotenv

def load_env(env_file: str=getenv("DOTENV_PATH", "."), fallover=True):
    print(f"Loading environment from {env_file}")
    if Path(env_file).is_file():
        print(f"Loading environment from .env file {env_file}")
        load_dotenv(env_file)
    elif fallover and Path(".env").is_file():
        print(f"Loading environment from .env file {env_file}")
        load_dotenv()
