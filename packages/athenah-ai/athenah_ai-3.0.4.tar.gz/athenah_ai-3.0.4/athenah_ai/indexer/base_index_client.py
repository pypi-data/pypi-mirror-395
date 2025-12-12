import os
import math
from typing import Dict, Any, List, Tuple, Optional, Union
import shutil
import faiss
import pickle
import tiktoken

from basedir import basedir
from dotenv import load_dotenv

from unstructured.file_utils.filetype import FileType, detect_filetype
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import Language
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from google.cloud.storage.bucket import Bucket, Blob
from athenah_ai.libs.google.storage import GCPStorageClient

from athenah_ai.client import AthenahClient
from athenah_ai.indexer.splitters import code_splitter, text_splitter
from athenah_ai.logger import logger

load_dotenv()

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
EMBEDDING_MODEL: str = os.environ.get("EMBEDDING_MODEL")
GCP_INDEX_BUCKET: str = os.environ.get("GCP_INDEX_BUCKET", "athenah-ai-indexes")
DEFAULT_CHUNK_SIZE: int = 200
CHUNK_OVERLAP: int = 0

# --- Utility Functions ---


def estimate_tokens(text: str, model: str = "gpt-3.5-turbo-16k") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))
    except Exception as e:
        logger.error(f"Token estimation failed: {e}")
        return len(text) // 4  # fallback: rough estimate


def estimate_chunk_size(
    model: str,
    max_tokens: int,
    avg_chars_per_token: int = 4,
    safety_margin: float = 0.9,
) -> int:
    try:
        # Use tiktoken to get a more accurate chars/token if needed
        # For now, use avg_chars_per_token as a fallback
        return int(max_tokens * avg_chars_per_token * safety_margin)
    except Exception as e:
        logger.error(f"Chunk size estimation failed: {e}")
        return int(max_tokens * avg_chars_per_token * safety_margin)


def get_dynamic_chunk_size(
    model: str,
    max_tokens: int,
    sample_text: Optional[str] = None,
    safety_margin: float = 0.9,
) -> int:
    if sample_text:
        try:
            tokens = estimate_tokens(sample_text, model)
            chars_per_token = len(sample_text) / max(tokens, 1)
            return int(max_tokens * chars_per_token * safety_margin)
        except Exception as e:
            logger.error(f"Dynamic chunk size estimation failed: {e}")
    return estimate_chunk_size(model, max_tokens, safety_margin=safety_margin)


# --- Summarization ---


def summarize_file(content: str) -> str:
    try:
        client = AthenahClient(id="id", model_name="gpt-3.5-turbo-16k")
        response = client.base_prompt(
            (
                "Describe and summarize what this document says. "
                "Be very specific. Everything must be documented. "
                "Keep it very short and concise, this will be used for labeling a vector search."
            ),
            content,
        )
        return response
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return ""


# --- Directory/File Preparation ---


def load_ai_json_metadata(root: str) -> Dict[str, Any]:
    ai_metadata = {}
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".ai.json"):
                path = os.path.join(dirpath, filename)
                try:
                    with open(path, "r") as f:
                        import json

                        data = json.load(f)
                    real_file = data.get("file_path")
                    if real_file:
                        ai_metadata[os.path.abspath(real_file)] = data
                except Exception as e:
                    logger.error(f"Failed to load metadata {path}: {e}")
    return ai_metadata


