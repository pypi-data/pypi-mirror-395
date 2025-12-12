from langchain_chroma import Chroma as CHROMA
from langchain_core.documents import Document
from typing import Any, Optional
import asyncio, gc, logging
from langchain_core.embeddings import Embeddings
from ws_bom_robot_app.llm.utils.chunker import DocumentChunker
from ws_bom_robot_app.llm.vector_store.db.base import VectorDBStrategy


class Chroma(VectorDBStrategy):
    """
    A strategy class for interacting with a Chroma-based vector store implementation.
    This class provides methods to create a Chroma vector store from a list of documents
    and retrieve an existing Chroma instance. The vector store can be used to perform
    operations such as embedding documents, persisting them to a storage directory, and
    later loading them for retrieval tasks.
    Attributes:
      _CACHE (dict[str, CHROMA]): A cache to store and reuse Chroma instances.
    Methods:
      create(embeddings, documents, storage_id, **kwargs):
        Creates a new Chroma instance after chunking the provided documents
        and embedding them. Persists the vector store in the given storage directory.
        If any error occurs during creation, logs the error and returns None.
        Args:
          embeddings (Embeddings): The embeddings strategy used to embed documents.
          documents (list[Document]): The list of documents to be chunked and embedded.
          storage_id (str): The directory where the Chroma vector store should be persisted.
          **kwargs: Additional keyword arguments.
        Returns:
          Optional[str]: The storage ID if creation is successful; otherwise, None.
      get_loader(embeddings, storage_id, **kwargs):
        Retrieves a Chroma instance from the cache if it exists;
        otherwise, creates and caches a new instance using the given embeddings and storage ID.
        Args:
          embeddings (Embeddings): The embeddings strategy used to create or load the Chroma instance.
          storage_id (str): The directory where the Chroma vector store is persisted.
          **kwargs: Additional keyword arguments.
        Returns:
          CHROMA: The retrieved or newly created Chroma instance.
    """
    def __init__(self):
        super().__init__()

    async def create(
        self,
        embeddings: Embeddings,
        documents: list[Document],
        storage_id: str,
        **kwargs
    ) -> Optional[str]:
        try:
            documents = self._remove_empty_documents(documents)
            chunked_docs = DocumentChunker.chunk(documents)
            batches = self._batch_documents_by_tokens(chunked_docs)
            logging.info(f"documents: {len(documents)}, after chunking: {len(chunked_docs)}, processing batches: {len(batches)}")
            _instance: CHROMA = None
            for i, batch in enumerate(batches):
                batch_tokens = sum(self._count_tokens(doc.page_content) for doc in batch)
                logging.info(f"processing batch {i+1}/{len(batches)} with {len(batch)} docs ({batch_tokens:,} tokens)")
                # create instance from first batch
                if _instance is None:
                    _instance = await asyncio.to_thread(
                    CHROMA.from_documents,
                    documents=batch,
                    embedding=embeddings,
                    persist_directory=storage_id
                )
                else:
                    # merge to existing instance
                    await _instance.aadd_documents(batch)
                # add a small delay to avoid rate limiting
                if i < len(batches) - 1:  # except last batch
                    await asyncio.sleep(1)
            if _instance:
                self._clear_cache(storage_id)
                logging.info(f"Successfully created {Chroma.__name__} index with {len(chunked_docs)} total documents")
            return storage_id
        except Exception as e:
            logging.error(f"{Chroma.__name__} create error: {e}")
            raise e
        finally:
            del documents, chunked_docs, _instance
            gc.collect()

    def get_loader(
        self,
        embeddings: Embeddings,
        storage_id: str,
        **kwargs
    ) -> CHROMA:
        if storage_id not in self._CACHE:
            self._CACHE[storage_id] = CHROMA(
                collection_name="default",
                embedding_function=embeddings,
                persist_directory=storage_id
            )
        return self._CACHE[storage_id]
