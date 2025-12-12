import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.fsspec.dropbox import DropboxConnectionConfig, DropboxAccessConfig, DropboxDownloaderConfig, DropboxIndexerConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union
from pydantic import BaseModel, Field, AliasChoices
class DropboxParams(BaseModel):
  """
  DropboxParams is a model for storing parameters required to interact with Dropbox.

  Attributes:
    remote_url (str): The URL of the remote Dropbox location, e.g. 'dropbox://demo-directory' or 'dropbox://demo-directory/sub-directory'.
    token (str): The authentication token for accessing Dropbox.
      create app: https://www.dropbox.com/developers, with file.content.read permission, and generate token, or use existing app: https://www.dropbox.com/account/connected_apps / https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps
    recursive (bool, optional): A flag indicating whether to search directories recursively. Defaults to False.
    extension (list[str], optional): A list of file extensions to filter by. Defaults to None, e.g. ['.pdf', '.docx'].
  """
  remote_url: str = Field(validation_alias=AliasChoices("remoteUrl","remote_url"))
  token: str
  recursive: bool = False
  extension: list[str] = Field(default=None)
class Dropbox(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = DropboxParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'dropbox'
  def run(self) -> None:
    indexer_config = DropboxIndexerConfig(
      remote_url=self.__data.remote_url,
      recursive=self.__data.recursive,
      #sample_n_files=1
    )
    downloader_config = DropboxDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = DropboxConnectionConfig(
      access_config=DropboxAccessConfig(
        token=self.__data.token
        )
    )
    self.__unstructured_ingest.pipeline(
      indexer_config,
      downloader_config,
      connection_config,
      extension=self.__data.extension).run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()

