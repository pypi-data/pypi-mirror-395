from typing import Optional
from urllib.parse import urlparse
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, ConfigDict, Field
import os
from ws_bom_robot_app.llm.utils.download import Base64File

class LlmConfig(BaseModel):
    api_url: Optional[str] = None
    api_key: str
    embedding_api_key: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0)

# abstract LLM interface with default implementations
class LlmInterface:
    def __init__(self, config: LlmConfig):
        self.config = config

    def get_llm(self) -> BaseChatModel:
        raise NotImplementedError

    def get_embeddings(self) -> Embeddings:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            api_key=self.config.embedding_api_key or os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small")

    def get_models(self) -> list:
        raise NotImplementedError

    def get_formatter(self,intermadiate_steps):
        from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
        return format_to_openai_tool_messages(intermediate_steps=intermadiate_steps)

    def get_parser(self):
        from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
        return OpenAIToolsAgentOutputParser()
    async def _format_multimodal_image_message(self, message: dict) -> dict:
        return {
            "type": "image_url",
            "image_url": {
                "url": message.get("url")
            }
        }
    async def _format_multimodal_file_message(self, message: dict, file: Base64File = None) -> dict:
        _file = file or await Base64File.from_url(message.get("url"))
        return {"type": "text", "text": f"Here's a file attachment named `{_file.name}` of type `{_file.mime_type}` in base64: `{_file.base64_content}`"}
    async def format_multimodal_content(self, content: list) -> list:
        _content = []
        for message in content:
            if isinstance(message, dict):
                if message.get("type") == "image" and "url" in message:
                    _content.append(await self._format_multimodal_image_message(message))
                elif message.get("type") == "file" and "url" in message:
                    _content.append(await self._format_multimodal_file_message(message))
                else:
                    # pass through text or other formats unchanged
                    _content.append(message)
            else:
                _content.append(message)
        return _content

class Anthropic(LlmInterface):
    def get_llm(self):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            api_key=self.config.api_key or os.getenv("ANTHROPIC_API_KEY"),
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=8192,
            streaming=True,
            #betas=["files-api-2025-04-14"] #https://docs.anthropic.com/en/docs/build-with-claude/files
        )

    """
    def get_embeddings(self):
        from langchain_voyageai import VoyageAIEmbeddings
        return VoyageAIEmbeddings(
            api_key=self.config.embedding_api_key, #voyage api key
            model="voyage-3")
    """

    def get_models(self):
        import anthropic
        client = anthropic.Client(api_key=self.config.api_key or os.getenv("ANTHROPIC_API_KEY"))
        response = client.models.list()
        return response.data

    """
    async def _format_multimodal_image_message(self, message: dict) -> dict:
        file = await Base64File.from_url(message.get("url"))
        return { "type": "image_url", "image_url": { "url": file.base64_url }}
    """

    #https://python.langchain.com/docs/integrations/chat/anthropic/
    #https://python.langchain.com/docs/how_to/multimodal_inputs/
    async def _format_multimodal_file_message(self, message: dict, file: Base64File = None) -> dict:
        _url = str(message.get("url", ""))
        _url_lower = _url.lower()
        if _url_lower.startswith("http") and any(urlparse(_url_lower).path.endswith(ext) for ext in [".pdf"]):
            return {"type": "file", "source_type": "url", "url": _url}
        else:
          _file = file or await Base64File.from_url(_url)
          if _file.extension in ["pdf"]:
            return {"type": "document", "source": {"type": "base64", "media_type": _file.mime_type, "data": _file.base64_content}}
          else:
            return await super()._format_multimodal_file_message(message, _file)

class OpenAI(LlmInterface):
    def __init__(self, config: LlmConfig):
        super().__init__(config)
        self.config.embedding_api_key = self.config.api_key

    def get_llm(self):
        from langchain_openai import ChatOpenAI
        chat = ChatOpenAI(
            api_key=self.config.api_key or os.getenv("OPENAI_API_KEY"),
            model=self.config.model,
            streaming=True
        )
        if not (any(self.config.model.startswith(prefix) for prefix in ["gpt-5", "o1", "o3"]) or "search" in self.config.model):
            chat.temperature = self.config.temperature
            chat.streaming = True
        return chat

    def get_models(self):
        import openai
        openai.api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        response = openai.models.list()
        return response.data

    async def _format_multimodal_file_message(self, message: dict, file: Base64File = None) -> dict:
        _file = file or await Base64File.from_url(message.get("url"))
        if _file.extension in ["pdf"]:
            return {"type": "file", "file": { "source_type": "base64", "file_data": _file.base64_url, "mime_type": _file.mime_type, "filename": _file.name}}
        else:
          return await super()._format_multimodal_file_message(message, _file)

