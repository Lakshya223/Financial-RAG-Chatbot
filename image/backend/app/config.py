import os
from pathlib import Path
import shutil
from dotenv import load_dotenv
from pydantic import BaseModel
import sys


# Load environment variables from .env so OPENAI_API_KEY and others are available
load_dotenv()

# OpenRouter configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

env_value = os.environ.get("IS_USING_IMAGE_RUNTIME", "false").lower()

# IS_USING_IMAGE_RUNTIME will be True only if the string value matches 'true', '1', 't', etc.
IS_USING_IMAGE_RUNTIME = env_value in ('true', '1', 't', 'y', 'yes', 'on')
def copy_chroma_db_to_tmp(src_path: str, dst_path: str):
    """
    Copies the ChromaDB from the Docker image to the Lambda writable /tmp directory.
    """
    # Ensure Lambda-safe absolute path
    if not dst_path.startswith("/tmp/"):
        raise ValueError("dst_path must start with /tmp/, Lambda can only write to /tmp")

    print(f"DEBUG: Copying ChromaDB → {dst_path}")

    # Source inside the Docker image
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source ChromaDB path does not exist: {src_path}")

    # Create destination directory (all parents)
    os.makedirs(dst_path, exist_ok=True)

    # Check if destination already populated
    if os.listdir(dst_path):
        print(f"📁 ChromaDB already exists at {dst_path}, skipping copy.")
        return

    print(f"📁 Copying ChromaDB from '{src_path}' to '{dst_path}' ...")

    # Copy entire tree safely
    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)

    print("✅ ChromaDB copied successfully.")




class Settings(BaseModel):
    openai_api_key: str
    openai_base_url: str | None = None
    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-large"

    # OpenRouter settings for multi-model evaluation
    openrouter_api_key: str = ""
    openrouter_base_url: str = OPENROUTER_BASE_URL

    if IS_USING_IMAGE_RUNTIME:
        os.environ['HOME'] = '/tmp'
        os.environ['HF_HOME'] = '/tmp'
        os.environ['CHROMA_CACHE_DIR'] = '/tmp'
        print(" 🐳 Detected image runtime environment.")
        print("Forcing pysqlite3 replacement for compatibility. :: ", IS_USING_IMAGE_RUNTIME)
        __import__("pysqlite3")
        sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
        data_dir: Path = Path("/data")
        raw_dir: Path = Path("/data/raw")
        processed_dir: Path = Path("/data/processed")
        index_dir: Path = Path("/tmp/data/indexes")
        chroma_persist_dir: Path = Path("/tmp/data/indexes/chroma")
        # Copy ChromaDB to /tmp if needed
        copy_chroma_db_to_tmp(
            src_path="data/indexes/chroma/",
            dst_path="/tmp/data/indexes/chroma/",
        )
    else:
        index_dir: Path = Path("backend/data/indexes")
        chroma_persist_dir: Path = Path("backend/data/indexes/chroma")

class AppConfig(BaseModel):
    settings: Settings


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        openai_base_url=os.environ.get("OPENAI_BASE_URL") or None,
        openai_chat_model=os.environ.get("OPENAI_CHAT_MODEL", "gpt-4.1-mini"),
        openai_embedding_model=os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
        openrouter_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        openrouter_base_url=os.environ.get("OPENROUTER_BASE_URL", OPENROUTER_BASE_URL),
    )



