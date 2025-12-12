from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict
import asyncio
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores.base import VectorStoreRetriever, VectorStore
from langchain.retrievers import SelfQueryRetriever
from langchain.chains.query_constructor.schema import AttributeInfo
import tiktoken

class VectorDBStrategy(ABC):
    class VectorDBStrategy:
      """
      A strategy interface for managing vector databases. It caches and retrieves vector
      stores, providing mechanisms for creating them, retrieving them, and invoking
      document searches.
      Attributes:
        _CACHE (dict[str, VectorStore]):
          A dictionary that caches loaded VectoreStore(e.g. Faiss,Chroma,qDrant) indexes keyed by their storage IDs.
      Methods:
        create(embeddings, documents, storage_id, **kwargs):
          Asynchronously create a vector store using the provided embeddings,
          documents, and a unique storage identifier. Returns the created
          store's ID or None if creation fails.
        get_loader(embeddings, storage_id, **kwargs):
          Retrieve a vector store loader based on the provided embeddings
          and storage identifier. This loader can be used to perform
          further operations like retrieving documents.
        get_retriever(embeddings, storage_id, search_type, search_kwargs, **kwargs):
          Retrieve a VectorStoreRetriever for searching documents. Supports
          different search methods (e.g., similarity, mmr) and employs the
          appropriate strategy based on the search_type argument.
        supports_self_query():
          Indicates whether this strategy supports self-querying functionality.
          By default, returns True.
        _get_self_query_retriever(llm, store, description, metadata):
          Creates a SelfQueryRetriever using the specified language model,
          vector store, document description, and metadata. Used internally
          for self-querying when supported.
        invoke(embeddings, storage_id, query, search_type, search_kwargs, **kwargs):
          Asynchronously searches for documents based on a query. Depending
          on arguments and available metadata, either uses a self-query
          retriever or falls back to other retrieval methods (e.g., mixed
          similarity and mmr).
        _remove_duplicates(docs):
          Removes duplicate documents by checking their page content,
          returning a list with unique results.
        _combine_search(retrievers, query):
          Asynchronously invokes multiple retrievers in parallel, then merges
          their results while removing duplicates.
      """
    MAX_TOKENS_PER_BATCH = 300_000 * 0.8
    def __init__(self):
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")  # text-embedding-3-small, text-embedding-3-large: https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
        except Exception:
            self.encoding = None

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken or fallback estimation"""
        if self.encoding:
            try:
                return len(self.encoding.encode(text))
            except Exception:
                pass
        # fallback: rough estimation (1 token ≈ 4 characters)
        return len(text) // 4

    def _batch_documents_by_tokens(self, documents: list[Document]) -> list[list[Document]]:
      """Split documents into batches based on token count"""
      if not documents:
        return []
      batches = []
      current_batch = []
      current_token_count = 0

      for doc in documents:
          doc_tokens = self._count_tokens(doc.page_content)
          # check if adding this document exceeds the limit
          if current_token_count + doc_tokens > VectorDBStrategy.MAX_TOKENS_PER_BATCH:
              # start new batch if current batch is not empty
              if current_batch:
                  batches.append(current_batch)
              # reset current batch
              current_batch = [doc]
              current_token_count = doc_tokens  # reset to current doc's tokens
          else:
              # add to current batch
              current_batch.append(doc)
              current_token_count += doc_tokens

      # add final batch if not empty
      if current_batch:
          batches.append(current_batch)

      return batches

    _CACHE: dict[str, VectorStore] = {}
    def _clear_cache(self, key: str):
        if key in self._CACHE:
            del self._CACHE[key]

    @abstractmethod
    async def create(
        self,
        embeddings: Embeddings,
        documents: List[Document],
        storage_id: str,
        **kwargs
    ) -> Optional[str]:
        pass

    @abstractmethod
    def get_loader(
        self,
        embeddings: Embeddings,
        storage_id: str,
        **kwargs
    ) -> VectorStore:
        pass

    def get_retriever(
        self,
        embeddings: Embeddings,
        storage_id: str,
        search_type: str,
        search_kwargs: Dict[str, Any],
        **kwargs
    ) -> VectorStoreRetriever:
        return self.get_loader(embeddings, storage_id).as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )

    def supports_self_query(self) -> bool:
        return True

    @staticmethod
    def _get_self_query_retriever(llm:BaseChatModel,store:VectorStore,description:str, metadata: list[AttributeInfo]) -> SelfQueryRetriever:
        return SelfQueryRetriever.from_llm(
            llm=llm,
            vectorstore=store,
            document_contents=description,
            metadata_field_info=metadata,
            enable_limit=True,
            verbose=True
        )

    async def invoke(
        self,
        embeddings: Embeddings,
        storage_id: str,
        query: str,
        search_type: str,
        search_kwargs: Dict[str, Any],
        **kwargs
    ) -> List[Document]:
        if self.supports_self_query():
            if "app_tool" in kwargs and "llm" in kwargs:
                from ws_bom_robot_app.llm.tools.tool_manager import LlmAppTool
                app_tool: LlmAppTool = kwargs["app_tool"]
                _description,_metadata=app_tool.get_vector_filtering()
                if _description and _metadata:
                    llm: BaseChatModel = kwargs["llm"]
                    retriever = VectorDBStrategy._get_self_query_retriever(llm,self.get_loader(embeddings, storage_id),_description,_metadata)
                    return await retriever.ainvoke(query, config={"source": kwargs.get("source", "retriever")})
        if search_type == "mixed":
            similarity_retriever = self.get_retriever(embeddings, storage_id, "similarity", search_kwargs)
            mmr_kwargs = {
                "k": search_kwargs.get("k", 4),
                "fetch_k": search_kwargs.get("fetch_k", 20),
                "lambda_mult": search_kwargs.get("lambda_mult", 0.2),
            }
            mmr_retriever = self.get_retriever(embeddings, storage_id, "mmr", mmr_kwargs)
            return await VectorDBStrategy._combine_search([similarity_retriever, mmr_retriever], query)
        retriever = self.get_retriever(embeddings, storage_id, search_type, search_kwargs)
        return await retriever.ainvoke(query, config={"source": kwargs.get("source", "retriever")})

    @staticmethod
    def _remove_empty_documents(docs: List[Document]) -> List[Document]:
        return [doc for doc in docs if doc.page_content and doc.page_content.strip()]
    @staticmethod
    def _remove_duplicates(docs: List[Document]) -> List[Document]:
        seen = set()
        return [doc for doc in docs if not (doc.page_content in seen or seen.add(doc.page_content))]
    @staticmethod
    async def _combine_search(
        retrievers: List[VectorStoreRetriever],
        query: str
    ) -> List[Document]:
        tasks = [retriever.ainvoke(query, config={"source": "custom source"}) for retriever in retrievers]
        return VectorDBStrategy._remove_duplicates([doc for res in await asyncio.gather(*tasks) for doc in res])