def prepare_dir(
    root: str,
    save_path: Optional[str] = None,
    recursive: bool = False,
    chunk_size: Optional[int] = None,
    chunk_overlap: int = CHUNK_OVERLAP,
    model: str = EMBEDDING_MODEL,
    max_tokens: int = 2048,
) -> Tuple[List[str], List[Dict[str, Any]]]:
    splited_docs: List[str] = []
    splited_metadatas: List[Dict[str, Any]] = []

    try:
        loader = DirectoryLoader(
            root,
            silent_errors=True,
            recursive=recursive,
            exclude=["**/node_modules/**", "**/*.ai.json"],
        )
        docs = loader.load()
    except Exception as e:
        logger.error(f"Directory loading failed: {e}")
        return [], []

    ai_metadata = load_ai_json_metadata(root)

    for doc in docs:
        real_path = os.path.abspath(
            doc.metadata.get("source", doc.metadata.get("file_path", ""))
        )
        if real_path in ai_metadata:
            doc.metadata.update(ai_metadata[real_path])
        doc.metadata["source"] = doc.metadata["source"].strip(".txt")

    for doc in docs:
        file_name: str = doc.metadata["source"]
        language = None
        file_type = "text"
        if ".cpp" in file_name or ".h" in file_name:
            file_type = "cpp"
            language = Language.CPP
        elif ".js" in file_name:
            file_type = "js"
            language = Language.JS
        elif ".ts" in file_name:
            file_type = "ts"
            language = Language.TS
        elif ".py" in file_name:
            file_type = "py"
            language = Language.PYTHON

        # Dynamic chunk size
        _chunk_size = chunk_size or get_dynamic_chunk_size(
            model, max_tokens, doc.page_content[:2000]
        )

        splitter = (
            code_splitter(language, chunk_size=_chunk_size, chunk_overlap=chunk_overlap)
            if language
            else text_splitter(chunk_size=_chunk_size, chunk_overlap=chunk_overlap)
        )

        try:
            splits = splitter.split_text(doc.page_content)
        except Exception as e:
            logger.error(f"Text splitting failed for {file_name}: {e}")
            continue

        for index, split in enumerate(splits):
            if not split.strip():
                continue
            chunk_metadata = {
                "file_path": file_name,
                "file_name": os.path.basename(file_name),
                "file_type": file_type,
                "chunk_index": index,
                "total_chunks": len(splits),
            }
            splited_docs.append(split)
            splited_metadatas.append(chunk_metadata)
            if save_path:
                try:
                    split_file_path = os.path.join(save_path, f"split_{index}.txt")
                    with open(split_file_path, "w") as split_file:
                        split_file.write(split)
                except Exception as e:
                    logger.error(f"Failed to save split: {e}")

    return splited_docs, splited_metadatas


def prepare_file(
    file: str,
    save_path: Optional[str] = None,
    chunk_size: Optional[int] = None,
    chunk_overlap: int = CHUNK_OVERLAP,
    model: str = EMBEDDING_MODEL,
    max_tokens: int = 2048,
) -> Tuple[List[str], List[Dict[str, Any]]]:
    splited_docs: List[str] = []
    splited_metadatas: List[Dict[str, Any]] = []
    file_name: str = os.path.basename(file)
    language = None
    file_type = "text"
    if ".h" in file_name or ".cpp" in file_name:
        file_type = "cpp"
        language = Language.CPP
    elif ".js" in file_name:
        file_type = "js"
        language = Language.JS
    elif ".ts" in file_name:
        file_type = "ts"
        language = Language.TS
    elif ".py" in file_name:
        file_type = "py"
        language = Language.PYTHON

    try:
        with open(file, "r") as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file}: {e}")
        return [], []

    _chunk_size = chunk_size or get_dynamic_chunk_size(
        model, max_tokens, content[:2000]
    )

    splitter = (
        code_splitter(language, chunk_size=_chunk_size, chunk_overlap=chunk_overlap)
        if language
        else text_splitter(chunk_size=_chunk_size, chunk_overlap=chunk_overlap)
    )

    try:
        splits = splitter.split_text(content)
    except Exception as e:
        logger.error(f"Text splitting failed for {file_name}: {e}")
        return [], []

    for index, split in enumerate(splits):
        if not split.strip():
            continue
        chunk_metadata = {
            "file_name": file_name,
            "file_path": file,
            "file_type": file_type,
            "chunk_index": index,
            "total_chunks": len(splits),
        }
        splited_docs.append(split)
        splited_metadatas.append(chunk_metadata)
        if save_path:
            try:
                split_file_path = os.path.join(save_path, f"split_{index}.txt")
                with open(split_file_path, "w") as split_file:
                    split_file.write(split)
            except Exception as e:
                logger.error(f"Failed to save split: {e}")

    return splited_docs, splited_metadatas


# --- BaseIndexClient ---


