import aiofiles
import json, os , uuid, httpx
from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.json_loader import JsonLoader
from ws_bom_robot_app.util import timer
import asyncio

class LlmKbIntegration(BaseModel):
  type: str = Field(..., validation_alias=AliasChoices("blockType","type"))
  model_config = ConfigDict(
      extra='allow',
      populate_by_name=True
  )
  def model_dump(self, **kwargs):
      """
      Custom model_dump method to ensure all properties are included
      Args:
          **kwargs: Additional arguments to pass to the default model_dump method
      Returns:
          dict: A dictionary representation of the model with all properties
      """
      # Use the default model_dump method with additional configuration
      return super().model_dump(
          by_alias=False,  # Use original field names
          exclude_unset=True,  # Include all fields, even unset ones
          include_extras=True,  # Include extra fields not defined in the model
          serialize_as_any=True,  # Serialize all fields as Any
          **kwargs
        )

class ExternalEndpointAuthentication(str, Enum):
    NONE = 'none'
    BASIC = 'basic'
    BEARER = 'bearer'
    CUSTOM = 'custom'

class LlmKbEndpointFieldsMapping(BaseModel):
    class ReplacedField(BaseModel):
        src_name: str = Field(validation_alias=AliasChoices("srcName","src_name"))
        dest_name: str = Field(validation_alias=AliasChoices("destName","dest_name"))
    class NamedField(BaseModel):
        name: str
    class NewField(NamedField):
        value: str
    class MetaField(NamedField):
        description: str
        type: Literal['string','int','float','bool','list[str]','list[int]','list[float]','list[bool]']
    replaced_fields: Optional[list[ReplacedField]] = Field(default_factory=list, validation_alias=AliasChoices("replacedFields","replaced_fields"))
    new_fields: Optional[list[NewField]] = Field(default_factory=list, validation_alias=AliasChoices("newFields","new_fields"))
    deleted_fields: Optional[list[NamedField]] = Field(default_factory=list, validation_alias=AliasChoices("deletedFields","deleted_fields"))
    meta_fields: Optional[list[MetaField]] = Field(default_factory=list, validation_alias=AliasChoices("metaFields","meta_fields"))
    """ select fields to be included in the metadata of the document
    Sample:
    [
      { "name": "price", description": "Product price", "type": "float" },
      { "name": "qty", "description": "Product availabilty: number of sellable items", "type": "int" }
    ]
    """

class LlmKbEndpoint(BaseModel):
    endpoint_url: str = Field(validation_alias=AliasChoices("endpointUrl","endpoint_url"))
    description: Optional[str] = None
    """ description of the document returned by the endpoint
    Usage: Provide additional information and prompting about the knowledge, providing context to the metadata fields detailed
    in the fields_mapping attribute
    Sample:
      List of sellable products, can filtered by price and availability.
      Price lower than 10 can be considered as discounted.
      Availability is the number of sellable items, 0 means out of stock, less than 10 means limited stock.
    """
    authentication: ExternalEndpointAuthentication
    auth_secret: Optional[str] = Field("",validation_alias=AliasChoices("authSecret","auth_secret"))
    fields_mapping: LlmKbEndpointFieldsMapping = Field(validation_alias=AliasChoices("fieldsMapping","fields_mapping"))

# Remapping Function
async def __remap_knowledgebase_file(filepath: str, mapping: LlmKbEndpointFieldsMapping) -> None:
    map_new_fields = mapping.new_fields or []
    map_replaced_fields = mapping.replaced_fields or []
    deleted_fields = mapping.deleted_fields or []

    if all([not map_new_fields,not map_replaced_fields,not deleted_fields]):
        return

    async with aiofiles.open(filepath, 'r', encoding='utf8') as file:
        original_data = json.load(file)

    for item in original_data:
        # Replaced fields
        for field in map_replaced_fields:
            if '.' in field.src_name:
                keys = field.src_name.split('.')
                last_key = keys.pop()
                obj = item
                for key in keys:
                    obj = obj.get(key, None)
                if obj is not None:
                    obj[field.dest_name] = obj.pop(last_key, None)
            else:
                item[field.dest_name] = item.pop(field.src_name, None)

        # Deleted fields
        for field in deleted_fields:
            if '.' in field.name:
                keys = field.name.split('.')
                last_key = keys.pop()
                obj = item
                for key in keys:
                    obj = obj.get(key, None)
                if obj is not None:
                    obj.pop(last_key, None)
            else:
                item.pop(field.name, None)

        # New fields
        for field in map_new_fields:
            item[field.name] = field.value
            async with aiofiles.open(filepath, 'w', encoding='utf8') as file:
              await file.write(json.dumps(original_data, ensure_ascii=False, indent=4))

    async with aiofiles.open(filepath, 'w', encoding='utf8') as file:
        json.dump(original_data, file, ensure_ascii=False, indent=4)

