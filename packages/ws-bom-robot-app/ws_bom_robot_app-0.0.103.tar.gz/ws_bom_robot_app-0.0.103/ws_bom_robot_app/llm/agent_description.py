import json, requests, re
from typing import Any
from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableSerializable
from langchain_core.runnables import RunnableLambda
from bs4 import BeautifulSoup
from ws_bom_robot_app.llm.models.api import LlmRules
from ws_bom_robot_app.llm.providers.llm_manager import LlmInterface
from ws_bom_robot_app.llm.utils.agent import get_rules

# SafeDict helper class
class SafeDict(dict):
    def __missing__(self, key):
        return ''

# Strategy Interface
class AgentDescriptorStrategy(ABC):
    @abstractmethod
    def enrich_prompt(self, prompt: str, input: dict) -> str:
        pass

    @abstractmethod
    def rule_input(self, input: dict) -> str:
        pass

# Concrete Strategy for Default Agent
class DefaultAgentDescriptor(AgentDescriptorStrategy):
    def enrich_prompt(self, prompt: str, input: dict) -> str:
        # Default enrichment logic (could be minimal or no-op)
        return prompt.format_map(SafeDict(input))

    def rule_input(self, input: dict) -> str:
        return input.get('content', "")

# Concrete Strategy for URL2Text Agent
class URL2TextAgentDescriptor(AgentDescriptorStrategy):
    def enrich_prompt(self, prompt: str, input: dict) -> str:
        input["context"] = self._get_page_text(input)
        return prompt.format_map(SafeDict(input))

    def rule_input(self, input: dict) -> str:
        return input.get('context', "")

    def _get_page_text(self, input: dict) -> str:
        url = input.get("content", "")
        exclusions = input.get("exclude", {})
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html5lib')
        classes_to_exclude = exclusions.get("classes", [])
        ids_to_exclude = exclusions.get("ids", [])
        for class_name in classes_to_exclude:
            for element in soup.find_all(class_=class_name):
                element.extract()
        for id_name in ids_to_exclude:
            for element in soup.find_all(id=id_name):
                element.extract()
        for script in soup(["script", "noscript", "style", "head", "footer", "iframe"]):
            script.extract()
        return re.sub(' +', ' ', soup.get_text())


class AgentDescriptor:
    # Dictionary to hold all agent strategies
    _list: dict[str,AgentDescriptorStrategy] = {
        "default": DefaultAgentDescriptor(),
        "url2text": URL2TextAgentDescriptor(),
    }

    # Functions to manage strategies
    @staticmethod
    def add_strategy(name: str, strategy: AgentDescriptorStrategy):
        """_summary_
            add a new strategy to the dictionary
        Args:
            name (str): name of the strategy, in lowercase
            strategy (AgentDescriptorStrategy): class implementing the strategy
        Examples:
            AgentDescriptor.add_strategy("custom_agent_descriptor", CustomAgentDescriptor())
        """
        AgentDescriptor._list[name.lower()] = strategy

    @staticmethod
    def get_strategy(name: str) -> AgentDescriptorStrategy:
        return AgentDescriptor._list.get(name.lower(), DefaultAgentDescriptor())

    def __init__(self, llm: LlmInterface, prompt: str, mode: str, rules: LlmRules = None):
        self.__prompt = prompt
        self.__llm = llm
        self.rules= rules
        self.strategy = self.get_strategy(mode)  # Selects the strategy from the dictionary

    async def __create_prompt(self, input_dict: dict):
        input_data = json.loads(input_dict.get("input", {}))
        system = self.strategy.enrich_prompt(self.__prompt, input_data)
        if self.rules:
            rule_input = self.strategy.rule_input(input_data)
            rules_prompt = await get_rules(self.__llm.get_embeddings(), self.rules, rule_input)
            system += rules_prompt
        return ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("user", input_data.get("content", ""))
            ]
        )

    def __create_agent_descriptor(self, content) -> RunnableSerializable[Any, Any]:
        content = json.loads(content)
        agent = (
            {
                "input": lambda x: x["input"],
            }
            | RunnableLambda(self.__create_prompt)
            | self.__llm.get_llm()
        )
        return agent

    async def run_agent(self, content) -> Any:
        agent_descriptor = self.__create_agent_descriptor(content)
        response: AIMessage = await agent_descriptor.ainvoke({"input": content})
        return response
