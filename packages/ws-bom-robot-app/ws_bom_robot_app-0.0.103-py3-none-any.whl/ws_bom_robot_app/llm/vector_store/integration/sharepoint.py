import asyncio, logging, traceback
from dataclasses import dataclass
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.sharepoint  import SharepointIndexerConfig, SharepointIndexer, SharepointDownloaderConfig, SharepointConnectionConfig, SharepointAccessConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union, Optional
from pydantic import BaseModel, Field, AliasChoices

class SharepointParams(BaseModel):
  """
  SharepointParams is a Pydantic model that defines the parameters required to connect to a SharePoint site.

  Attributes:
    client_id (str): The client ID for SharePoint authentication.
    client_secret (str): The client secret for SharePoint authentication.
    tenant_id (str, optional): The tenant ID for SharePoint authentication. Defaults to None.
    site_url (str): The URL of the SharePoint site. i.e. site collection level: https://<tenant>.sharepoint.com/sites/<site-collection-name>, or root site: https://<tenant>.sharepoint.com
    site_path (str, optional): TThe path in the SharePoint site from which to start parsing files, for example "Shared Documents". Defaults to None.
    recursive (bool, optional): Whether to recursively access subdirectories. Defaults to False.
    extension (list[str], optional): A list of file extensions to include, i.e. [".pdf"]  Defaults to None.
  """
  client_id : str = Field(validation_alias=AliasChoices("clientId","client_id"))
  client_secret : str = Field(validation_alias=AliasChoices("clientSecret","client_secret"))
  site_url: str = Field(validation_alias=AliasChoices("siteUrl","site_url"))
  site_path: str = Field(default=None,validation_alias=AliasChoices("sitePath","site_path"))
  tenant_id: str = Field(default=None, validation_alias=AliasChoices("tenantId","tenant_id"))
  recursive: bool = Field(default=False)
  extension: list[str] = Field(default=None)
class Sharepoint(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = SharepointParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'sharepoint'
  def run(self) -> None:
    indexer_config = SharepointIndexerConfig(
      path=self.__data.site_path,
      recursive=self.__data.recursive
    )
    downloader_config = SharepointDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = SharepointConnectionConfig(
      access_config=SharepointAccessConfig(client_cred=self.__data.client_secret),
      client_id=self.__data.client_id,
      site=self.__data.site_url,
      tenant= self.__data.tenant_id if self.__data.tenant_id else None
    )
    pipeline = self.__unstructured_ingest.pipeline(
      indexer_config,
      downloader_config,
      connection_config,
      extension=self.__data.extension)
    #current_indexer_process = pipeline.indexer_step.process
    #pipeline.indexer_step.process = CustomSharepointIndexer(**vars(current_indexer_process))
    pipeline.run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()

@dataclass
class CustomSharepointIndexer(SharepointIndexer):
  def __init__(self, **kwargs):
      # Initialize all attributes from the base indexer
      for key, value in kwargs.items():
          setattr(self, key, value)
  def list_files(self, folder, recursive):
      try:
        _files = super().list_files(folder, recursive)
        return _files
      except Exception as e:
        tb = traceback.format_exc()
        logging.error(f"Error listing sharepoint files: {e} \n {tb}")
        return []
  def file_to_file_data(self, client, file):
    try:
      return super().file_to_file_data(client, file)
    except Exception as e:
      tb = traceback.format_exc()
      logging.error(f"Error converting sharepoint file {file} to data: {e} \n {tb}")
      return None
  def list_pages(self, client):
    try:
      _pages = super().list_pages(client)
      _allowed_content_type = None
      for page in _pages:
        # determine the allowed content type from the first page (Home.aspx)
        if not _allowed_content_type:
          _allowed_content_type = page.content_type_id
        if not page.content_type_id == _allowed_content_type:
          _pages.remove_child(page)
      return _pages
    except Exception as e:
      tb = traceback.format_exc()
      logging.error(f"Error listing sharepoint pages: {e} \n {tb}")
      return []
