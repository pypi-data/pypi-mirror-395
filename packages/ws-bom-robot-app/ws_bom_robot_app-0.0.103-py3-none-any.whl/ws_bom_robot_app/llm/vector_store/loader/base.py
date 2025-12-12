import asyncio, gc, logging, os, traceback
from typing import Any, Optional
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_core.documents import Document
from pydantic import BaseModel
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.vector_store.loader.json_loader import JsonLoader
from ws_bom_robot_app.llm.vector_store.loader.docling import DoclingLoader
from langchain_community.document_loaders import (
    BSHTMLLoader,
    CSVLoader,
    UnstructuredEmailLoader,
    UnstructuredImageLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredXMLLoader,
    UnstructuredExcelLoader,
    UnstructuredPDFLoader,
    UnstructuredPowerPointLoader,
    TextLoader
    )
class LoaderConfig(BaseModel):
  loader: type[BaseLoader]
  kwargs: Optional[dict[str, Any]] = {}
  #post_processors: Optional[list[Callable[[str], str]]] = None

class Loader():
  def __init__(self, knowledgebase_path: str):
    self.knowledgebase_path = knowledgebase_path
    self._runtime_options = config.runtime_options()

  _list: dict[str, LoaderConfig | None] = {
    '.json': LoaderConfig(loader=JsonLoader),
    '.csv': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":CSVLoader}),
    '.xls': None,
    '.xlsx': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredExcelLoader, "strategy":"auto"}),
    '.eml': LoaderConfig(loader=UnstructuredEmailLoader,kwargs={"strategy":"auto", "process_attachments": False}),
    '.msg': LoaderConfig(loader=UnstructuredEmailLoader,kwargs={"strategy":"auto", "process_attachments": False}),
    '.epub': None,
    '.md': LoaderConfig(loader=TextLoader, kwargs={"autodetect_encoding": True}),
    '.org': None,
    '.odt': None,
    '.ppt': None,
    '.pptx': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredPowerPointLoader, "strategy":"auto"}),
    '.txt': LoaderConfig(loader=TextLoader, kwargs={"autodetect_encoding": True}),
    '.rst': None,
    '.rtf': None,
    '.tsv': None,
    '.text': None,
    '.log': None,
    '.htm': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":BSHTMLLoader}),
    '.html': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":BSHTMLLoader}),
    ".pdf": LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredPDFLoader, "strategy":"auto"}),
    '.png': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredImageLoader, "strategy":"auto"}),
    '.jpg': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredImageLoader, "strategy":"auto"}),
    '.jpeg': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredImageLoader, "strategy":"auto"}),
    '.gif': None,
    ".emf": None,
    ".wmf": None,
    '.tiff': None,
    '.doc': None, #see liberoffice dependency
    '.docx': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredWordDocumentLoader, "strategy":"auto"}),
    '.xml': LoaderConfig(loader=DoclingLoader, kwargs={"fallback":UnstructuredXMLLoader, "strategy":"auto"}),
    '.js': None,
    '.py': None,
    '.c': None,
    '.cc': None,
    '.cpp': None,
    '.java': None,
    '.cs': None,
    '.php': None,
    '.rb': None,
    '.swift': None,
    '.ts': None,
    '.go': None,
  }

  @staticmethod
  def managed_file_extensions() -> list[str]:
    return [k for k,v in Loader._list.items() if v is not None]

  #@timer
  def __directory_loader(self) -> list[DirectoryLoader]:
    loader_configs = {}
    for ext, loader_config in Loader._list.items():
        if loader_config:
            loader_key = (loader_config.loader, tuple(loader_config.kwargs.items())) # type: ignore
            if loader_key not in loader_configs:
                loader_configs[loader_key] = {
                    "loader_cls": loader_config.loader,
                    "loader_kwargs": loader_config.kwargs,
                    "glob_patterns": []
                }
            loader_configs[loader_key]["glob_patterns"].append(f"**/*{ext}")
    loaders = []

    for loader_config in loader_configs.values():
        loaders.append(
          DirectoryLoader(
            os.path.abspath(self.knowledgebase_path),
            glob=loader_config["glob_patterns"],
            loader_cls=loader_config["loader_cls"],
            loader_kwargs=loader_config["loader_kwargs"],
            show_progress=self._runtime_options.loader_show_progress,
            recursive=True,
            silent_errors=True, #self._runtime_options.loader_silent_errors,
            use_multithreading=config.robot_loader_max_threads>1,
            max_concurrency=config.robot_loader_max_threads,
            #sample_size=200
          )
        )
    return loaders

  #@timer
  async def load(self) -> list[Document]:
    #region log
    import warnings
    warnings.filterwarnings("ignore", message=".*pin_memory.*no accelerator is found.*")
    warnings.filterwarnings("ignore", category=UserWarning)
    log_msg_to_ignore = [
        "Going to convert document batch...",
        "Initializing pipeline for",
        "Accelerator device:",
        "detected formats:",
        "The text detection result is empty",
        "RapidOCR returned empty result!",       
    ]
    class MessageFilter(logging.Filter):
        def __init__(self, patterns):
            super().__init__()
            self.log_msg_to_ignore = patterns

        def filter(self, record):
            for pattern in self.log_msg_to_ignore:
                if pattern in record.getMessage():
                    return False
            return True
    message_filter = MessageFilter(log_msg_to_ignore)
    loggers_to_filter = [
        'docling',
        'docling.document_converter',
        'docling.datamodel',
        'docling.datamodel.document',
        'docling.models',
        'docling.models.rapidocr_model',
        'docling.utils.accelerator_utils',
        'unstructured',
        'RapidOCR'
    ]
    for logger_name in loggers_to_filter:
        logging.getLogger(logger_name).addFilter(message_filter)
    #endregion log

    MAX_RETRIES = 3
    loaders: MergedDataLoader = MergedDataLoader(self.__directory_loader())
    try:
      for attempt in range(MAX_RETRIES):
        try:
          _documents = []
          async for document in loaders.alazy_load():
            _documents.append(document)
          return _documents
        except Exception as e:
          logging.warning(f"Attempt {attempt+1} load document  failed: {e}")
          await asyncio.sleep(2)
          if attempt == MAX_RETRIES - 1:
            tb = traceback.format_exc()
            logging.error(f"Failed to load documents: {e} | {tb}")
            return []
        finally:
           del _documents
    finally:
      # Remove logging filters
      for logger_name in loggers_to_filter:
          logging.getLogger(logger_name).removeFilter(message_filter)
      del loaders
      gc.collect()
