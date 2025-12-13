import os
import logging
from pathlib import Path
import yaml
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from .constants import DEFAULT_CONFIG_FILE_PATH, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP, DEFAULT_STORAGE_DIR


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



with open(DEFAULT_CONFIG_FILE_PATH) as f:
    config = yaml.safe_load(f)

embeddings = HuggingFaceEmbeddings(model_name=config["embedding_model"])

def index():
    all_docs = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=DEFAULT_CHUNK_SIZE, 
        chunk_overlap=DEFAULT_CHUNK_OVERLAP
    )

    glob_patterns = config["glob_patterns"]

    for root in config["workspace_roots"]:
        logger.info(f"Processing workspace root: {root}")
        root = Path(root).expanduser()
        if not root.exists():
            print(f"Workspace root does not exist: {root}")
            continue

        logger.info(f"Indexing workspace: {root}")
        
        # Create exclude patterns for DirectoryLoader
        exclude_patterns = [f"**/{pattern}" if not pattern.startswith("*") else pattern 
                           for pattern in config["ignore_dirs"]]
        
        loader = DirectoryLoader(
            str(root),
            glob=glob_patterns,
            loader_cls=TextLoader,
            exclude=exclude_patterns,
            silent_errors=True
        )
        
        try:
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} documents from {root}")
            
            split_docs = text_splitter.split_documents(docs)
            for doc in split_docs:
                doc.metadata["source_path"] = str(Path(doc.metadata["source"]).relative_to(root))
            all_docs.extend(split_docs)
            
        except Exception as e:
            logger.error(f"Error loading documents from {root}: {e}")
            continue

    logger.info(f"Loaded {len(all_docs)} chunks from {len(config['workspace_roots'])} workspace(s)")

    if all_docs:
        storage_dir = Path(DEFAULT_STORAGE_DIR).expanduser()
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        vectorstore = FAISS.from_documents(all_docs, embeddings)
        vectorstore.save_local(str(storage_dir))
        logger.info(f"Index saved to {storage_dir}")
    else:
        logger.info("No documents found to index.")

def main():
    """Main entry point for the jps-forge-index command."""
    index()

if __name__ == "__main__":
    main()