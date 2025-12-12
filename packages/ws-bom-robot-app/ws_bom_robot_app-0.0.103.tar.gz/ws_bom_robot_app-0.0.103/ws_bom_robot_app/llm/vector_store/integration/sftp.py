import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.fsspec.sftp import SftpConnectionConfig, SftpAccessConfig, SftpDownloaderConfig, SftpIndexerConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union, Optional
from pydantic import BaseModel, Field, AliasChoices
class SftpParams(BaseModel):
  """
  SftpParams is a model that defines the parameters required for SFTP integration.

  Attributes:
    remote_url (str): The URL of the remote SFTP server, e.g. 'sftp://example.com' or 'sftp://example.com/directory'.
    host (Optional[str]): The hostname or IP address of the SFTP server. Defaults to None and inferred from remote_url
    port (Optional[int]): The port number to connect to on the SFTP server. Defaults to 22.
    username (str): The username to authenticate with the SFTP server.
    password (str): The password to authenticate with the SFTP server.
    recursive (bool): Whether to perform recursive operations. Defaults to False.
    extension (list[str]): A list of file extensions to filter by. Defaults to None, e.g. ['.pdf', '.docx'].
  """
  remote_url: str = Field(validation_alias=AliasChoices("remoteUrl","remote_url"))
  host: Optional[str] = None
  port: Optional[int] = 22
  username: str
  password: str
  recursive: bool = False
  extension: list[str] = Field(default=None)
class Sftp(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = SftpParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'sftp'
  def run(self) -> None:
    indexer_config = SftpIndexerConfig(
      remote_url=self.__data.remote_url,
      recursive=self.__data.recursive,
      #sample_n_files=1
    )
    downloader_config = SftpDownloaderConfig(
      download_dir=self.working_directory,
      remote_url=self.__data.remote_url
    )
    connection_config = SftpConnectionConfig(
      access_config=SftpAccessConfig(
        password=self.__data.password
        ),
      username=self.__data.username,
      host=self.__data.host,
      port=self.__data.port,
      look_for_keys=False,
      allow_agent=False
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

