from asyncio import Queue
import aiohttp, re
from typing import  Optional, Type, Callable
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.models.api import LlmApp,LlmAppTool
from ws_bom_robot_app.llm.providers.llm_manager import LlmInterface
from ws_bom_robot_app.llm.utils.cms import CmsApp, get_app_by_id
from ws_bom_robot_app.llm.vector_store.db.manager import VectorDbManager
from ws_bom_robot_app.llm.tools.utils import getRandomWaitingMessage, translate_text
from ws_bom_robot_app.llm.tools.models.main import NoopInput,DocumentRetrieverInput,ImageGeneratorInput,LlmChainInput,SearchOnlineInput,EmailSenderInput
from pydantic import BaseModel, ConfigDict

class ToolConfig(BaseModel):
    function: Callable
    model: Optional[Type[BaseModel]] = NoopInput
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class ToolManager:
    """
    ToolManager is responsible for managing various tools used in the application.

    Attributes:
        app_tool (LlmAppTool): The application tool configuration.
        api_key (str): The API key for accessing external services.
        callbacks (list): A list of callback functions to be executed.

    Methods:
        document_retriever(query: str): Asynchronously retrieves documents based on the query.
        image_generator(query: str, language: str = "it"): Asynchronously generates an image based on the query.
        get_coroutine(): Retrieves the coroutine function based on the tool configuration.
    """

    def __init__(
        self,
        llm: LlmInterface,
        app_tool: LlmAppTool,
        callbacks: list,
        queue: Optional[Queue] = None
    ):
        self.llm = llm
        self.app_tool = app_tool
        self.callbacks = callbacks
        self.queue = queue

    async def __extract_documents(self, query: str, app_tool: LlmAppTool):
        search_type = "similarity"
        search_kwargs = {"k": 4}
        if app_tool.search_settings:
            search_settings = app_tool.search_settings # type: ignore
            if search_settings.search_type == "similarityScoreThreshold":
                search_type = "similarity_score_threshold"
                search_kwargs = {
                    "score_threshold": search_settings.score_threshold_id if search_settings.score_threshold_id else  0.5,
                    "k": search_settings.search_k if search_settings.search_k else 100
                }
            elif search_settings.search_type == "mmr":
                search_type = "mmr"
                search_kwargs = {"k": search_settings.search_k if search_settings.search_k else 4}
            elif search_settings.search_type == "default":
                search_type = "similarity"
                search_kwargs = {"k": search_settings.search_k if search_settings.search_k else 4}
            else:
                search_type = "mixed"
                search_kwargs = {"k": search_settings.search_k if search_settings.search_k else 4}
        if self.queue:
          await self.queue.put(getRandomWaitingMessage(app_tool.waiting_message, traduction=False))

        return await VectorDbManager.get_strategy(app_tool.vector_type).invoke(
            self.llm.get_embeddings(),
            app_tool.vector_db,
            query,
            search_type,
            search_kwargs,
            app_tool=app_tool,
            llm=self.llm.get_llm(),
            source=app_tool.function_id,
            )

    #region functions
    async def document_retriever(self, query: str) -> list:
        """
        Asynchronously retrieves documents based on the provided query using the specified search settings.

        Args:
          query (str): The search query string.

        Returns:
          list: A list of retrieved documents based on the search criteria.

        Raises:
          ValueError: If the configuration for the tool is invalid or the vector database is not found.

        Notes:
          - The function supports different search types such as "similarity", "similarity_score_threshold", "mmr", and "mixed".
          - The search settings can be customized through the `app_tool.search_settings` attribute.
          - If a queue is provided, a waiting message is put into the queue before invoking the search.
        """
        if (
            self.app_tool.type == "function" and self.app_tool.vector_db
            #and self.settings.get("dataSource") == "knowledgebase"
        ):
            return await self.__extract_documents(query, self.app_tool)

    async def image_generator(self, query: str, language: str = "it"):
        """
        Asynchronously generates an image based on the query.
        set OPENAI_API_KEY in your environment variables
        """
        from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
        model = self.app_tool.model or "dall-e-3"
        random_waiting_message = getRandomWaitingMessage(self.app_tool.waiting_message, traduction=False)
        if not language:
            language = "it"
        await translate_text(
            self.llm, language, random_waiting_message, self.callbacks
        )
        try:
            #set os.environ.get("OPENAI_API_KEY")!
            image_url = DallEAPIWrapper(model=model).run(query)  # type: ignore
            return image_url
        except Exception as e:
            return f"Error: {str(e)}"

    async def llm_chain(self, input: str):
        if self.app_tool.type == "llmChain":
          from langchain_core.prompts import ChatPromptTemplate
          from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
          from pydantic import create_model
          system_message = self.app_tool.llm_chain_settings.prompt.format(
             thread_id = self.app_tool.thread_id if self.app_tool.thread_id else "no-thread-id",
          )
          context = []
          if self.app_tool.data_source == "knowledgebase":
            context = await self.__extract_documents(input, self.app_tool)
          if len(context) > 0:
            for doc in context:
              system_message += f"\n\nContext:\n{doc.metadata.get("source", "")}: {doc.page_content}"
          # Determine output parser and format based on output type
          output_type = self.app_tool.llm_chain_settings.outputStructure.get("outputType")
          is_json_output = output_type == "json"

          if is_json_output:
            output_format = self.app_tool.llm_chain_settings.outputStructure.get("outputFormat", {})
            json_schema = create_model('json_schema', **{k: (type(v), ...) for k, v in output_format.items()})
            output_parser = JsonOutputParser(pydantic_object=json_schema)
            system_message += "\n\nFormat instructions:\n{format_instructions}".strip()
          else:
            output_parser = StrOutputParser()
          # Create prompt template with or without format instructions
          base_messages = [
            ("system", system_message),
            ("user", "{input}")
          ]
          if is_json_output:
            prompt = ChatPromptTemplate.from_messages(base_messages).partial(
              format_instructions=output_parser.get_format_instructions()
            )
          else:
            prompt = ChatPromptTemplate.from_messages(base_messages)
          model = self.app_tool.llm_chain_settings.model
          self.llm.config.model = model
          llm = self.llm.get_llm()
          llm.tags = ["llm_chain"]
          chain = prompt | llm | output_parser
          result = await chain.ainvoke({"input": input})
          return result

    async def proxy_app_chat(self, query: str) -> str | None:
        from ws_bom_robot_app.llm.models.api import LlmMessage
        secrets = self.app_tool.secrets_to_dict()
        app_id = secrets.get("appId")
        if not app_id:
            raise ValueError("Tool configuration is invalid. 'appId' is required.")
        app: CmsApp = await get_app_by_id(app_id)
        if not app:
            raise ValueError(f"App with id {app_id} not found.")
        # message
        app.rq.messages.append(LlmMessage(role="user", content=query))
        # tracing
        if str(secrets.get("disable_tracing", False)).lower() in ['1','true','yes']:
          app.rq.lang_chain_tracing = False
          app.rq.lang_chain_project = ''
          app.rq.secrets['nebulyApiKey'] = ''
        # http: for debugging purposes
        if str(secrets.get("use_http", False)).lower() in ['1','true','yes']:
          import base64
          url = f"http://localhost:{config.runtime_options().tcp_port}/api/llm/stream/raw"
          auth = f"Basic {base64.b64encode((config.robot_user + ':' + config.robot_password).encode('utf-8')).decode('utf-8')}"
          headers = {"Authorization": auth} if auth else {}
          async with aiohttp.ClientSession() as session:
              _data = app.rq.model_dump(mode='json',by_alias=True,exclude_unset=True,exclude_none=True, exclude_defaults=True)
              async with session.post(url, json=_data, headers=headers) as response:
                  if response.status == 200:
                    return await response.text()
                  else:
                    raise ValueError(f"Error fetching chat response: {response.status}")
          return None
        else:  # default
          try:
            from ws_bom_robot_app.llm.main import stream
            import json
            chunks = []
            async for chunk in stream(rq=app.rq, ctx=None, formatted=False):
                chunks.append(chunk)
            rs = ''.join(chunks) if chunks else None

            # if the app has output_structure, parse the JSON and return dict
            if rs and app.rq.output_structure:
                try:
                    cleaned_rs = re.sub(r'^```(?:json)?\s*\n?', '', rs.strip())
                    cleaned_rs = re.sub(r'\n?```\s*$', '', cleaned_rs)
                    return json.loads(cleaned_rs)
                except json.JSONDecodeError:
                    print(f"[!] Failed to parse JSON output from proxy_app_chat: {rs}")
                    return rs
            return rs
          except Exception as e:
            print(f"[!] Error in proxy_app_chat: {e}")
            return None

    async def proxy_app_tool(self) -> None:
        return None

    async def _fetch_urls(self, urls: list[str]) -> list[dict]:
        import aiohttp, asyncio
        from ws_bom_robot_app.llm.tools.utils import fetch_page, extract_content_with_trafilatura
        if not urls:
            return []
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_page(session, url) for url in urls]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
        final_results = []
        for item in responses:
            if isinstance(item, Exception):
                continue
            url = item["url"]
            html = item["html"]
            if html:
                content = await extract_content_with_trafilatura(html)
                if content:
                    final_results.append({"url": url, "content": content})
                else:
                    final_results.append({"url": url, "content": "No content found"})
            else:
                final_results.append({"url": url, "content": "Page not found"})
        return final_results

    async def search_online(self, query: str) -> list[dict]:
        from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
        # Wrapper DuckDuckGo
        search = DuckDuckGoSearchAPIWrapper(max_results=10)
        try:
          raw_results = search.results(query, max_results=10)
        except Exception as e:
            return f"[!] Errore ricerca: {e}"
        urls = [r["link"] for r in raw_results]
        return await self._fetch_urls(urls)

    async def search_online_google(self, query: str) -> list[dict]:
      from langchain_google_community import GoogleSearchAPIWrapper
      secrets = self.app_tool.secrets_to_dict()
      search_type = secrets.get("searchType")
      if search_type:
          search_kwargs = {"searchType" : search_type}
      search = GoogleSearchAPIWrapper(
          google_api_key=secrets.get("GOOGLE_API_KEY"),
          google_cse_id=secrets.get("GOOGLE_CSE_ID"),
      )
      if search_type:
          raw_results = search.results(query=query,
                     num_results=secrets.get("num_results", 5),
                     search_params=search_kwargs)
          return raw_results
      raw_results = search.results(
          query=query,
          num_results=secrets.get("num_results", 5)
      )
      urls = [r["link"] for r in raw_results]
      return await self._fetch_urls(urls)

    async def send_email(self, email_subject: str, body: str, to_email:str):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        secrets = self.app_tool.secrets
        secrets = {item["secretId"]: item["secretValue"] for item in secrets}
        import urllib.parse as urlparse
        url_preview = secrets.get("url_preview", "")
        if url_preview and url_preview != "":
          message_tread = "Puoi visualizzare la chat su questo indirizzo: " + urlparse.urljoin(url_preview, f"?llmThreadId={self.app_tool.thread_id}")
          body = body.replace("##url_preview##", message_tread)
        # Email configuration
        smtp_server = secrets.get("smtp_server")
        smtp_port = secrets.get("smtp_port")
        smtp_user = secrets.get("smtp_user")
        smtp_password = secrets.get("smtp_password")
        from_email = secrets.get("from_email")
        if not to_email or to_email == "":
          return "No recipient email provided"
        if not email_subject or email_subject == "":
          return "No email object provided"
        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = email_subject

        # Create the email body
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
          with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Use authentication and SSL only if password is provided
            if smtp_password:
              server.starttls()
              server.login(smtp_user, smtp_password)
            server.send_message(msg)
        except Exception as e:
          return f"Failed to send email: {str(e)}"
        return "Email sent successfully"

    #endregion

    #class variables (static)
    _list: dict[str,ToolConfig] = {
        f"{document_retriever.__name__}": ToolConfig(function=document_retriever, model=DocumentRetrieverInput),
        f"{image_generator.__name__}": ToolConfig(function=image_generator, model=ImageGeneratorInput),
        f"{llm_chain.__name__}": ToolConfig(function=llm_chain, model=LlmChainInput),
        f"{search_online.__name__}": ToolConfig(function=search_online, model=SearchOnlineInput),
        f"{search_online_google.__name__}": ToolConfig(function=search_online_google, model=SearchOnlineInput),
        f"{send_email.__name__}": ToolConfig(function=send_email, model=EmailSenderInput),
        f"{proxy_app_chat.__name__}": ToolConfig(function=proxy_app_chat, model=DocumentRetrieverInput),
        f"{proxy_app_tool.__name__}": ToolConfig(function=proxy_app_tool, model=NoopInput),

    }

    #instance methods
    def get_coroutine(self):
        tool_cfg = self._list.get(self.app_tool.function_name)
        return getattr(self, tool_cfg.function.__name__)  # type: ignore
