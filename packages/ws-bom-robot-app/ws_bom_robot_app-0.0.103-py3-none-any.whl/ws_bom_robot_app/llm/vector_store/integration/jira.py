import logging
import asyncio, os
import sys
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from pydantic import BaseModel, Field, AliasChoices
from typing import Any, Generator, Iterable, Optional, Union
from unstructured_ingest.pipeline.pipeline import Pipeline
from unstructured_ingest.processes.connectors.jira import (
    JiraIndexerConfig,
    JiraIndexer,
    JiraIssueMetadata,
    api_page_based_generator,
    JiraDownloaderConfig,
    JiraDownloader,
    DEFAULT_C_SEP,
    DEFAULT_R_SEP,
    JiraConnectionConfig,
    JiraAccessConfig
)
from unstructured_ingest.pipeline.pipeline import (
  Pipeline,
  PartitionerConfig,
  FiltererConfig
)
from unstructured_ingest.interfaces import ProcessorConfig

class JiraParams(BaseModel):
  """
  JiraParams is a Pydantic model that represents the parameters required to interact with a Jira instance.
  Docs: https://docs.unstructured.io/open-source/ingestion/source-connectors/jira#jira

  Attributes:
    url (str): The URL of the Jira instance, e.g., 'https://example.atlassian.net'.
    access_token (str): The access token for authenticating with the Jira API: https://id.atlassian.com/manage-profile/security/api-tokens
    user_email (str): The email address of the Jira user.
    projects (list[str]): A list of project keys or IDs to interact with, e.g., ['SCRUM', 'PROJ1'].
    boards (Optional[list[str]]): An optional list of board IDs to interact with. Defaults to None, e.g., ['1', '2'].
    issues (Optional[list[str]]): An optional list of issue keys or IDs to interact with. Defaults to None, e.g., ['SCRUM-1', 'PROJ1-1'].
  """
  url: str = Field(..., pattern=r'^https?:\/\/.+')
  access_token: str = Field(..., validation_alias=AliasChoices("accessToken","access_token"), min_length=1)
  user_email: str = Field(validation_alias=AliasChoices("userEmail","user_email"), min_length=1)
  projects: list[str]
  boards: Optional[list[str]] | None = None
  issues: Optional[list[str]] | None = None
  status_filters: Optional[list[str]] | None = None

class Jira(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = JiraParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'jira'
  def run(self) -> None:
    indexer_config = JiraIndexerConfig(
      projects=self.__data.projects,
      boards=self.__data.boards,
      issues=self.__data.issues,
      status_filters=self.__data.status_filters
      )
    downloader_config = JiraDownloaderConfig(
      download_dir=self.working_directory,
      download_attachments=False
    )
    _is_cloud = "atlassian.net" in self.__data.url
    _access_config = JiraAccessConfig(token=self.__data.access_token) \
      if not _is_cloud  \
      else JiraAccessConfig(password=self.__data.access_token)
    connection_config = JiraConnectionConfig(
      access_config=_access_config,
      username=self.__data.user_email,
      url=self.__data.url,
      cloud=_is_cloud
    )
    pipeline: Pipeline = self.__unstructured_ingest.pipeline(
      indexer_config,
      downloader_config,
      connection_config,
      extension=None)
    if _is_cloud and sys.platform == "win32":
      pipeline.indexer_step.process = CustomJiraIndexer(**vars(pipeline.indexer_step.process))
    pipeline.downloader_step.process = CustomJiraDownloader(**vars(pipeline.downloader_step.process))
    pipeline.run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()


# region override
class CustomJiraIndexer(JiraIndexer):
  """
    fix default run_jql for cloud: missing enhanced_jql
  """
  import sys
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
        try:
            setattr(super(), key, value)
        except AttributeError:
            setattr(self, key, value)
  def run_jql(self, jql: str, **kwargs) -> Generator[JiraIssueMetadata, None, None]:
      with self.connection_config.get_client() as client:
          for issue in api_page_based_generator(client.jql, jql=jql, **kwargs):
              yield JiraIssueMetadata.model_validate(issue)

class CustomJiraDownloader(JiraDownloader):
  CUSTOM_FIELDS: list | None = None
  def _set_custom_fields(self) -> list:
    with self.connection_config.get_client() as client:
        _custom_fields = client.get_all_custom_fields()
        return [{"id": item["id"], "name": item["name"]} for item in _custom_fields]
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
        try:
            setattr(super(), key, value)
        except AttributeError:
            setattr(self, key, value)
    if not self.CUSTOM_FIELDS:
      self.CUSTOM_FIELDS = self._set_custom_fields()

  def _get_custom_fields_for_issue(self, issue: dict, c_sep=DEFAULT_C_SEP, r_sep=DEFAULT_R_SEP) -> str:
      def _parse_value(value: Any) -> Any:
          if isinstance(value, dict):
            _candidate = ["displayName", "name", "value"]
            for item in _candidate:
                if item in value:
                    return value[item]
          return value
      def _remap_custom_fields(fields: dict):
        remapped_fields = {}
        for field_key, field_value in fields.items():
          new_key = next((map_item["name"] for map_item in self.CUSTOM_FIELDS if field_key == map_item["id"]), field_key)
          if new_key != field_value:
            remapped_fields[new_key] = field_value
        return remapped_fields
      filtered_fields = {key: _parse_value(value) for key, value in issue.items() if value is not None and type(value) not in [list]}
      custom_fields =_remap_custom_fields(filtered_fields)
      return (r_sep + c_sep ).join([f"{key}: {value}{r_sep}" for key, value in custom_fields.items()])

  def _get_text_fields_for_issue(self, issue: dict, c_sep: str = DEFAULT_C_SEP, r_sep: str = DEFAULT_R_SEP) -> str:
      #no need any more: original data will be included in the custom fields
      #_origin = super()._get_text_fields_for_issue(issue, c_sep=c_sep, r_sep=r_sep)
      _custom_fields = self._get_custom_fields_for_issue(issue, c_sep=c_sep, r_sep=r_sep)
      return f"""Details:
      {r_sep}
      {_custom_fields}"""
# endregion
