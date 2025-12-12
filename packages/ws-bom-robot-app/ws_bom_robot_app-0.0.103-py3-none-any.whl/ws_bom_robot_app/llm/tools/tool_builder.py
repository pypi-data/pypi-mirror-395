import asyncio
from asyncio import Queue
from langchain.tools import StructuredTool
from ws_bom_robot_app.llm.models.api import LlmAppTool
from ws_bom_robot_app.llm.tools.tool_manager import ToolManager
from ws_bom_robot_app.llm.providers.llm_manager import LlmInterface

async def __process_proxy_tool(proxy_tool: LlmAppTool) -> LlmAppTool | None:
    import os
    from ws_bom_robot_app.llm.utils.cms import CmsApp, get_app_by_id
    from ws_bom_robot_app.config import config
    try:
        secrets = proxy_tool.secrets_to_dict()
        app_id = secrets.get("appId")
        if not app_id:
            raise ValueError("Tool configuration is invalid. 'appId' is required.")
        app: CmsApp = await get_app_by_id(app_id)
        if not app:
            raise ValueError(f"App with id {app_id} not found.")
        tool_id = secrets.get("toolId")
        tool = next((t for t in app.rq.app_tools if app.rq.app_tools and t.id == tool_id), None)
        if not tool:
            raise ValueError(f"Tool with function_id {tool_id} not found in app {app.name}.")
        #override derived tool with proxy tool props
        tool.name = proxy_tool.name if proxy_tool.name else tool.name
        tool.description = proxy_tool.description if proxy_tool.description else tool.description
        tool.function_id = proxy_tool.function_id if proxy_tool.function_id else tool.function_id
        tool.function_description = proxy_tool.function_description if proxy_tool.function_description else tool.function_description
        #normalize vector_db
        if tool.vector_db:
            tool.vector_db = os.path.join(
               os.path.join(config.robot_data_folder,config.robot_data_db_folder,config.robot_data_db_folder_store),
               os.path.splitext(os.path.basename(tool.vector_db))[0]) if tool.vector_db else None
        return tool
    except Exception as e:
        print(f"[!] Error in proxy_app_tool: {e}")
        return None

def get_structured_tools(llm: LlmInterface, tools: list[LlmAppTool], callbacks:list, queue: Queue) -> list[StructuredTool]:
  _structured_tools :list[StructuredTool] = []
  for tool in [tool for tool in tools if tool.is_active]:
    if tool.function_name == "proxy_app_tool":
        # override the tool
        loop = asyncio.get_event_loop()
        if loop.is_running():
          import nest_asyncio
          nest_asyncio.apply()
        processed_tool = loop.run_until_complete(__process_proxy_tool(tool))
        if processed_tool is None:
            continue
        tool = processed_tool
    if _tool_config := ToolManager._list.get(tool.function_name):
      _tool_instance = ToolManager(llm, tool, callbacks, queue)
      _structured_tool = StructuredTool.from_function(
        coroutine=_tool_instance.get_coroutine(),
        name=tool.function_id if tool.function_id else tool.function_name,
        description=tool.function_description,
        args_schema=_tool_config.model
        #infer_schema=True,
        #parse_docstring=True,
        #error_on_invalid_docstring=True
      )
      _structured_tool.tags = [tool.function_id if tool.function_id else tool.function_name]
      secrets = tool.secrets_to_dict()
      if secrets and secrets.get("stream") == "true":
        _structured_tool.tags.append("stream")
      _structured_tools.append(_structured_tool)
  return _structured_tools
