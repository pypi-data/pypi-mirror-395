import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.interfaces.downloader import DownloaderConfig
from unstructured_ingest.processes.connectors.slack import SlackIndexerConfig, SlackDownloaderConfig, SlackConnectionConfig, SlackAccessConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union
from pydantic import BaseModel, Field, AliasChoices
from datetime import datetime, timedelta

class SlackParams(BaseModel):
  """
  SlackParams is a data model for storing Slack integration parameters.
  Documentation:
    - create slack app: https://api.slack.com/quickstart#creating
    - set channels:history scope: https://api.slack.com/quickstart#scopes
    - installing app/get token: https://api.slack.com/quickstart#installing
    - add app to channel/s

  Attributes:
    token (str): The authentication token for accessing the Slack API.
    channels (list[str]): A list of Slack channel IDs, e.g. ['C01B2PZQX1V'].
    num_days (int, optional): The number of days to retrieve messages from. Defaults to 7.
    extension (list[str], optional): A list of file extensions to filter messages by, e.g. [".xml"]. Defaults to None.
  """
  token: str
  channels: list[str]
  num_days: int = Field(default=7,validation_alias=AliasChoices("numDays","num_days"))
  extension: list[str] = Field(default=None)
class Slack(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = SlackParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'slack'
  def run(self) -> None:
    indexer_config = SlackIndexerConfig(
      channels=self.__data.channels,
      start_date=datetime.now() - timedelta(days=self.__data.num_days),
      end_date=datetime.now()
    )
    downloader_config = DownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = SlackConnectionConfig(
      access_config=SlackAccessConfig(token=self.__data.token)
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

