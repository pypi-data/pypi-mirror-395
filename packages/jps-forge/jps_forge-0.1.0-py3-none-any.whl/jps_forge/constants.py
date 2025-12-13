import os


DEFAULT_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "conf", "config.yaml")

DEFAULT_TEMPERATURE = 0.3
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100

# DEFAULT_STORAGE_DIR = "~/.config/jps-forge/storage"
DEFAULT_STORAGE_DIR = os.path.expanduser("~/.config/jps-forge/storage")