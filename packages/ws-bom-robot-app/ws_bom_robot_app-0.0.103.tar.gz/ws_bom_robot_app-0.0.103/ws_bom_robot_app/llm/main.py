from asyncio import Queue
import asyncio, json, logging, os, traceback, re
from fastapi import Request
from langchain.callbacks.tracers import LangChainTracer
from langchain_core.callbacks.base import AsyncCallbackHandler
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langsmith import Client as LangSmithClient
from typing import AsyncGenerator, List
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.agent_description import AgentDescriptor
from ws_bom_robot_app.llm.agent_handler import AgentHandler, RawAgentHandler
from ws_bom_robot_app.llm.agent_lcel import AgentLcel
from ws_bom_robot_app.llm.models.api import InvokeRequest, StreamRequest
from ws_bom_robot_app.llm.providers.llm_manager import LlmInterface
from ws_bom_robot_app.llm.tools.tool_builder import get_structured_tools
from ws_bom_robot_app.llm.nebuly_handler import NebulyHandler

async def invoke(rq: InvokeRequest) -> str:
  await rq.initialize()
  _msg: str = rq.messages[-1].content
  processor = AgentDescriptor(
      llm=rq.get_llm(),
      prompt=rq.system_message,
      mode = rq.mode,
      rules=rq.rules if rq.rules else None
  )
  result: AIMessage = await processor.run_agent(_msg)
  return {"result": result.content}

def _parse_formatted_message(message: str) -> str:
  try:
    text_fragments = []
    quoted_strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', message)
    for string in quoted_strings:
      if not string.startswith(('threadId', 'type')) and len(string) > 1:
          text_fragments.append(string)
    result = ''.join(text_fragments)
    result = result.replace('\\n', '\n')
  except:
    result = message
  return result

async def __stream(rq: StreamRequest, ctx: Request, queue: Queue, formatted: bool = True) -> None:
  #os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

  # rq initialization
  await rq.initialize()
  for tool in rq.app_tools:
    tool.thread_id = rq.thread_id

  #llm
  __llm: LlmInterface = rq.get_llm()

  #chat history
  chat_history: list[BaseMessage] = []
  for message in rq.messages:
    if message.role in ["human","user"]:
      _content = message.content
      # multimodal content parsing
      if isinstance(_content, list):
        try:
          _content = await __llm.format_multimodal_content(_content)
        except Exception as e:
          logging.warning(f"Error parsing multimodal content {_content[:100]}: {e}")
      chat_history.append(HumanMessage(content=_content))
    elif message.role in ["ai","assistant"]:
      message_content = ""
      if formatted:
        if '{\"type\":\"string\"' in message.content:
          try:
            json_msg = json.loads('[' + message.content[:-1] + ']')
            for msg in json_msg:
              if msg.get("content"):
                message_content += msg["content"]
          except:
            message_content = _parse_formatted_message(message.content)
        elif '{\"type\":\"text\"' in message.content:
          try:
            json_msg = json.loads('[' + message.content[:-1] + ']')
            for msg in json_msg:
              if msg.get("text"):
                message_content += msg["text"]
          except:
            message_content = _parse_formatted_message(message.content)
        else:
          message_content = _parse_formatted_message(message.content)
      else:
        message_content = message.content
      if message_content:
        chat_history.append(AIMessage(content=message_content))


  #agent handler
  if formatted:
    agent_handler = AgentHandler(queue, rq.provider, rq.thread_id)
  else:
    agent_handler = RawAgentHandler(queue, rq.provider)
  #TODO: move from os.environ to rq
  os.environ["AGENT_HANDLER_FORMATTED"] = str(formatted)

  #callbacks
  ## agent
  callbacks: List[AsyncCallbackHandler] = [agent_handler]
  ## langchain tracing
  if rq.lang_chain_tracing:
    client = LangSmithClient(
      api_key= rq.secrets.get("langChainApiKey", "")
    )
    trace = LangChainTracer(project_name=rq.lang_chain_project,client=client,tags=[str(ctx.base_url) if ctx else ''])
    callbacks.append(trace)
  ## nebuly tracing
  if rq.secrets.get("nebulyApiKey","") != "":
    user_id = rq.system_context.user.id if rq.system_context and rq.system_context.user and rq.system_context.user.id else None
    nebuly_callback = NebulyHandler(
        llm_model=__llm.config.model,
        threadId=rq.thread_id,
        chat_history=chat_history,
        url=config.NEBULY_API_URL,
        api_key=rq.secrets.get("nebulyApiKey", None),
        user_id=user_id
      )
    callbacks.append(nebuly_callback)

  # chain
  processor = AgentLcel(
      llm=__llm,
      sys_message=rq.system_message,
      sys_context=rq.system_context,
      tools=get_structured_tools(__llm, tools=rq.app_tools, callbacks=[callbacks], queue=queue),
      rules=rq.rules,
      json_schema=rq.output_structure.get("outputFormat") if rq.output_structure and rq.output_structure.get("outputType") == "json" else None
  )
  try:
    await processor.executor.ainvoke(
        {"chat_history": chat_history},
        {"callbacks": callbacks},
    )
  except Exception as e:
    _error = f"Agent invoke ex: {e}"
    logging.warning(_error)
    if config.runtime_options().debug:
      _error += f" | {traceback.format_exc()}"
      await queue.put(_error)
    await queue.put(None)

  # signal the end of streaming
  await queue.put(None)

async def stream(rq: StreamRequest, ctx: Request, formatted: bool = True) -> AsyncGenerator[str, None]:
    queue = Queue()
    task = asyncio.create_task(__stream(rq, ctx, queue, formatted))
    try:
        while True:
            token = await queue.get()
            if token is None:  # None indicates the end of streaming
                break
            yield token
    finally:
        await task
