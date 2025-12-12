import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.fsspec.s3 import S3ConnectionConfig, S3AccessConfig, S3DownloaderConfig, S3IndexerConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union, Optional
from pydantic import BaseModel, Field, AliasChoices
class S3Params(BaseModel):
  """
  S3Params is a data model for storing parameters required to interact with an S3 bucket.
  Documentation:
    - ceate S3 bucket: https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html#creating-bucket
    - enable authenticated bucket access: https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html
    - set policies s3:ListBucket and s3:GetObject: https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-policies-s3.html
    - generate key/secret: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey
    - optionally create STS token: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#api_getsessiontoken

  Attributes:
    remote_url (str): The URL of the remote S3 bucket, e.g., 's3://demo-bucket' or 's3://demo-bucket/sub-directory'.
    key (Optional[str]): The AWS access key ID for the authenticated AWS IAM user, e.g., 'AKIAIOSFODNN7EXAMPLE'.
    secret (Optional[str]): The corresponding AWS secret access key, e.g., 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'.
    token (Optional[str]):  If required, the AWS STS session token for temporary access. Default is None.
    recursive (bool): A flag indicating whether to perform operations recursively. Default is False.
    extension (list[str]): A list of file extensions to filter the files. Default is None. e.g., ['.pdf', '.docx'].
  """
  remote_url: str = Field(validation_alias=AliasChoices("remoteUrl","remote_url"))
  key: str
  secret: str
  token: Optional[str]  = None
  recursive: bool = False
  extension: list[str] = Field(default=None)
class S3(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = S3Params.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 's3'
  def run(self) -> None:
    indexer_config = S3IndexerConfig(
      remote_url=self.__data.remote_url,
      recursive=self.__data.recursive,
      #sample_n_files=1
    )
    downloader_config = S3DownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = S3ConnectionConfig(
      access_config=S3AccessConfig(
        key=self.__data.key,
        secret=self.__data.secret,
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

