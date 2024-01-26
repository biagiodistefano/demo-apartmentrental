import os
import warnings
from pathlib import Path

from decouple import Config, RepositoryEnv

# Set the base directories
base_dirs = [
    Path(__file__).resolve().parent.parent.parent.parent,  # Root of the project
    Path(__file__).resolve().parent.parent.parent,  # src of the project
    Path(__file__).resolve().parent.parent,  # fhir_engine directory
    Path(__file__).resolve().parent,  # settings directory
]

# Default to '.env.defaults' if 'USE_ENV' is not set
env_file_name = os.environ.get("USE_ENV", ".env.defaults")

# Initialize the config
config: Config = None  # type: ignore

# Try to find and load the .env file
for base_dir in base_dirs:
    env_path = base_dir / env_file_name
    if env_path.is_file():
        print(f"Loading env file: {env_path}")
        config = Config(RepositoryEnv(str(env_path)))
        break

# Fall back to loading from environment variables if no .env file is found
if config is None:
    warnings.warn(f"Env file not found: {env_file_name}. Loading from environment variables.")
    from decouple import config  # type: ignore
