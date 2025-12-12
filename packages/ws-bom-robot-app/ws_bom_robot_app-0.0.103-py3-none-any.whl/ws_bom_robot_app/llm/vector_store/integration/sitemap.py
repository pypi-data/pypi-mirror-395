import sys, asyncio
from typing import Any, AsyncGenerator, AsyncIterator
import aiofiles
import aiofiles.os
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.document_transformers import MarkdownifyTransformer as markdownify
from langchain_core.documents import Document
from langchain_core.runnables import run_in_executor
from bs4 import BeautifulSoup, Tag

class Sitemap(IntegrationStrategy):
    """Class to load a sitemap.xml file and extract text from the URLs.
      Load a sitemap.xml file and extract text from the urls.
    Args:
        data (dict[str, str]):
        data["sitemapUrl"] (str): absolute/relative url of the sitemap.xml
        data["outputFormat"] (str): ["text", "html", "markdown"] default to "text"
        data["filterUrls"] list[str]: list of regex pattern to filter urls ["https://www.example.com/en/products", "^.*products.*$"]
        data["includeOnlySelector"] : list[str] [".content", "#main-article", "article p"]
        data["excludeTag"] (list[str]): default to ["script", "noscript", "style", "head", "header","nav","footer", "iframe"]
        data["excludeClass"] (list[str]): ["class1", "class2"]
        data["excludeId"] (list[str]): ["id1", "id2"]
        data["restrictDomain"] (bool): if True, only urls from the same domain will be loaded, default to True
    """
    def __init__(self, knowledgebase_path: str, data: dict[str, Any]):
        super().__init__(knowledgebase_path, data)
        self.__sitemap_url = self.data.get("sitemapUrl")
        self.__filter_urls: list[str] = self.data.get("filterUrls",[]) # type: ignore
        self.__output_format: str = self.data.get("outputFormat", "text") # type: ignore
        self.__include_only_selectors: list[str] = self.data.get("includeOnlySelector", []) # type: ignore
        self.__exclude_tag: list[str] = self.data.get("excludeTag",[]) # type: ignore
        self.__exclude_class: list[str] = self.data.get("excludeClass",[]) # type: ignore
        self.__exclude_id: list[str] = self.data.get("excludeId",[]) # type: ignore
        self.__restrict_to_same_domain: bool = self.data.get("restrictDomain", True) # type: ignore
        self.__header_template = self.data.get("headers", None)
    def working_subdirectory(self) -> str:
        return ""
    def _extract(self, tag: Tag) -> str:
        return tag.get_text() if self.__output_format == "text" else tag.prettify()
    def _output(self, documents: list[Document]) -> list[Document]:
        return list(markdownify().transform_documents(documents)) if self.__output_format == "markdown" else documents
    def _parse(self,content: BeautifulSoup) -> str:
        if self.__include_only_selectors:
            extracted = []
            for selector in self.__include_only_selectors:
                matching_elements = content.select(selector)
                for element in matching_elements:
                    extracted.append(self._extract(element))
            return '\n\n'.join(extracted)
        else:
            selectors: list[str] = ["script", "noscript", "style", "head", "header","nav","footer", "iframe"]
            selectors.extend(
                self.__exclude_tag
                + [f".{class_name}" for class_name in self.__exclude_class]
                + [f"#{id_name}" for id_name in self.__exclude_id]
                )
            for element in selectors:
                for _ in content.select(element):
                    _.decompose()
            return str(self._extract(content))
    def _is_local(self, url: str) -> bool:
        return not url.startswith("http")

    def _remap_if_local(self, url: str) -> str:
        return f"{self.knowledgebase_path}/{url}" if self._is_local(url) else url
    async def alazy_load(self,loader: SitemapLoader) -> AsyncIterator[Document]:
        """A lazy loader for Documents."""
        if sys.platform == 'win32':
          asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        iterator = await run_in_executor(None, loader.lazy_load)
        done = object()
        while True:
            doc = await run_in_executor(None, next, iterator, done)  # type: ignore[call-arg, arg-type]
            if doc is done:
                break
            yield doc  # type: ignore[misc]
    async def load(self) -> list[Document]:
        if (self.__sitemap_url):
            _loader = SitemapLoader(
                web_path=self._remap_if_local(self.__sitemap_url),
                filter_urls=self.__filter_urls,
                parsing_function=self._parse,
                is_local=self._is_local(self.__sitemap_url),
                restrict_to_same_domain=self.__restrict_to_same_domain,
                header_template=self.__header_template
            )
            _docs = self._output([document async for document in self.alazy_load(_loader)])
            if self._is_local(self.__sitemap_url):
              try:
                  await aiofiles.os.remove(_loader.web_path)
              except FileNotFoundError:
                  pass
            return _docs
        return []
