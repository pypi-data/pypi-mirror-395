import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.fsspec.azure import AzureConnectionConfig, AzureAccessConfig, AzureDownloaderConfig, AzureIndexerConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union, Optional
from pydantic import BaseModel, Field, AliasChoices
class AzureParams(BaseModel):
  """
  AzureParams is a model that holds configuration parameters for connecting to Azure services.

  Attributes:
    remote_url (str): The URL of the remote Azure service, in the form az://<container> or az://<container>/<path> for sub-folders.
    account_name (str): The name of the Azure storage account.
    \nProvide one of the following:
      - account_key (Optional[str]): The key for the Azure storage account. Default is None.
      - connection_string (Optional[str]): The connection string for the Azure storage account. Default is None.
      - sas_token (Optional[str]): The Shared Access Signature token for the Azure storage account. Default is None. Detail: https://learn.microsoft.com/en-us/azure/ai-services/translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers
    recursive (bool): Indicates whether the operation should be recursive. Default is False.
    extension (list[str]): A list of file extensions to filter the files. Default is None.
  """
  remote_url: str = Field(validation_alias=AliasChoices("remoteUrl","remote_url"))
  account_name: str = Field(validation_alias=AliasChoices("accountName","account_name"))
  account_key: Optional[str] = Field(default=None,validation_alias=AliasChoices("accountKey","account_key"))
  connection_string: Optional[str]  = Field(default=None,validation_alias=AliasChoices("connectionString","connection_string"))
  sas_token: Optional[str]  = Field(default=None,validation_alias=AliasChoices("sasToken","sas_token"))
  recursive: bool = False
  extension: list[str] = Field(default=None)
class Azure(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = AzureParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'azure'
  def run(self) -> None:
    indexer_config = AzureIndexerConfig(
      remote_url=self.__data.remote_url,
      recursive=self.__data.recursive,
      #sample_n_files=1
    )
    downloader_config = AzureDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = AzureConnectionConfig(
      access_config=AzureAccessConfig(
        account_name=self.__data.account_name,
        account_key=self.__data.account_key,
        connection_string=self.__data.connection_string,
        sas_token=self.__data.sas_token
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