class DeepSeek(LlmInterface):
    def get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=self.config.api_key or os.getenv("DEEPSEEK_API_KEY"),
            model=self.config.model,
            base_url="https://api.deepseek.com",
            max_tokens=8192,
            temperature=self.config.temperature,
            streaming=True
        )

    def get_models(self):
        import openai
        openai.api_key = self.config.api_key or os.getenv("DEEPSEEK_API_KEY")
        openai.base_url = "https://api.deepseek.com"
        response = openai.models.list()
        return response.data

    async def _format_multimodal_image_message(self, message: dict) -> dict:
        print(f"{DeepSeek.__name__} does not support image messages")
        return None

    async def _format_multimodal_file_message(self, message: dict, file: Base64File = None) -> dict:
        print(f"{DeepSeek.__name__} does not support file messages")
        return None

class Google(LlmInterface):
    def get_llm(self):
      from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
      return ChatGoogleGenerativeAI(
        model=self.config.model,
        google_api_key=self.config.api_key or os.getenv("GOOGLE_API_KEY"),
        temperature=self.config.temperature,
        disable_streaming=False,
      )

    def get_embeddings(self):
      from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
      return GoogleGenerativeAIEmbeddings(
        google_api_key=self.config.api_key or os.getenv("GOOGLE_API_KEY"),
        model="models/gemini-embedding-001")

    def get_models(self):
      import google.generativeai as genai
      genai.configure(api_key=self.config.api_key or os.getenv("GOOGLE_API_KEY"))
      response = genai.list_models()
      return [{
        "id": model.name,
        "name": model.display_name,
        "description": model.description,
        "input_token_limit": model.input_token_limit,
        "output_token_limit": model.output_token_limit
      } for model in response if "gemini" in model.name.lower()]

    async def _format_multimodal_file_message(self, message: dict, file: Base64File = None) -> dict:
        _file = file or await Base64File.from_url(message.get("url"))
        if _file.extension in ["pdf", "csv"]:
            return {"type": "media", "mime_type": _file.mime_type, "data": _file.base64_content }
        else:
          return await super()._format_multimodal_file_message(message, _file)

class GoogleVertex(LlmInterface):
    def get_llm(self):
        from langchain_google_vertexai  import ChatVertexAI
        return ChatVertexAI(
            model=self.config.model,
            temperature=self.config.temperature
        )
    def get_embeddings(self):
        from langchain_google_vertexai.embeddings import VertexAIEmbeddings
        embeddings = VertexAIEmbeddings(model_name="gemini-embedding-001")
        return embeddings
    def get_models(self):
        _models = [
                {"id":"gemini-2.5-pro"},
                {"id":"gemini-2.5-flash"},
                {"id":"gemini-2.0-flash"},
                {"id":"gemini-2.0-flash-lite"}
              ]
        try:
          from google.cloud import aiplatform
          aiplatform.init()
          _list = aiplatform.Model.list()
          if _list:
            _models = list([{"id": model.name} for model in _list])
        # removed due issue: https://github.com/langchain-ai/langchain-google/issues/733
        # Message type "google.cloud.aiplatform.v1beta1.GenerateContentResponse" has no field named "createTime" at "GenerateContentResponse".  Available Fields(except extensions): "['candidates', 'modelVersion', 'promptFeedback', 'usageMetadata']"
        except Exception as e:
          print(f"Error fetching models from Gvertex: {e}")
          # fallback to hardcoded models
          #see https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#united-states for available models
        finally:
          return _models

    async def _format_multimodal_file_message(self, message: dict, file: Base64File = None) -> dict:
        _file = file or await Base64File.from_url(message.get("url"))
        if _file.extension in ["pdf", "csv"]:
            return {"type": "media", "mime_type": _file.mime_type, "data": _file.base64_content }
        else:
          return await super()._format_multimodal_file_message(message, _file)

