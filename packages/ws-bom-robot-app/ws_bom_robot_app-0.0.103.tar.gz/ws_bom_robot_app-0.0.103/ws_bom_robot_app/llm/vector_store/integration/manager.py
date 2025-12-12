from typing import Type
from ws_bom_robot_app.llm.vector_store.integration.azure import Azure
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from ws_bom_robot_app.llm.vector_store.integration.confluence import Confluence
from ws_bom_robot_app.llm.vector_store.integration.dropbox import Dropbox
from ws_bom_robot_app.llm.vector_store.integration.gcs import Gcs
from ws_bom_robot_app.llm.vector_store.integration.github import Github
from ws_bom_robot_app.llm.vector_store.integration.googledrive import GoogleDrive
from ws_bom_robot_app.llm.vector_store.integration.jira import Jira
from ws_bom_robot_app.llm.vector_store.integration.s3 import S3
from ws_bom_robot_app.llm.vector_store.integration.sftp import Sftp
from ws_bom_robot_app.llm.vector_store.integration.sharepoint import Sharepoint
from ws_bom_robot_app.llm.vector_store.integration.sitemap import Sitemap
from ws_bom_robot_app.llm.vector_store.integration.slack import Slack
from ws_bom_robot_app.llm.vector_store.integration.thron import Thron
from ws_bom_robot_app.llm.vector_store.integration.shopify import Shopify
from ws_bom_robot_app.llm.vector_store.integration.api import Api
class IntegrationManager:
  _list: dict[str, Type[IntegrationStrategy]] = {
    "llmkbazure": Azure,
    "llmkbconfluence": Confluence,
    "llmkbdropbox": Dropbox,
    "llmkbgithub": Github,
    "llmkbgcs": Gcs,
    "llmkbgoogledrive": GoogleDrive,
    "llmkbjira": Jira,
    "llmkbs3": S3,
    "llmkbsftp": Sftp,
    "llmkbsharepoint": Sharepoint,
    "llmkbsitemap": Sitemap,
    "llmkbslack": Slack,
    "llmkbthron": Thron,
    "llmkbshopify": Shopify,
    "llmkbapi": Api,
  }
  @classmethod
  def get_strategy(cls, name: str, knowledgebase_path: str, data: dict[str, str]) -> IntegrationStrategy:
      if name not in cls._list:
          raise ValueError(f"Integration strategy '{name}' not found")
      return cls._list[name](knowledgebase_path, data)
