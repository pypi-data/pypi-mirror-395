import asyncio, logging, aiohttp
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import List, Union, Optional
from pydantic import BaseModel, Field, AliasChoices
import json
import os
import platform
import pandas as pd
from io import BytesIO

# Fix for Windows event loop issue with aiodns
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class ThronParams(BaseModel):
  """
  ThronParams is a model that defines the parameters required for Thron integration.

  Attributes:
    app_id (str): The application ID for Thron.
    client_id (str): The client ID for Thron.
    client_secret (str): The client secret for Thron.
  """
  organization_name: str = Field(validation_alias=AliasChoices("organizationName","organization_name"))
  attribute_fields: Optional[List[str]] = Field(default=None, validation_alias=AliasChoices("attributeFields","attribute_fields"))
  client_id: str = Field(validation_alias=AliasChoices("clientId","client_id"))
  client_secret: str = Field(validation_alias=AliasChoices("clientSecret","client_secret"))

class Thron(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__token = None
    self.__data = ThronParams.model_validate(self.data)

  def working_subdirectory(self) -> str:
    return 'thron'

  async def __ensure_token(self) -> bool:
    """Ensure we have a valid token, getting one if needed."""
    if not self.__token:
      self.__token = await self.__get_auth_token()
    return self.__token is not None

  def __convert_xlsx_to_csv(self, file_content: bytes) -> bool:
    """Convert XLSX file content to CSV and save to working directory."""
    try:
      df = pd.read_excel(BytesIO(file_content))
      csv_path = os.path.join(self.working_directory, 'thron_export.csv')
      df.to_csv(csv_path, index=False, encoding='utf-8')
      return True
    except Exception as e:
      logging.error(f"Error converting XLSX to CSV: {e}")
      return False

  async def run(self) -> None:
    _run_id = await self.__get_data()
    if _run_id:
      await self.__fetch_exported_file(_run_id)

  async def load(self) -> list[Document]:
    await self.run()
    await asyncio.sleep(1)
    return await Loader(self.working_directory).load()

  async def __get_auth_token(self) -> str:
    """
    Get authentication token from Thron API.

    Returns:
      str: The access token if successful, None otherwise.
    """
    try:
      async with aiohttp.ClientSession() as session:
        auth_data = {
          "grant_type": "client_credentials",
          "client_id": self.__data.client_id,
          "client_secret": self.__data.client_secret
        }
        headers = {
          "accept": "application/json",
          "Content-Type": "application/x-www-form-urlencoded"
        }
        async with session.post(f"https://{self.__data.organization_name}.thron.com/api/v1/authentication/oauth2/token", data=auth_data, headers=headers) as response:
          result = await response.json()
          return result.get("access_token", "")
    except Exception as e:
      logging.error(f"Error fetching Thron auth token: {e}")
      return None

  async def __refresh_token(self) -> bool:
    """Refresh the authentication token and update the instance variable."""
    try:
      new_token = await self.__get_auth_token()
      if new_token:
        self.__token = new_token
        logging.info("Thron authentication token refreshed successfully.")
        return True
      else:
        logging.error("Failed to refresh Thron authentication token.")
        return False
    except Exception as e:
      logging.error(f"Error refreshing Thron auth token: {e}")
      return False

  async def __get_data(self) -> str:
    """
    Initiates a data export request to Thron API.

    Returns:
      str: The export ID if successful, None otherwise.
    """
    max_retries = 2
    retry_count = 0

    while retry_count < max_retries:
      try:
        if not await self.__ensure_token():
          logging.error("Failed to obtain Thron authentication token.")
          return {}

        async with aiohttp.ClientSession() as session:
          headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.__token}"
          }
          payload = {"attributes": self.__data.attribute_fields or [],"assetsBy":"CODE","type":"CODES","format":"XLSX","locales":[],"systemAttributes":["family","master","variation","variationGroup","hierarchyLevel"]}
          async with session.post(f"https://{self.__data.organization_name}.thron.com/api/v1/product-sync/exports", headers=headers, json=payload) as response:
            # Check for authentication errors
            if response.status == 401:
              logging.warning("Authentication failed in __get_data, attempting to refresh token...")
              if await self.__refresh_token():
                retry_count += 1
                continue
              else:
                logging.error("Token refresh failed in __get_data.")
                return None

            if response.status not in range(200, 300):
              logging.error(f"API request failed with status {response.status}")
              return None

            result = await response.json()
            return result.get("id", None)

      except Exception as e:
        logging.error(f"Error fetching Thron product data (attempt {retry_count + 1}): {e}")
        if retry_count < max_retries - 1:
          if await self.__refresh_token():
            retry_count += 1
            continue
        retry_count += 1

    logging.error(f"Failed to fetch Thron product data after {max_retries} attempts.")
    return {}


  async def __fetch_exported_file(self, export_id: str) -> bool:
    """
    Fetches the exported file from Thron API using the provided export ID.
    Polls the export status until it's processed, then downloads the XLSX file
    and converts it to CSV format in the working directory.

    Args:
      export_id (str): The ID of the export to fetch.

    Returns:
      bool: True if file was successfully downloaded and converted, False otherwise.
    """
    max_retries = 2
    retry_count = 0

    while retry_count < max_retries:
      try:
        # Ensure we have a token
        if not await self.__ensure_token():
          logging.error("Failed to obtain Thron authentication token.")
          return {}

        async with aiohttp.ClientSession() as session:
          headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.__token}"
          }

          # Polling until status is PROCESSED
          while True:
            async with session.get(f"https://{self.__data.organization_name}.thron.com/api/v1/product-sync/exports/{export_id}", headers=headers) as response:
              # Check for authentication errors
              if response.status == 401:
                logging.warning("Authentication failed, attempting to refresh token...")
                if await self.__refresh_token():
                  headers["Authorization"] = f"Bearer {self.__token}"
                  continue
                else:
                  logging.error("Token refresh failed, aborting request.")
                  return {}

              if response.status != 200:
                logging.error(f"API request failed with status {response.status}")
                break

              result = await response.json()
              if result.get("status") == "PROCESSED":
                download_uri = result.get("downloadUri")
                if download_uri:
                  async with session.get(download_uri) as file_response:
                    if file_response.status == 200:
                      # Download XLSX file
                      file_content = await file_response.read()
                      return self.__convert_xlsx_to_csv(file_content)

                    elif file_response.status == 401:
                      logging.warning("Authentication failed during file download, attempting to refresh token...")
                      if await self.__refresh_token():
                        retry_count += 1
                        break
                      else:
                        logging.error("Token refresh failed during file download.")
                        return False
                break

              await asyncio.sleep(5)
        return False

      except Exception as e:
        logging.error(f"Error fetching exported data (attempt {retry_count + 1}): {e}")
        if retry_count < max_retries - 1:
          if await self.__refresh_token():
            retry_count += 1
            continue
        retry_count += 1

    logging.error(f"Failed to fetch exported data after {max_retries} attempts.")
    return False
