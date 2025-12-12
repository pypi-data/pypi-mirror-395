import asyncio, logging, aiohttp
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import List, Union, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, AliasChoices, field_validator
import json
import os


class AuthConfig(BaseModel):
  """
  Configuration for API authentication.

  Attributes:
    type: Type of authentication (bearer, basic, api_key, custom, none)
    token: Bearer token or API key value
    username: Username for basic auth
    password: Password for basic auth
    header_name: Custom header name for API key
    prefix: Prefix for the auth value (e.g., 'Bearer', 'Token')
  """
  type: Literal["bearer", "basic", "api_key", "custom", "none"] = Field(default="none")
  token: Optional[str] = Field(default=None)
  username: Optional[str] = Field(default=None)
  password: Optional[str] = Field(default=None)
  header_name: Optional[str] = Field(default=None, validation_alias=AliasChoices("headerName", "header_name"))
  prefix: Optional[str] = Field(default=None)


class ApiParams(BaseModel):
  """
  Generic API Integration Parameters.

  Attributes:
    url: The base URL of the API endpoint
    method: HTTP method (GET, POST, PUT, DELETE, PATCH)
    headers: Custom headers to include in the request
    params: Query parameters for the request
    body: Request body for POST/PUT/PATCH requests
    auth: Authentication configuration
    response_data_path: JSON path to extract data from response (e.g., 'data.items', 'results')
    max_retries: Maximum number of retry attempts for failed requests
    retry_delay: Base delay in seconds between retries (uses exponential backoff)
    timeout: Request timeout in seconds
  """
  url: str = Field(validation_alias=AliasChoices("url", "endpoint"))
  method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = Field(default="GET")
  headers: Optional[Dict[str, str]] = Field(default_factory=dict)
  params: Optional[Dict[str, Any]] = Field(default_factory=dict)
  body: Optional[Union[Dict[str, Any], str]] = Field(default=None)
  auth: Optional[AuthConfig] = Field(default_factory=lambda: AuthConfig())
  response_data_path: Optional[str] = Field(default=None, validation_alias=AliasChoices("responseDataPath", "response_data_path"))
  max_retries: int = Field(default=5, validation_alias=AliasChoices("maxRetries", "max_retries"))
  retry_delay: float = Field(default=1.0, validation_alias=AliasChoices("retryDelay", "retry_delay"))
  timeout: int = Field(default=30)

  @field_validator('auth', mode='before')
  @classmethod
  def parse_auth(cls, v):
    """Parse auth config from dict if needed"""
    if isinstance(v, dict):
      return AuthConfig(**v)
    return v or AuthConfig()


class Api(IntegrationStrategy):
  """
  Generic API Integration that supports:
  - Multiple HTTP methods (GET, POST, PUT, DELETE, PATCH)
  - Various authentication types (Bearer, Basic, API Key, Custom)
  - Custom headers and parameters
  - Automatic retry with exponential backoff
  - Flexible response data extraction
  """

  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str, int, list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = ApiParams.model_validate(self.data)

  def working_subdirectory(self) -> str:
    return 'api_integration'

  async def run(self) -> None:
    """Fetch data from the API and save to JSON file"""
    _data = await self.__fetch_data()
    json_file_path = os.path.join(self.working_directory, 'api_data.json')
    with open(json_file_path, 'w', encoding='utf-8') as f:
      json.dump(_data, f, ensure_ascii=False, indent=2)
    logging.info(f"Saved {len(_data) if isinstance(_data, list) else 1} items to {json_file_path}")

  async def load(self) -> list[Document]:
    """Load data from API and convert to documents"""
    await self.run()
    await asyncio.sleep(1)
    return await Loader(self.working_directory).load()

  def __prepare_headers(self) -> Dict[str, str]:
    """Prepare request headers with authentication"""
    headers = self.__data.headers.copy() if self.__data.headers else {}

    # Add Content-Type if not present
    if 'Content-Type' not in headers and self.__data.method in ["POST", "PUT", "PATCH"]:
      headers['Content-Type'] = 'application/json'

    # Add authentication
    auth = self.__data.auth
    if auth.type == "bearer":
      prefix = auth.prefix or "Bearer"
      headers['Authorization'] = f"{prefix} {auth.token}"
    elif auth.type == "basic":
      import base64
      credentials = f"{auth.username}:{auth.password}"
      encoded = base64.b64encode(credentials.encode()).decode()
      headers['Authorization'] = f"Basic {encoded}"
    elif auth.type == "api_key" and auth.header_name:
      prefix = f"{auth.prefix} " if auth.prefix else ""
      headers[auth.header_name] = f"{prefix}{auth.token}"

    return headers

  def __get_nested_value(self, data: Any, path: Optional[str]) -> Any:
    """Extract nested value from data using dot notation path"""
    if not path:
      return data

    keys = path.split('.')
    current = data
    for key in keys:
      if isinstance(current, dict):
        current = current.get(key)
      elif isinstance(current, list) and key.isdigit():
        current = current[int(key)]
      else:
        return None

      if current is None:
        return None

    return current

  async def __make_request(
    self,
    url: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None
  ) -> Dict[str, Any]:
    """Make HTTP request with retry logic"""
    retry_count = 0

    while retry_count <= self.__data.max_retries:
      try:
        timeout = aiohttp.ClientTimeout(total=self.__data.timeout)

        async with aiohttp.ClientSession(timeout=timeout) as session:
          request_kwargs = {
            "headers": headers,
            "params": params or self.__data.params
          }

          # Add body for POST/PUT/PATCH
          if self.__data.method in ["POST", "PUT", "PATCH"] and self.__data.body:
            if isinstance(self.__data.body, dict):
              request_kwargs["json"] = self.__data.body
            else:
              request_kwargs["data"] = self.__data.body

          async with session.request(
            self.__data.method,
            url,
            **request_kwargs
          ) as response:
            # Check response status
            if response.status == 429:  # Rate limit
              retry_count += 1
              if retry_count > self.__data.max_retries:
                raise Exception("Rate limit exceeded. Maximum retries reached.")

              wait_time = self.__data.retry_delay * (2 ** retry_count)
              logging.warning(f"Rate limited. Waiting {wait_time}s (Attempt {retry_count}/{self.__data.max_retries})")
              await asyncio.sleep(wait_time)
              continue

            response.raise_for_status()

            # Parse response
            try:
              data = await response.json()
              return data
            except aiohttp.ContentTypeError:
              text = await response.text()
              logging.warning(f"Non-JSON response received: {text[:200]}")
              return {"text": text}

      except aiohttp.ClientError as e:
        retry_count += 1
        if retry_count > self.__data.max_retries:
          raise Exception(f"Request failed after {self.__data.max_retries} retries: {e}")

        wait_time = self.__data.retry_delay * (2 ** retry_count)
        logging.warning(f"Request error: {e}. Retrying in {wait_time}s...")
        await asyncio.sleep(wait_time)
        continue

    raise Exception("Maximum retries exceeded")

  async def __fetch_data(self) -> Any:
    """Fetch data from API"""
    headers = self.__prepare_headers()
    response = await self.__make_request(self.__data.url, headers)

    # Extract data from response using path if specified
    data = self.__get_nested_value(response, self.__data.response_data_path)
    result = data if data is not None else response

    return result