class BaseIndexClient:
    storage_type: str = "local"
    id: str = ""
    name: str = ""
    version: str = ""
    splited_docs: List[str] = []
    splited_metadatas: List[Dict[str, Any]] = []

    def __init__(
        self,
        storage_type: str,
        id: str,
        dir: str,
        name: str,
        version: str = "v1",
    ) -> None:
        self.storage_type = storage_type
        self.id = id
        self.name = name
        self.version = version
        self.base_path: str = os.path.join(basedir, dir)
        self.name_path: str = os.path.join(self.base_path, self.name)
        self.name_source_path: str = os.path.join(self.name_path, f"{self.name}-source")
        self.name_version_path: str = os.path.join(
            self.base_path, f"{self.name}-{self.version}"
        )
        os.makedirs(self.name_version_path, exist_ok=True)
        self.splited_docs: List[str] = []
        self.splited_metadatas: List[Dict[str, Any]] = []
        if self.storage_type == "gcs":
            self.storage_client: GCPStorageClient = GCPStorageClient().add_client()
            self.bucket: Bucket = self.storage_client.init_bucket(GCP_INDEX_BUCKET)

    def copy(self, source: str, destination: str, is_dir: bool = False):
        try:
            if is_dir:
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copyfile(source, destination)
        except Exception as e:
            logger.error(f"Copy failed: {e}")

    def _build_from_dirs(
        self,
        source: str,
        dirs: List[str],
        include_root: bool,
        chunk_size: Optional[int] = None,
        chunk_overlap: int = CHUNK_OVERLAP,
        model: str = EMBEDDING_MODEL,
        max_tokens: int = 2048,
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        _splitted_docs: List[str] = []
        _splited_metadatas: List[Dict[str, Any]] = []
        for dir in dirs:
            splited_docs, splited_metadatas = prepare_dir(
                dir,
                self.name_version_path,
                True,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                model=model,
                max_tokens=max_tokens,
            )
            _splitted_docs.extend(splited_docs)
            _splited_metadatas.extend(splited_metadatas)
        return _splitted_docs, _splited_metadatas

    def _build_from_files(
        self,
        file_paths: List[str],
        chunk_size: Optional[int] = None,
        chunk_overlap: int = CHUNK_OVERLAP,
        model: str = EMBEDDING_MODEL,
        max_tokens: int = 2048,
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        _splitted_docs: List[str] = []
        _splited_metadatas: List[Dict[str, Any]] = []
        for file_path in file_paths:
            splited_docs, splited_metadatas = prepare_file(
                file_path,
                self.name_version_path,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                model=model,
                max_tokens=max_tokens,
            )
            _splitted_docs.extend(splited_docs)
            _splited_metadatas.extend(splited_metadatas)
        return _splitted_docs, _splited_metadatas

    def store_from_docs(
        self,
        splited_docs: List[str],
        splited_metadatas: List[Dict[str, Any]],
        model: str = EMBEDDING_MODEL,
        chunk_size: Optional[int] = None,
    ):
        try:
            embedder = OpenAIEmbeddings(
                openai_api_key=OPENAI_API_KEY,
                model=model,
                chunk_size=chunk_size or DEFAULT_CHUNK_SIZE,
            )
            return FAISS.from_texts(
                splited_docs, embedding=embedder, metadatas=splited_metadatas
            )
        except Exception as e:
            logger.error(f"FAISS store creation failed: {e}")
            return None

    def save(self, store: Optional[FAISS] = None) -> bool:
        if not store:
            logger.error("No FAISS store to save.")
            return False
        try:
            if self.storage_type == "local":
                store.save_local(self.name_version_path)
                return True
            elif self.storage_type == "gcs":
                data_byte_array = pickle.dumps(
                    (store.docstore, store.index_to_docstore_id)
                )
                blob: Blob = self.bucket.blob(f"{self.name}/{self.version}/index.pkl")
                blob.upload_from_string(data_byte_array)
                temp_file_name = "/tmp/index.faiss"
                faiss.write_index(store.index, temp_file_name)
                blob: Blob = self.bucket.blob(f"{self.name}/{self.version}/index.faiss")
                blob.upload_from_filename(temp_file_name)
                return True
        except Exception as e:
            logger.error(f"Failed to save FAISS index: {e}")
        return False
