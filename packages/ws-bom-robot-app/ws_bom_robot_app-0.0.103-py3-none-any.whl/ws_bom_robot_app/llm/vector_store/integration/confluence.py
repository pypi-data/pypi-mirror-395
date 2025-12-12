import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.confluence import ConfluenceIndexerConfig, ConfluenceIndexer, ConfluenceDownloaderConfig, ConfluenceConnectionConfig, ConfluenceAccessConfig
from unstructured_ingest.pipeline.pipeline import Pipeline
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import List, Optional, Union
from pydantic import BaseModel, Field, AliasChoices

class ConfluenceParams(BaseModel):
  """
  ConfluenceParams is a data model for storing Confluence integration parameters.

  Attributes:
    url (str): The URL of the Confluence instance, e.g., 'https://example.atlassian.net'.
    username (str): The email address or username of the Confluence user
    password: Confluence password or Cloud API token, if filled, set the access_token to None and vice versa.
    access_token (str): The personal access token for authenticating with Confluence, e.g., 'AT....'
    spaces (list[str]): A list of Confluence spaces to interact with, e.g., ['SPACE1', 'SPACE2'].
    max_num_of_docs_from_each_space (int): The maximum number of documents to fetch from each space. Defaults to 500, with a maximum limit of 5000.
    extension (list[str], optional): A list of file extensions to filter by. Defaults to None, e.g., ['.pdf', '.docx'].
  """
  url: str
  username: str = Field(validation_alias=AliasChoices("userName","userEmail","username"))
  password: Optional[str] = None
  access_token: Optional[str] = Field(None, validation_alias=AliasChoices("accessToken","access_token"))
  spaces: list[str] = []
  max_num_of_docs_from_each_space: int = Field(default=500, ge=1, le=5000,validation_alias=AliasChoices("maxNumOfDocsFromEachSpace","max_num_of_docs_from_each_space"))
  extension: list[str] = Field(default=None)
class Confluence(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = ConfluenceParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'confluence'
  def run(self) -> None:
    indexer_config = ConfluenceIndexerConfig(
      spaces=self.__data.spaces,
      max_num_of_docs_from_each_space=self.__data.max_num_of_docs_from_each_space
    )
    downloader_config = ConfluenceDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = ConfluenceConnectionConfig(
      access_config=ConfluenceAccessConfig(password=self.__data.password, token=self.__data.access_token),
      url=self.__data.url,
      username=self.__data.username
    )
    pipeline: Pipeline = self.__unstructured_ingest.pipeline(
      indexer_config,
      downloader_config,
      connection_config,
      extension=self.__data.extension
    )
    pipeline.indexer_step.process = CustomConfluenceIndexer(**vars(pipeline.indexer_step.process))
    pipeline.run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()

class CustomConfluenceIndexer(ConfluenceIndexer):
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
        try:
            setattr(super(), key, value)
        except AttributeError:
            setattr(self, key, value)
  def _get_docs_ids_within_one_space(self, space_key: str) -> List[dict]:
      with self.connection_config.get_client() as client:
          pages = client.get_all_pages_from_space(
              space=space_key,
              start=0,
              limit=self.index_config.max_num_of_docs_from_each_space, #explicitly limit the number of pages fetched (omitted  in unstructured-ingest)
              expand=None,
              content_type="page",  # blogpost and comment types not currently supported
              status=None,
          )
      limited_pages = pages[: self.index_config.max_num_of_docs_from_each_space]
      doc_ids = [{"space_id": space_key, "doc_id": page["id"]} for page in limited_pages]
      return doc_ids