class Groq(LlmInterface):
    def get_llm(self):
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=self.config.api_key or os.getenv("GROQ_API_KEY"),
            model=self.config.model,
            #max_tokens=8192,
            temperature=self.config.temperature,
            streaming=True,
        )

    def get_models(self):
        import requests
        url = "https://api.groq.com/openai/v1/models"
        headers = {
            "Authorization": f"Bearer {self.config.api_key or os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json().get("data", [])

class IBM(LlmInterface):
    def __init__(self, config: LlmConfig):
        from ibm_watsonx_ai import APIClient,Credentials
        super().__init__(config)
        self.__base_url = self.config.api_url or os.getenv("WATSONX_URL") or "https://us-south.ml.cloud.ibm.com"
        self.__api_key = self.config.api_key or os.getenv("WATSONX_APIKEY")
        self.__client = APIClient(
            credentials=Credentials(url=self.__base_url,api_key=self.__api_key),
            project_id=os.getenv("WATSONX_PROJECTID") or "default"
        )
    def get_llm(self):
        from langchain_ibm import ChatWatsonx
        return ChatWatsonx(
            model_id=self.config.model,
            watsonx_client=self.__client
        )
    def get_models(self):
        import requests
        from datetime import date
        try:
          # https://cloud.ibm.com/apidocs/watsonx-ai#list-foundation-model-specs
          today = date.today().strftime("%Y-%m-%d")
          url = f"{self.__base_url}/ml/v1/foundation_model_specs?version={today}&filters=task_generation,task_summarization:and"
          headers = {
              "Authorization": f"Bearer {self.__api_key}",
              "Content-Type": "application/json"
          }
          response = requests.get(url, headers=headers)
          models = response.json().get("resources", [])
          return [{
                "id": model['model_id'],
                "provider": model['provider'],
                "tasks": model['task_ids'],
                "limits": model.get('model_limits', {}),
              } for model in models]
        except Exception as e:
          print(f"Error fetching models from IBM WatsonX: {e}")
          # https://www.ibm.com/products/watsonx-ai/foundation-models
          return [
            {"id":"ibm/granite-13b-instruct-v2"},
            {"id":"ibm/granite-3-2b-instruct"},
            {"id":"ibm/granite-3-8b-instruct"},
            {"id":"meta-llama/llama-2-13b-chat"},
            {"id":"meta-llama/llama-3-3-70b-instruct"},
            {"id":"meta-llama/llama-4-maverick-17b-128e-instruct-fp8"},
            {"id":"mistralai/mistral-large"},
            {"id":"mistralai/mixtral-8x7b-instruct-v01"},
            {"id":"mistralai/pixtral-12b"}
          ]

    def get_embeddings(self):
        from langchain_ibm import WatsonxEmbeddings
        from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
        # https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models-embed.html?context=wx&audience=wdp#embed
        embed_params = {
            EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 512,
            #EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
        }
        return WatsonxEmbeddings(
            model_id="ibm/granite-embedding-107m-multilingual", #https://www.ibm.com/products/watsonx-ai/foundation-models
            watsonx_client=self.__client,
            params=embed_params
        )

class Ollama(LlmInterface):
    def __init__(self, config: LlmConfig):
        super().__init__(config)
        self.__base_url = self.config.api_url or os.getenv("OLLAMA_API_URL") or "http://localhost:11434"
    def get_llm(self):
        from langchain_ollama.chat_models import ChatOllama
        return ChatOllama(
            model=self.config.model,
            base_url=self.__base_url,
            temperature=self.config.temperature,
            streaming=True,
        )
    def get_embeddings(self):
        from langchain_ollama.embeddings import OllamaEmbeddings
        return OllamaEmbeddings(
            base_url=self.__base_url,
            model="mxbai-embed-large" #nomic-embed-text
        )
    def get_models(self):
        import requests
        url = f"{self.__base_url}/api/tags"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        models = response.json().get("models", [])
        return [{
              "id": model['model'],
              "modified_at": model['modified_at'],
              "size": model['size'],
              "details": model['details']
            } for model in models]

    async def _format_multimodal_image_message(self, message: dict) -> dict:
        file = await Base64File.from_url(message.get("url"))
        return { "type": "image_url", "image_url": { "url": file.base64_url }}

class LlmManager:
    """
    Expose the available LLM providers.
    Names are aligned with the LangChain documentation:
    https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html
    """

    #class variables (static)
    _list: dict[str,LlmInterface] = {
        "anthropic": Anthropic,
        "deepseek": DeepSeek,
        "google": Google, #deprecated
        "google_genai": Google,
        "gvertex": GoogleVertex,#deprecated
        "google_vertexai": GoogleVertex,
        "groq": Groq,
        "ibm": IBM,
        "openai": OpenAI,
        "ollama": Ollama
    }
