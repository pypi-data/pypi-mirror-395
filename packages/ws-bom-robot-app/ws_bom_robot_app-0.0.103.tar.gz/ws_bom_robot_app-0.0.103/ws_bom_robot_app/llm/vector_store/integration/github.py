import asyncio
from typing import Optional, Union
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.processes.connectors.github import (
    GithubIndexerConfig,
    GithubDownloaderConfig,
    GithubConnectionConfig,
    GithubAccessConfig
)
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from pydantic import BaseModel, Field, AliasChoices

class GithubParams(BaseModel):
  """
  GithubParams is a model for storing parameters required to interact with a GitHub repository.

  Attributes:
    repo (str): The name of the GitHub repository, e.g., 'companyname/reponame'
    access_token (Optional[str]): The access token for authenticating with GitHub, e.g., 'ghp_1234567890'.
    branch (Optional[str]): The branch of the repository to interact with. Defaults to 'main'.
    file_ext (Optional[list[str]]): A list of file extensions to filter by, e.g. ['.md', '.pdf']. Defaults to an empty list.
  """
  repo: str
  access_token: Optional[str] | None = Field(None,validation_alias=AliasChoices("accessToken","access_token"))
  branch: Optional[str] = 'main'
  file_ext: Optional[list[str]] = Field(default_factory=list, validation_alias=AliasChoices("fileExt","file_ext"))
class Github(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = GithubParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'github'
  def run(self) -> None:
    indexer_config = GithubIndexerConfig(
      branch=self.__data.branch,
      recursive=True
    )
    downloader_config = GithubDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = GithubConnectionConfig(
      access_config=GithubAccessConfig(access_token=self.__data.access_token),
      url=self.__data.repo
    )
    self.__unstructured_ingest.pipeline(
      indexer_config,
      downloader_config,
      connection_config,
      extension=self.__data.file_ext).run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()
