from typing import List, Dict, Optional, Tuple, Union, Any
from datetime import datetime
from pydantic import AliasChoices, BaseModel, Field, ConfigDict
from langchain_core.embeddings import Embeddings
from langchain.chains.query_constructor.schema import AttributeInfo
from ws_bom_robot_app.llm.agent_context import AgentContext
from ws_bom_robot_app.llm.models.kb import LlmKbEndpoint, LlmKbIntegration
from ws_bom_robot_app.llm.providers.llm_manager import LlmManager, LlmConfig, LlmInterface
from ws_bom_robot_app.llm.utils.download import download_file
import os, shutil, uuid
from ws_bom_robot_app.config import Settings, config

class LlmMessage(BaseModel):
  """
  💬 multimodal chat

  The multimodal message allows users to interact with the application using both text and media files.
  `robot` accept multimodal input in a uniform way, regarding the llm provider used.

  - simple message

  ```json
  {
    "role": "user",
    "content": "What is the capital of France?"
  }
  ```

  - multimodal message

  ```jsonc
  {
    "role": "user",
    "content": [
      { "type": "text", "text": "Read carefully all the attachments, analize the content and provide a summary for each one:" },
      { "type": "image", "url": "https://www.example.com/image/foo.jpg" },
      { "type": "file", "url": "https://www.example.com/pdf/bar.pdf" },
      { "type": "file", "url": "data:plain/text;base64,CiAgICAgIF9fX19fCiAgICAgLyAgIC..." }, // base64 encoded file
      { "type": "media", "mime_type": "plain/text", "data": "CiAgICAgIF9fX19fCiAgICAgLyAgIC..." } // google/gemini specific input format
    ]
  }
  ```

  > 💡 `url` can be a remote url or a base64 representation of the file: [rfc 2397](https://datatracker.ietf.org/doc/html/rfc2397).
  Can also be used the llm/model specific input format.
  """
  role: str
  content: Union[str, list]

class LlmSearchSettings(BaseModel):
  search_type: Optional[str] = Field('default', validation_alias=AliasChoices("searchType","search_type"))
  score_threshold_id: Optional[float] = Field(None, validation_alias=AliasChoices("scoreThresholdId","score_threshold_id"))
  search_k: Optional[int] = Field(None, validation_alias=AliasChoices("searchK","search_k"))

class LlmRules(BaseModel):
  vector_type: Optional[str] = Field('faiss', validation_alias=AliasChoices("vectorDbType","vector_type"))
  vector_db: Optional[str] = Field(None, validation_alias=AliasChoices("rulesVectorDb","vector_db"))
  threshold: Optional[float] = 0.7

class LlmAppToolChainSettings(BaseModel):
  prompt: Optional[str] = None
  provider: Optional[str] = "openai"
  model: Optional[str] = None
  temperature: Optional[float] = 0
  outputStructure: Optional[dict] = None

class LlmAppToolDbSettings(BaseModel):
  connection_string: Optional[str] = Field(None, validation_alias=AliasChoices("connectionString","connection_string"))