# Download External Endpoints
#@timer
async def load_endpoints(endpoints: list[LlmKbEndpoint], destination_directory: str) -> list[Document]:
  _documents = []

  async def process_endpoint(endpoint: LlmKbEndpoint):
    headers = {}
    if endpoint.authentication != ExternalEndpointAuthentication.NONE:
      auth_formats = {
        ExternalEndpointAuthentication.BASIC: lambda secret: f'Basic {secret}',
        ExternalEndpointAuthentication.BEARER: lambda secret: f'Bearer {secret}',
        ExternalEndpointAuthentication.CUSTOM: lambda secret: secret
      }
      headers['Authorization'] = auth_formats[endpoint.authentication](endpoint.auth_secret)
    try:
      async with httpx.AsyncClient(headers=headers,timeout=60) as client:
        response = await client.get(endpoint.endpoint_url)
        response.raise_for_status()

        mime_type = response.headers.get('content-type', None)
        if mime_type.__contains__('application/json'):
          filename = f"{uuid.uuid4()}.json"
          file_path = os.path.join(destination_directory, filename)
          async with aiofiles.open(file_path, 'wb') as file:
            await file.write(response.content)
          await __remap_knowledgebase_file(file_path, endpoint.fields_mapping)
          try:
            documents = await JsonLoader(
              file_path,
              meta_fields=[field.name for field in endpoint.fields_mapping.meta_fields] if endpoint.fields_mapping.meta_fields else []
            ).aload()
            _documents.extend(documents)
            await aiofiles.os.remove(file_path)
          except Exception as e:
            raise Exception(f"Failed to load documents from endpoint: {endpoint.endpoint_url} [{e}]") from e
        else:
          raise Exception(f"Unsupported content type {mime_type}")
    except httpx.HTTPStatusError as e:
      raise Exception(f"Failed to download file from endpoint [status {e.response.status_code}]: {endpoint.endpoint_url}") from e
    except httpx.RequestError as e:
      raise Exception(f"Failed to download file from endpoint: {endpoint.endpoint_url} [{e.request.content}]") from e
    except Exception as e:
      raise Exception(f"Failed to download file from endpoint: {endpoint.endpoint_url} [{e}]") from e

  await asyncio.gather(*[process_endpoint(endpoint) for endpoint in endpoints])

  return _documents

async def __remap_knowledgebase_file(filepath: str, mapping: LlmKbEndpointFieldsMapping) -> None:
  map_new_fields = mapping.new_fields or []
  map_replaced_fields = mapping.replaced_fields or []
  deleted_fields = mapping.deleted_fields or []

  if all([not map_new_fields, not map_replaced_fields, not deleted_fields]):
    return

  async with aiofiles.open(filepath, 'r', encoding='utf8') as file:
    original_data = json.loads(await file.read())

  for item in original_data:
    # Replaced fields
    for field in map_replaced_fields:
      if '.' in field.src_name:
        keys = field.src_name.split('.')
        last_key = keys.pop()
        obj = item
        for key in keys:
          obj = obj.get(key, None)
        if obj is not None:
          obj[field.dest_name] = obj.pop(last_key, None)
      else:
        item[field.dest_name] = item.pop(field.src_name, None)

    # Deleted fields
    for field in deleted_fields:
      if '.' in field.name:
        keys = field.name.split('.')
        last_key = keys.pop()
        obj = item
        for key in keys:
          obj = obj.get(key, None)
        if obj is not None:
          obj.pop(last_key, None)
      else:
        item.pop(field.name, None)

    # New fields
    for field in map_new_fields:
      item[field.name] = field.value

  async with aiofiles.open(filepath, 'w', encoding='utf8') as file:
    await file.write(json.dumps(original_data, ensure_ascii=False, indent=4))

