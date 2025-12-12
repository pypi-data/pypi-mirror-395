from typing import Union
from ws_bom_robot_app.llm.models.api import NebulyInteraction, NebulyLLMTrace, NebulyRetrievalTrace
from datetime import datetime, timezone
from langchain_core.callbacks.base import AsyncCallbackHandler
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk

class NebulyHandler(AsyncCallbackHandler):
    def __init__(self, llm_model: str | None, threadId: str = None, chat_history: list[BaseMessage] = [],  url: str = None, api_key: str = None, user_id: str | None = None):
        super().__init__()
        self.__started: bool = False
        self.__url: str = url
        self.__api_key: str = api_key
        self.chat_history = chat_history
        self.interaction = NebulyInteraction(
            conversation_id=threadId,
            input="",
            output="",
            time_start="",
            time_end="",
            end_user= user_id if user_id and user_id != "" else threadId,
            tags={"model": llm_model},
        )
        self.llm_trace = NebulyLLMTrace(
            model=llm_model,
            messages=[],
            output="",
            input_tokens=0,
            output_tokens=0,
        )
        self.__response_with_rag: str = "false" # Flag to check if the AI used some retrieval tools
        self.__retrieval_query: str = ""
        self.retrieval_traces: list[NebulyRetrievalTrace] = []

    async def on_chat_model_start(self, serialized, messages, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
        # Initialize the interaction with the input message
        if not self.__started:
          message_list = self.__flat_messages(messages)
          if isinstance(message_list[-1], HumanMessage):
            if isinstance(message_list[-1].content, list):
              self.interaction.input = self.__parse_multimodal_input(message_list[-1].content)
            else:
              self.interaction.input = message_list[-1].content
              self.interaction.tags["generated"] = self.__is_message_generated(message_list)
          else:
            raise ValueError("Last message is not a HumanMessage")
          self.interaction.time_start = datetime.now().astimezone().isoformat()
          self.__started = True

    async def on_llm_end(self, response, *, run_id, parent_run_id = None, tags = None, **kwargs):
        generation: Union[ChatGenerationChunk, GenerationChunk] = response.generations[0]
        usage_metadata: dict = generation[0].message.usage_metadata
        self.llm_trace.input_tokens = usage_metadata.get("input_tokens", 0)
        self.llm_trace.output_tokens = usage_metadata.get("output_tokens", 0)

    async def on_retriever_start(self, serialized, query, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
        self.__retrieval_query = query


    async def on_retriever_end(self, documents, *, run_id, parent_run_id = None, tags = None, **kwargs):
        # pass the document source because of the large amount of data in the document content
        for doc in documents:
          self.retrieval_traces.append(
            NebulyRetrievalTrace(
              source=doc.metadata.get("source", "content unavailable"),
              input=self.__retrieval_query,
              outputs=[doc.metadata.get("source", "content unavailable")]
            )
          )

    async def on_tool_start(self, serialized, input_str, *, run_id, parent_run_id = None, tags = None, metadata = None, inputs = None, **kwargs):
        self.__response_with_rag = "true"  # Set the flag to true when the retriever starts

    async def on_agent_finish(self, finish, *, run_id, parent_run_id = None, tags = None, **kwargs):
        # Interaction
        self.interaction.output = finish.return_values["output"]
        # Trace
        self.llm_trace.output = finish.return_values["output"]
        message_history =  self._convert_to_json_format(self.chat_history)
        self.llm_trace.messages = self.__parse_multimodal_history(message_history)
        await self.__send_interaction()

    def __flat_messages(self, messages: list[list[BaseMessage]], to_json: bool = False) -> list[BaseMessage]:
      """
      Maps the messages to the format expected by the LLM.
      Flattens the nested list structure of messages.
      """
      # Flatten the nested list structure
      flattened_messages = []
      for message_list in messages:
        flattened_messages.extend(message_list)
      # Store JSON format in LLM trace
      if to_json:
        return self._convert_to_json_format(flattened_messages)
      return flattened_messages

    def _convert_to_json_format(self, messages: list[BaseMessage]) -> list[dict]:
      """Converts BaseMessage objects to JSON format with role and content."""
      result = []
      for message in messages:
        if isinstance(message, HumanMessage):
          role = "user"
        elif isinstance(message, AIMessage):
          role = "assistant"
        else:
          role = "system"

        result.append({
          "role": role,
          "content": message.content
        })
      return result

    async def __send_interaction(self):
        # Send the interaction to the server
        from urllib.parse import urljoin
        import requests

        payload = self.__prepare_payload()
        endpoint = urljoin(self.__url, "event-ingestion/api/v2/events/trace_interaction")
        # Prepare headers with authentication
        headers = {"Content-Type": "application/json"}
        if self.__api_key:
          headers["Authorization"] = f"Bearer {self.__api_key}"
        response = requests.post(
          url=endpoint,
          json=payload,
          headers=headers
        )
        if response.status_code != 200:
          print(f"Failed to send interaction: {response.status_code} {response.text}")

    def __prepare_payload(self):
        self.interaction.time_end = datetime.now().astimezone().isoformat()
        self.interaction.tags["response_with_rag"] = self.__response_with_rag
        payload = {
            "interaction": self.interaction.__dict__,
            "traces": [
              self.llm_trace.__dict__,
            ]
        }
        for trace in self.retrieval_traces:
          if trace.source:
              payload["traces"].append(trace.__dict__)
        return payload

    def __parse_multimodal_input(self, input: list[dict]) -> str:
      """Parse multimodal input and return a string representation."""
      type_mapping = {
        "text": lambda item: item.get("text", ""),
        "image": lambda _: " <image>",
        "image_url": lambda _: " <image>",
        "file": lambda _: " <file>",
        "media": lambda _: " <file>",
        "document": lambda _: " <file>",
      }

      return "".join(
        type_mapping.get(item.get("type", ""), lambda item: f" <{item.get('type', '')}>")
        (item) for item in input
      )

    def __parse_multimodal_history(self, messages: list[dict]) -> list[dict]:
        # Parse the multimodal history and return a list of dictionaries
        parsed_history = []
        for message in messages:
            if isinstance(message["content"], list):
              parsed_content = self.__parse_multimodal_input(message["content"])
            else:
              parsed_content = message["content"]
            parsed_history.append({
          "role": message["role"],
          "content": parsed_content
            })
        return parsed_history

    def __is_message_generated(self, messages: list[BaseMessage]) -> bool:
        # Check if the last message is generated by the model
        if len(messages) == 0:
            return False
        last_user_message = f'<div class="llm__pill">{messages[-1].content}</div>'
        last_ai_message = messages[-2].content
        if last_user_message in last_ai_message:
            return "true"
        return "false"