class LlmAppTool(BaseModel):
  id: Optional[str] = None
  thread_id: Optional[str] = Field(None, validation_alias=AliasChoices("threadId","thread_id"))
  name: str
  description: Optional[str] = None
  type: str
  function_id: str = Field(..., validation_alias=AliasChoices("functionId","function_id"))
  function_name: str = Field(..., validation_alias=AliasChoices("functionName","function_name"))
  function_description: str = Field(..., validation_alias=AliasChoices("functionDescription","function_description"))
  secrets: Optional[List[Dict[str,str]]] = []
  llm_chain_settings: LlmAppToolChainSettings = Field(None, validation_alias=AliasChoices("llmChainSettings","llm_chain_settings"))
  data_source: str = Field(..., validation_alias=AliasChoices("dataSource","data_source"))
  db_settings: Optional[LlmAppToolDbSettings] = Field(None, validation_alias=AliasChoices("dbSettings","db_settings"))
  search_settings: LlmSearchSettings = Field(None, validation_alias=AliasChoices("searchSettings","search_settings"))
  integrations: Optional[List[LlmKbIntegration]] = None
  endpoints: Optional[List[LlmKbEndpoint]] = Field(None, validation_alias=AliasChoices("externalEndpoints","endpoints"))
  waiting_message: Optional[str] = Field("", validation_alias=AliasChoices("waitingMessage","waiting_message"))
  vector_type: Optional[str] = Field('faiss', validation_alias=AliasChoices("vectorDbType","vector_type"))
  vector_db: Optional[str] = Field(None, validation_alias=AliasChoices("vectorDbFile","vector_db"))
  is_active: Optional[bool] = Field(True, validation_alias=AliasChoices("isActive","is_active"))
  def secrets_to_dict(self) -> Dict[str, str]:
      _secrets = {}
      for d in self.secrets or []:
        _secrets[d.get("secretId")] = d.get("secretValue")
      return _secrets
  def get_vector_filtering(self) -> Optional[Tuple[str, List[AttributeInfo]]]:
      _description = None
      _metadata = None
      if (
        self.endpoints
        and len(self.endpoints) == 1
        and self.endpoints[0].fields_mapping.meta_fields
      ):
        _description = self.endpoints[0].description or self.description
        _metadata = [
          AttributeInfo(
            name=m.name,
            description=m.description or "",
            type=m.type
          )
          for m in self.endpoints[0].fields_mapping.meta_fields
        ]
      return _description, _metadata

  model_config = ConfigDict(
      extra='allow'
  )

class NebulyInteraction(BaseModel):
  conversation_id: str = Field(..., description="Unique identifier for grouping related interactions")
  input: str = Field(..., description="User input text in the interaction")
  output: str = Field(..., description="LLM response shown to the user")
  time_start: str = Field(..., description="ISO 8601 formatted start time of the LLM call")
  time_end: str = Field(..., description="ISO 8601 formatted end time of the LLM call")
  end_user: str = Field(..., description="Unique identifier for the end user (recommended: hashed username/email or thread_id)")
  tags: Optional[Dict[str, str]] = Field(default=None, description="Custom key-value pairs for tagging interactions")

class NebulyLLMTrace(BaseModel):
  model: str = Field(..., description="The name of the LLM model used for the interaction")
  messages: List[LlmMessage] = Field(..., description="List of messages exchanged during the interaction")
  output: str = Field(..., description="The final output generated by the LLM")
  input_tokens: Optional[int] = Field(..., description="Number of tokens in the input messages")
  output_tokens: Optional[int] = Field(..., description="Number of tokens in the output message")

class NebulyRetrievalTrace(BaseModel):
  source: Union[str, None] = Field(..., description="The source of the retrieved documents")
  input: str = Field(..., description="The input query used for retrieval")
  outputs: List[str] = Field(..., description="List of retrieved document contents")

#region llm public endpoints

