from asyncio import Queue
from langchain_core.agents import AgentFinish
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
from langchain.callbacks.base import AsyncCallbackHandler
from ws_bom_robot_app.llm.utils.print import print_json, print_string
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from langchain_core.callbacks.base import AsyncCallbackHandler
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
from langchain_core.messages import BaseMessage, AIMessage
import json, logging, re

# Here is a custom handler that will print the tokens to stdout.
# Instead of printing to stdout you can send the data elsewhere; e.g., to a streaming API response


def _parse_token(llm:str,token: str) -> str:
    """Parses the token based on the LLM provider."""
    if llm == "anthropic" and isinstance(token, list):
      first = token[0]
      if 'text' in first:
        token = first['text']
      else:
        #[{'id': 'toolu_01GGLwJcrQ8PvFMUkQPGu8n7', 'input': {}, 'name': 'document_retriever_xxx', 'type': 'tool_use', 'index': 1}]
        token = ""
    return token

class AgentHandler(AsyncCallbackHandler):

    def __init__(self, queue: Queue, llm:str, threadId: str = None) -> None:
        super().__init__()
        self._threadId = threadId
        self.queue = queue
        self.llm = llm
        self.__started: bool = False
        # on new token event
        self.stream_buffer = ""      # accumulates text that hasn't been processed yet
        self.in_json_block = False
        self.json_buffer = ""
        self.json_start_regex = re.compile(r'(`{1,3}\s*json\b)') # detect a potential json start fence.
        self.json_end_regex = re.compile(r'(`{1,3})')         # an end fence (one to three backticks).
        self.stream_cut_last_output_chunk_size = 16  # safe cut last chunk size to output if no markers are found
    async def on_chat_model_start(self, serialized, messages, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
        if not self.__started:
          self.__started = True
          firstChunk = {
              "type": "info",
              "threadId": self._threadId,
          }
          await self.queue.put(print_json(firstChunk))

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        if token and "llm_chain" not in (tags or []):
            token = _parse_token(self.llm,token)
            if token:
              self.stream_buffer += token  # append new data to pending buffer
              if not self.in_json_block:
                # search for the start of a json block.
                start_match = self.json_start_regex.search(self.stream_buffer)
                if start_match:
                    start_index = start_match.start()
                    # everything before the start marker is normal content.
                    if start_index > 0:
                        _before = self.stream_buffer[:start_index].replace('`','').strip() # remove eventual preceding backticks.
                        if _before:
                            await self.queue.put(print_string(_before))
                    # remove the start marker from pending.
                    self.stream_buffer = self.stream_buffer[start_match.end():]
                    # switch into json mode.
                    self.in_json_block = True
                    self.json_buffer = ""
                else:
                    # no json start marker found. It might be because the marker is split between chunks.
                    # to avoid losing potential marker fragments, output what we can safely process:
                    # if the pending text is long, we output most of it except the last few characters.
                    if len(self.stream_buffer) > self.stream_cut_last_output_chunk_size:
                        safe_cut = self.stream_buffer[:-3]
                        if safe_cut.startswith('`'):
                          safe_cut = safe_cut[1:]
                        await self.queue.put(print_string(safe_cut))
                        self.stream_buffer = self.stream_buffer[-3:]
              else:
                  # in json block: look for an end fence.
                  end_match = self.json_end_regex.search(self.stream_buffer)
                  if end_match:
                      end_index = end_match.start()
                      self.json_buffer += self.stream_buffer[:end_index]
                      try:
                          data = json.loads(self.json_buffer.replace('`',''))
                          await self.queue.put(print_json(data))
                      except json.JSONDecodeError as e:
                          logging.error(f"on_token: invalid json: {e} | {self.json_buffer}")
                      finally:
                          self.json_buffer = ""
                      # remove the end fence from pending.
                      self.stream_buffer = self.stream_buffer[end_match.end():].strip()
                      self.in_json_block = False
                  else:
                      # no end marker found
                      # accumulate everything and break to wait for more data.
                      self.json_buffer += self.stream_buffer
                      self.stream_buffer = ""

    async def on_tool_end(self, output, *, run_id, parent_run_id = None, tags = None, **kwargs):
        if "stream" in (tags or []):
            await self.queue.put(print_json(output))

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        **kwargs: Any,
    ) -> None:
        # end-of-stream: flush any remaining text
        if self.in_json_block:
            try:
                data = json.loads(self.json_buffer)
                await self.queue.put(print_json(data))
            except json.JSONDecodeError as e  :
                logging.error(f"on_agent_finish: invalid json: {e} | {self.json_buffer}")
                #await self.queue.put(print_string(self.json_buffer))
        elif self.stream_buffer:
            await self.queue.put(print_string(self.stream_buffer))

        finalChunk = {"type": "end"}
        await self.queue.put(print_json(finalChunk))
        await self.queue.put(None)


class RawAgentHandler(AsyncCallbackHandler):

    def __init__(self,queue: Queue, llm: str) -> None:
        super().__init__()
        self.queue = queue
        self.llm = llm

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Handles new tokens during streaming."""
        if token:  # only process non-empty tokens
            await self.queue.put(_parse_token(self.llm,token))

    async def on_tool_end(self, output, *, run_id, parent_run_id = None, tags = None, **kwargs):
        if "stream" in (tags or []):
            await self.queue.put(print_json(output))

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        **kwargs: Any,
    ) -> None:
        await self.queue.put(None)
