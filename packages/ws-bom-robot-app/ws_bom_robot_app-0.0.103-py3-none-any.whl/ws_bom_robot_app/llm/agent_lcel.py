from typing import Any, Optional
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import render_text_description
from pydantic import create_model, BaseModel
import chevron
from ws_bom_robot_app.llm.agent_context import AgentContext
from ws_bom_robot_app.llm.providers.llm_manager import LlmInterface
from ws_bom_robot_app.llm.models.api import LlmMessage, LlmRules
from ws_bom_robot_app.llm.utils.agent import get_rules
from ws_bom_robot_app.llm.defaut_prompt import default_prompt, tool_prompt

class AgentLcel:

    def __init__(self, llm: LlmInterface, sys_message: str, sys_context: AgentContext, tools: list, rules: LlmRules = None, json_schema: Optional[dict] = None):
        self.sys_message = chevron.render(template=sys_message,data=sys_context)
        self.__llm = llm
        self.__tools = tools
        self.rules = rules
        self.json_schema = json_schema
        self.embeddings = llm.get_embeddings()
        self.memory_key: str = "chat_history"
        self.__llm_with_tools = llm.get_llm().bind_tools(self.__tools) if len(self.__tools) > 0 else llm.get_llm()
        if self.json_schema:
            self.__pydantic_schema = self.__create_pydantic_schema()
        else:
            self.__pydantic_schema = None

        self.executor = self.__create_agent()

    def __create_pydantic_schema(self) -> type[BaseModel]:
        """Crea un Pydantic model dinamico dallo schema JSON."""
        if not self.json_schema:
            return None

        type_map = {
            "string": str,
            "text": str,
            "number": float,
            "float": float,
            "int": int,
            "integer": int,
            "bool": bool,
            "boolean": bool,
            "list": list,
            "array": list,
            "dict": dict,
            "object": dict,
        }

        fields: dict[str, tuple[Any, Any]] = {}
        for k, v in self.json_schema.items():
            if isinstance(v, str):
                py_type = type_map.get(v.lower(), str)
                fields[k] = (py_type, ...)
            elif isinstance(v, dict):
                fields[k] = (dict, ...)
            elif isinstance(v, list):
                fields[k] = (list, ...)
            else:
                fields[k] = (type(v), ...)

        return create_model('JsonSchema', **fields)

    def __get_output_parser(self):
        return self.__llm.get_parser()

    async def __create_prompt(self, input: dict) -> ChatPromptTemplate:
        from langchain_core.messages import SystemMessage
        message : LlmMessage = input[self.memory_key][-1]
        rules_prompt = await get_rules(self.embeddings, self.rules, message.content) if self.rules else ""
        system = default_prompt + (tool_prompt(render_text_description(self.__tools)) if len(self.__tools)>0 else "") + self.sys_message + rules_prompt

        # Aggiungi istruzioni per output JSON strutturato se necessario
        if self.json_schema and self.__pydantic_schema:
            json_instructions = f"\n\nIMPORTANT: You must format your final response as a JSON object with the following structure:\n"
            for field_name, field_info in self.__pydantic_schema.model_fields.items():
                field_type = field_info.annotation.__name__ if hasattr(field_info.annotation, '__name__') else str(field_info.annotation)
                json_instructions += f"- {field_name}: {field_type}\n"
            json_instructions += "\nProvide ONLY the JSON object in your response, no additional text."
            system += json_instructions

        messages = [
            SystemMessage(content=system),
            MessagesPlaceholder(variable_name=self.memory_key),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]

        prompt = ChatPromptTemplate.from_messages(
            messages=messages,
            template_format=None,
        )
        return prompt

    def __create_agent(self):
        # Un solo AgentExecutor per entrambe le modalità
        agent = (
            {
                "agent_scratchpad": lambda x: self.__llm.get_formatter(x["intermediate_steps"]),
                self.memory_key: lambda x: x[self.memory_key],
            }
            | RunnableLambda(self.__create_prompt)
            | self.__llm_with_tools
            | self.__get_output_parser()
        )
        return AgentExecutor(agent=agent, tools=self.__tools, verbose=False)
