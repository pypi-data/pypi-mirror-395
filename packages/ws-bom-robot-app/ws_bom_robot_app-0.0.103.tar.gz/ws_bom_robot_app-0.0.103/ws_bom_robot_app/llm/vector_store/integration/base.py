import os, copy
from random import random
from langchain_core.documents import Document
from abc import ABC, abstractmethod
from unstructured_ingest.interfaces import ProcessorConfig
from unstructured_ingest.pipeline.pipeline import (
  Pipeline,
  PartitionerConfig,
  FiltererConfig
)
from unstructured_ingest.processes.connector_registry import source_registry
from typing import Union
from ws_bom_robot_app.llm.utils.secrets import Secrets
from ws_bom_robot_app.config import config

class IntegrationStrategy(ABC):
  @classmethod
  def _parse_data(cls, data: dict[str, Union[str, int, list]]) -> dict[str, Union[str, int, list]]:
    for key, fn in (
      ("__from_env", Secrets.from_env),
      ("__from_file", Secrets.from_file),
    ):
      if key in data:
        if secret := fn(data[key]):
          return secret
    return data
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    self.knowledgebase_path = knowledgebase_path
    self.data = self._parse_data(data)
    self.working_directory = os.path.join(self.knowledgebase_path,self.working_subdirectory())
    os.makedirs(self.working_directory, exist_ok=True)
  @property
  @abstractmethod
  def working_subdirectory(self) -> str:
    pass
  @abstractmethod
  #@timer
  def load(self) -> list[Document]:
    pass

class UnstructuredIngest():
  _PIPELINE: Pipeline = None
  def __init__(self, working_directory: str):
    self.working_directory = working_directory
    self._runtime_options = config.runtime_options()
  def pipeline(self,indexer_config,downloader_config,connection_config,extension: list[str] = None) -> Pipeline:
    def _default_processor_config() -> ProcessorConfig:
      return ProcessorConfig(
        reprocess=False,
        verbose=False,
        tqdm=False,
        num_processes=config.robot_ingest_max_threads, #safe choice to 1, avoid potential process-related issues with Docker
        disable_parallelism=False,
        preserve_downloads=True,
        download_only=True,
        raise_on_error=False,
        iter_delete=True,
        delete_cache=False #already managed by the generator task
      )
    def _init_pipeline() -> Pipeline:
      return Pipeline.from_configs(
        context=_default_processor_config(),
        indexer_config=indexer_config,
        downloader_config=downloader_config,
        source_connection_config=connection_config,
        partitioner_config=PartitionerConfig(),
        filterer_config=FiltererConfig(file_glob=[f"**/*{ext}" for ext in extension] if extension else None)
      )
    def _instance_pipeline() -> Pipeline:
        from unstructured_ingest.pipeline.steps.index import  IndexStep
        from unstructured_ingest.pipeline.steps.download import  DownloadStep
        from unstructured_ingest.pipeline.steps.filter import Filterer, FilterStep
        _context = _default_processor_config()
        source_entry = {
                    k: v
                    for k, v in source_registry.items()
                    if type(indexer_config) is v.indexer_config
                    and type(downloader_config) is v.downloader_config
                    and type(connection_config) is v.connection_config
                }
        source = list(source_entry.values())[0]
        _pipeline = copy.deepcopy(UnstructuredIngest._PIPELINE)
        _pipeline.context = _context
        _pipeline.context.work_dir = f"{self.working_directory}_unstructured" # use sibling directory, cleaned up by the generator task
        _pipeline.indexer_step = IndexStep(process=source.indexer(index_config=indexer_config, connection_config=connection_config), context=_context)
        _pipeline.downloader_step = DownloadStep(process=source.downloader(download_config=downloader_config, connection_config=connection_config), context=_context)
        _pipeline.filter_step = FilterStep(process=Filterer(config=FiltererConfig(file_glob=[f"**/*{ext}" for ext in extension] if extension else None)), context=_context) if extension else None
        return _pipeline

    if not UnstructuredIngest._PIPELINE:
      import random
      import time
      time.sleep(random.uniform(0.2, 1))
      if not UnstructuredIngest._PIPELINE:
        UnstructuredIngest._PIPELINE = _init_pipeline()

    return _instance_pipeline()
