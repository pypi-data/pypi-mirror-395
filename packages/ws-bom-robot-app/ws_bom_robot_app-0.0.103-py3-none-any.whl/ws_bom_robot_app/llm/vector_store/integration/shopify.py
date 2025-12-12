import asyncio, logging, aiohttp
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import List, Union, Optional
from pydantic import BaseModel, Field, AliasChoices, field_validator
import json
import os

class ShopifyParams(BaseModel):
  """
  ShopifyParams is a model that defines the parameters required for Shopify integration.

  Attributes:
    shop_name (str): The shop name for Shopify.
    access_token (str): The access token for Shopify.
    graphql_query (Union[str, dict]): The GraphQL query string or dict for Shopify.
  """
  shop_name: str = Field(validation_alias=AliasChoices("shopName","shop_name"))
  access_token: str = Field(validation_alias=AliasChoices("accessToken","access_token"))
  graphql_query: Union[str, dict] = Field(validation_alias=AliasChoices("graphqlQuery","graphql_query"))

  @field_validator('graphql_query')
  @classmethod
  def extract_query_string(cls, v):
    """Extract the query string from dict format if needed"""
    if isinstance(v, dict) and 'query' in v:
      return v['query']
    return v

class Shopify(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = ShopifyParams.model_validate(self.data)

  def working_subdirectory(self) -> str:
    return 'shopify'

  async def run(self) -> None:
    _data = await self.__get_data()
    json_file_path = os.path.join(self.working_directory, 'shopify_data.json')
    with open(json_file_path, 'w', encoding='utf-8') as f:
      json.dump(_data, f, ensure_ascii=False)

  async def load(self) -> list[Document]:
    await self.run()
    await asyncio.sleep(1)
    return await Loader(self.working_directory).load()

  async def __get_data(self, page_size: int = 50) -> List[dict]:
      # URL dell'API
    url = f"https://{self.__data.shop_name}.myshopify.com/admin/api/2024-07/graphql.json"

    # Headers
    headers = {
        "X-Shopify-Access-Token": self.__data.access_token,
        "Content-Type": "application/json"
    }

    all_data: List[dict] = []
    has_next_page = True
    cursor = None
    retry_count = 0
    max_retries = 5

    while has_next_page:
        # Variables per la query
        variables = {
            "first": page_size
        }

        if cursor:
            variables["after"] = cursor

        # Payload della richiesta
        payload = {
            "query": self.__data.graphql_query,
            "variables": variables
        }

        try:
            # Effettua la richiesta
            async with aiohttp.ClientSession() as session:
              async with session.post(url, headers=headers, json=payload) as response:
                # Controlla se la risposta è JSON
                try:
                  data = await response.json()
                except aiohttp.ContentTypeError:
                  text = await response.text()
                  logging.error(f"Non-JSON response received. Status code: {response.status}")
                  logging.error(f"Content: {text}")
                  raise Exception("Invalid response from API")

            # Gestione del throttling
            if "errors" in data:
                error = data["errors"][0]
                if error.get("extensions", {}).get("code") == "THROTTLED":
                    retry_count += 1
                    if retry_count > max_retries:
                        raise Exception("Too many throttling attempts. Stopping execution.")

                    # Aspetta un po' più a lungo ad ogni tentativo
                    wait_time = 2 ** retry_count  # Backoff esponenziale
                    print(f"Rate limit reached. Waiting {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"GraphQL errors: {data['errors']}")

            # Resetta il contatore dei retry se la richiesta è andata bene
            retry_count = 0

            # Estrae i dati
            _data = list(data["data"].values())[0]
            edges = _data["edges"]
            page_info = _data["pageInfo"]

            # Aggiungi i dati alla lista
            for edge in edges:
                all_data.append(edge["node"])

            # Aggiorna il cursore e il flag per la paginazione
            has_next_page = page_info["hasNextPage"]
            cursor = page_info["endCursor"]

            print(f"Recuperati {len(edges)} prodotti. Totale: {len(all_data)}")

            # Piccola pausa per evitare di saturare l'API
            await asyncio.sleep(0.1)

        except aiohttp.ClientError as e:
            logging.error(f"Connection error: {e}")
            retry_count += 1
            if retry_count <= max_retries:
                wait_time = 2 ** retry_count
                logging.warning(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                continue
            else:
                raise Exception("Too many network errors. Stopping execution.")

    logging.info(f"Data retrieval completed! Total data: {len(all_data)}")
    return all_data
