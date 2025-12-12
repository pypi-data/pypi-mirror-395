import asyncio
import json
from pathlib import Path
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.google_drive import GoogleDriveConnectionConfig, GoogleDriveDownloaderConfig, GoogleDriveIndexerConfig, GoogleDriveAccessConfig
from unstructured_ingest.data_types.file_data import FileData as OriginalFileData, BatchFileData as OriginalBatchFileData
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union
from pydantic import BaseModel, Field, AliasChoices

# UTF-8 safe FileData classes
class FileData(OriginalFileData):
  @classmethod
  def from_file(cls, path: str):
    path = Path(path).resolve()
    if not path.exists() or not path.is_file():
      raise ValueError(f"file path not valid: {path}")
    for encoding in ['utf-8', 'cp1252', 'iso-8859-1', 'latin-1']:
      try:
        with open(str(path), "r", encoding=encoding) as f:
          return cls.model_validate(json.load(f))
      except (UnicodeDecodeError, UnicodeError):
        continue
    raise ValueError(f"Could not decode file {path} with any supported encoding")

  def to_file(self, path: str) -> None:
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), "w", encoding="utf-8") as f:
      json.dump(self.model_dump(), f, indent=2, ensure_ascii=False)

class BatchFileData(OriginalBatchFileData, FileData):
  pass

class GoogleDriveParams(BaseModel):
  """
  GoogleDriveParams is a model that holds parameters for Google Drive integration.

  Attributes:
    service_account_key (dict): The service account key for Google Drive API authentication \n
      - detail: https://developers.google.com/workspace/guides/create-credentials#service-accountc \n
      - create a service account key, download the JSON file, and pass the content of the JSON file as a dictionary \n
      - e.g., {
        "type": "service_account",
        "project_id": "demo-project-123456",
        "private_key_id": "**********",
        "private_key": "-----BEGIN PRIVATE KEY-----...----END PRIVATE KEY-----",
        "client_email": "demo-client@demo-project-123456.iam.gserviceaccount.com",
        "client_id": "123456",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/demo-client%40demo-project-123456.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
      }
      - enable Google Drive API: https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com
      - copy email address of the service account and share the Google Drive with the email address: https://www.youtube.com/watch?v=ykJQzEe_2dM&t=2s

    drive_id (str): The {folder_id} of the Google Drive to interact with, e.g., https://drive.google.com/drive/folders/{folder_id}
    extensions (list[str]): A list of file extensions to filter the files in the Google Drive, e.g., ['.pdf', '.docx'].
    recursive (bool): A flag indicating whether to search files recursively in the Google Drive.
  """
  service_account_key: dict = Field(validation_alias=AliasChoices("serviceAccountKey","service_account_key"))
  drive_id: str = Field(validation_alias=AliasChoices("driveId","drive_id"))
  extensions: list[str] = []
  recursive: bool = False
class GoogleDrive(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = GoogleDriveParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
    self._apply_encoding_fix()

  def _apply_encoding_fix(self):
    """Replace FileData classes with UTF-8 safe versions"""
    import unstructured_ingest.data_types.file_data as fd
    fd.FileData = FileData
    fd.BatchFileData = BatchFileData
    fd.file_data_from_file = lambda path: BatchFileData.from_file(path) if path else FileData.from_file(path)

  def working_subdirectory(self) -> str:
    return 'googledrive'

  def run(self) -> None:
    self.__unstructured_ingest.pipeline(
      GoogleDriveIndexerConfig(extensions=self.__data.extensions, recursive=self.__data.recursive),
      GoogleDriveDownloaderConfig(download_dir=self.working_directory),
      GoogleDriveConnectionConfig(
        access_config=GoogleDriveAccessConfig(service_account_key=self.__data.service_account_key),
        drive_id=self.__data.drive_id
      )
    ).run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()