#region api
class LlmApp(BaseModel):
  system_message: str = Field(..., validation_alias=AliasChoices("systemMessage","system_message"))
  system_context: Optional[AgentContext] = Field(AgentContext(), validation_alias=AliasChoices("systemContext","system_context"))
  messages: List[LlmMessage]
  provider: Optional[str] = "openai"
  model: Optional[str] = None
  temperature: Optional[float] = 0
  secrets: Dict[str, str]
  app_tools: Optional[List[LlmAppTool]] = Field([], validation_alias=AliasChoices("appTools","app_tools"))
  vector_type: Optional[str] = "faiss"
  vector_db: Optional[str] = Field(None, validation_alias=AliasChoices("vectorDb","vector_db"))
  rules: Optional[LlmRules] = None
  fine_tuned_model: Optional[str] = Field(None, validation_alias=AliasChoices("fineTunedModel","fine_tuned_model"))
  lang_chain_tracing: Optional[bool] = Field(False, validation_alias=AliasChoices("langChainTracing","lang_chain_tracing"))
  lang_chain_project: Optional[str] = Field(None, validation_alias=AliasChoices("langChainProject","lang_chain_project"))
  output_structure: Optional[Dict[str, Any]] = Field(None, validation_alias=AliasChoices("outputStructure","output_structure"))
  model_config = ConfigDict(
      extra='allow'
  )
  def __vector_db_folder(self) -> str:
    return os.path.join(config.robot_data_folder,config.robot_data_db_folder,config.robot_data_db_folder_store)
  def __vector_dbs(self):
      return list(set(
          os.path.basename(db) for db in [self.vector_db] +
          ([self.rules.vector_db] if self.rules and self.rules.vector_db else []) +
          [db for tool in (self.app_tools or []) for db in [tool.vector_db] if tool.is_active]
          if db is not None
      ))
  def __decompress_zip(self,zip_file_path, extract_to):
    shutil.unpack_archive(zip_file_path, extract_to, "zip")
    os.remove(zip_file_path)
  async def __extract_db(self) -> None:
    for db_file in self.__vector_dbs():
      db_folder = os.path.join(self.__vector_db_folder(), os.path.splitext(db_file)[0])
      if not os.path.exists(db_folder):
        db_destination_file = os.path.join(db_folder, db_file)
        result: Optional[str] = await download_file(f'{config.robot_cms_host}/{config.robot_cms_db_folder}/' + db_file,db_destination_file, authorization=config.robot_cms_auth)
        if result:
          self.__decompress_zip(db_destination_file, db_folder)
        else:
          os.removedirs(db_folder)
  def __normalize_vector_db_path(self) -> None:
    _vector_db_folder = self.__vector_db_folder()
    self.vector_db = os.path.join(_vector_db_folder, os.path.splitext(os.path.basename(self.vector_db))[0]) if self.vector_db else None
    if self.rules:
      self.rules.vector_db = os.path.join(_vector_db_folder, os.path.splitext(os.path.basename(self.rules.vector_db))[0]) if self.rules.vector_db else ""
    for tool in self.app_tools or []:
      tool.vector_db = os.path.join(_vector_db_folder, os.path.splitext(os.path.basename(tool.vector_db))[0]) if tool.vector_db else None
  def api_key(self):
    return self.secrets.get("apiKey", "")
  def get_llm(self) -> LlmInterface:
    return LlmManager._list[self.provider](LlmConfig(
      api_key=self.api_key(),
      embedding_api_key=self.secrets.get("embeddingApiKey", ""),
      model=self.model,
      temperature=self.temperature))
  async def initialize(self) -> None:
      await self.__extract_db()
      self.__normalize_vector_db_path()

class InvokeRequest(LlmApp):
  mode: str

class StreamRequest(LlmApp):
  thread_id: Optional[str] = Field(default=str(uuid.uuid4()), validation_alias=AliasChoices("threadId","thread_id"))
  msg_id: Optional[str] = Field(default=str(uuid.uuid4()), validation_alias=AliasChoices("msgId","msg_id"))
#endregion

#region vector_db
class VectorDbRequest(BaseModel):
  secrets: Optional[Dict[str, str]] = None
  provider: Optional[str] = "openai"
  model: Optional[str] = "gpt-4o"
  vector_type: Optional[str] = Field('faiss', validation_alias=AliasChoices("vectorDbType","vector_type"))
  vector_db: Optional[str] = None
  """
    if filled override the randomic out_name
  """
  def llm(self) -> LlmInterface:
    return LlmManager._list[self.provider](LlmConfig(model=self.model,api_key=self.api_key(),embedding_api_key=self.secrets.get("embeddingApiKey", ""),temperature=0))
  def embeddings(self) -> Embeddings:
    return self.llm().get_embeddings()
  def config(self) -> Settings:
    return config
  def api_key(self):
    return self.secrets.get("apiKey", "")
  def out_name(self):
    if self.vector_db:
      return ".".join(self.vector_db.split(".")[:-1]) if self.vector_db.endswith(".zip") else self.vector_db
    return f"db_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]}_{uuid.uuid1()}_{os.getpid()}_{self.vector_type}"

class RulesRequest(VectorDbRequest):
  type: Optional[str] = 'rules'
  rules: List[str]

class KbRequest(VectorDbRequest):
  files: Optional[List[str]] = []
  integrations: Optional[List[LlmKbIntegration]] = []
  endpoints: Optional[List[LlmKbEndpoint]] = []

class VectorDbResponse(BaseModel):
  success: bool = True
  vector_type: Optional[str] = None
  file: Optional[str] = None
  error: Optional[str] = None

#endregion

#endregion

