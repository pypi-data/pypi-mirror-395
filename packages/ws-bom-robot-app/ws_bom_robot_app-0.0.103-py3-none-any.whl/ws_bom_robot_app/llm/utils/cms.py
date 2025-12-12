import logging, aiohttp
from typing import Any, List, Optional
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from ws_bom_robot_app.llm.models.api import LlmAppTool, LlmRules, StreamRequest
from ws_bom_robot_app.llm.models.kb import LlmKbEndpoint, LlmKbIntegration
from ws_bom_robot_app.util import cache_with_ttl

class CmsAppCredential(BaseModel):
  app_key: str = Field(..., description="The app key for the credential", validation_alias=AliasChoices("appKey","app_key"))
  api_key: str = Field(..., description="The api key for the credential", validation_alias=AliasChoices("apiKey","api_key"))
  model_config = ConfigDict(extra='ignore')
class CmsApp(BaseModel):
  id: str = Field(..., description="Unique identifier for the app")
  name: str = Field(..., description="Name of the app")
  mode: str
  prompt_samples: Optional[List[str]]
  credentials: CmsAppCredential = None
  rq: StreamRequest
  kb: Optional[Any] = None
  model_config = ConfigDict(extra='ignore')

@cache_with_ttl(600)  # Cache for 10 minutes
async def get_apps() -> list[CmsApp]:
  import json
  from ws_bom_robot_app.config import config
  class DictObject(object):
      def __init__(self, dict_):
          self.__dict__.update(dict_)
      def __repr__(self):
          return json.dumps(self.__dict__)
      @classmethod
      def from_dict(cls, d):
          return json.loads(json.dumps(d), object_hook=DictObject)
  def __attr(obj, *attrs, default=None):
      for attr in attrs:
          obj = getattr(obj, attr, default)
          if obj is None:
              break
      return obj
  def __to_dict(obj):
      """Converts DictObject to dict recursively"""
      if isinstance(obj, DictObject):
          return {k: __to_dict(v) for k, v in obj.__dict__.items()}
      elif isinstance(obj, list):
          return [__to_dict(item) for item in obj]
      else:
          return obj
  host = config.robot_cms_host
  if host:
    url = f"{host}/api/llmApp?depth=1&pagination=false&locale=it"
    auth = config.robot_cms_auth
    headers = {"Authorization": auth} if auth else {}
    async with aiohttp.ClientSession() as session:
      async with session.get(url, headers=headers) as response:
        if response.status == 200:
          _apps=[]
          cms_apps = await response.json()
          for cms_app in cms_apps:
             if __attr(cms_app,"isActive",default=True) == True:
                _cms_app_dict = DictObject.from_dict(cms_app)
                try:
                  _app: CmsApp = CmsApp(
                    id=_cms_app_dict.id,
                    name=_cms_app_dict.name,
                    mode=_cms_app_dict.mode,
                    prompt_samples=[__attr(sample,'sampleInputText') or f"{sample.__dict__}" for sample in _cms_app_dict.contents.sampleInputTexts],
                    credentials=CmsAppCredential(app_key=_cms_app_dict.settings.credentials.appKey,api_key=_cms_app_dict.settings.credentials.apiKey),
                    rq=StreamRequest(
                      #thread_id=str(uuid.uuid1()),
                      messages=[],
                      secrets={
                        "apiKey": __attr(_cms_app_dict.settings,'llmConfig','secrets','apiKey', default=''),
                        "langChainApiKey": __attr(_cms_app_dict.settings,'llmConfig','secrets','langChainApiKey', default=''),
                        "nebulyApiKey": __attr(_cms_app_dict.settings,'llmConfig','secrets','nebulyApiKey', default=''),
                        },
                      system_message=__attr(_cms_app_dict.settings,'llmConfig','prompt','prompt','systemMessage') if __attr(_cms_app_dict.settings,'llmConfig','prompt','prompt','systemMessage') else __attr(_cms_app_dict.settings,'llmConfig','prompt','systemMessage'),
                      provider= __attr(_cms_app_dict.settings,'llmConfig','provider') or 'openai',
                      model= __attr(_cms_app_dict.settings,'llmConfig','model') or 'gpt-4o',
                      temperature=_cms_app_dict.settings.llmConfig.temperature or 0,
                      app_tools=[LlmAppTool(**tool) for tool in cms_app.get('settings').get('appTools',[])],
                      rules=LlmRules(
                        vector_type=__attr(_cms_app_dict.settings,'rules','vectorDbType', default='faiss'),
                        vector_db=__attr(_cms_app_dict.settings,'rules','vectorDbFile','filename'),
                        threshold=__attr(_cms_app_dict.settings,'rules','threshold', default=0.7)
                        ) if __attr(_cms_app_dict.settings,'rules','vectorDbFile','filename') else None,
                      #fine_tuned_model=__attr(_cms_app_dict.settings,'llmConfig','fineTunedModel'),
                      lang_chain_tracing= __attr(_cms_app_dict.settings,'llmConfig','langChainTracing', default=False),
                      lang_chain_project= __attr(_cms_app_dict.settings,'llmConfig','langChainProject', default=''),
                      output_structure= __to_dict(__attr(_cms_app_dict.settings,'llmConfig','outputStructure')) if __attr(_cms_app_dict.settings,'llmConfig','outputStructure') else None
                    ))
                except Exception as e:
                  import traceback
                  ex = traceback.format_exc()
                  logging.error(f"Error creating CmsApp {_cms_app_dict.name} from dict: {e}\n{ex}")
                  continue
                if _app.rq.app_tools:
                  for tool in _app.rq.app_tools:
                    _knowledgeBase = tool.knowledgeBase
                    tool.integrations = [LlmKbIntegration(**item) for item in _knowledgeBase.get('integrations')] if _knowledgeBase.get('integrations') else []
                    try:
                      tool.endpoints = [LlmKbEndpoint(**item) for item in _knowledgeBase.get('externalEndpoints')] if _knowledgeBase.get('externalEndpoints') else []
                    except Exception as e:
                      logging.error(f"Error parsing endpoints for app {_cms_app_dict.name} tool {tool.name}: {e}")
                    tool.vector_db = _knowledgeBase.get('vectorDbFile').get('filename') if _knowledgeBase.get('vectorDbFile') else None
                    tool.vector_type = _knowledgeBase.get('vectorDbType') if _knowledgeBase.get('vectorDbType') else 'faiss'
                    del tool.knowledgeBase
                _apps.append(_app)
          return _apps
        else:
          logging.error(f"Error fetching cms apps: {response.status}")
  else:
    logging.error("robot_cms_host environment variable is not set.")
  return []


async def get_app_by_id(app_id: str) -> CmsApp | None:
    apps = await get_apps()
    app = next((a for a in apps if a.id == app_id), None)
    if app:
        return app
    else:
        logging.error(f"App with id {app_id} not found.")
        return None
