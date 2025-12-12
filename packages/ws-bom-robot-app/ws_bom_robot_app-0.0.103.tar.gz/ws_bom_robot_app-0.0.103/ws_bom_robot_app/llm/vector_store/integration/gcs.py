import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.fsspec.gcs import GcsIndexerConfig, GcsConnectionConfig, GcsAccessConfig, GcsDownloaderConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union, Optional
from pydantic import BaseModel, Field, AliasChoices
class GcsParams(BaseModel):
  """
  GcsParams is a model that defines the parameters required for Google Cloud Storage (GCS) integration.
  Documentation:
    - create service account: https://cloud.google.com/iam/docs/service-accounts-create?hl=en#console
    - create key: https://cloud.google.com/iam/docs/keys-create-delete?hl=en#creating
    - export key in a single line\n
    ```pwsh
    (Get-Content -Path "<path-to-downloaded-key-file>" -Raw).Replace("`r`n", "").Replace("`n", "")
    ```
    - create bucket with 'Storage Object Viewer' permission: https://cloud.google.com/storage/docs/creating-buckets?hl=en#console
    - add principal to bucket: https://cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=en#console
    - manage IAM policies: https://cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=en

  Attributes:
    remote_url (str): The URL of the remote GCS bucket, e.g. 'gcs://demo-bucket' or 'gcs://demo-bucket/sub-directory'.
    service_account_key (str): The service account key for accessing the GCS bucket.
    recursive (bool): A flag indicating whether to recursively access the GCS bucket. Defaults to False.
    extension (list[str]): A list of file extensions to filter the files in the GCS bucket. Defaults to None.
  """
  remote_url: str = Field(validation_alias=AliasChoices("remoteUrl","remote_url"))
  service_account_key: str = Field(validation_alias=AliasChoices("serviceAccountKey","service_account_key"))
  recursive: bool = False
  extension: list[str] = Field(default=None)
class Gcs(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = GcsParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'gcs'
  def run(self) -> None:
    indexer_config = GcsIndexerConfig(
      remote_url=self.__data.remote_url,
      recursive=self.__data.recursive,
      #sample_n_files=1
    )
    downloader_config = GcsDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = GcsConnectionConfig(
      access_config=GcsAccessConfig(
        service_account_key=self.__data.service_account_key
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

