from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from typing import Any, Optional
import asyncio, gc, logging
from langchain_core.embeddings import Embeddings
from ws_bom_robot_app.llm.utils.chunker import DocumentChunker
from ws_bom_robot_app.llm.vector_store.db.base import VectorDBStrategy

class Faiss(VectorDBStrategy):
    """
    Faiss is a vector database strategy that leverages a FAISS index to store and retrieve
    vectorized documents. It provides methods for creating a new FAISS index and for
    loading an existing index from a local directory, with an internal caching mechanism
    to optimize repeated retrievals.
    Methods:
      create(
        Asynchronously creates a FAISS index from the given documents, using the
        provided embeddings, then saves it locally under the specified storage ID.
        Returns the storage ID if successful, or None otherwise.
      get_loader(
        Retrieves a FAISS index associated with a given storage ID. If this index
        was previously loaded and cached, it returns the cached instance; otherwise,
        it loads the index from local storage and caches it for subsequent use.
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
            _instance: FAISS = None
            for i, batch in enumerate(batches):
                batch_tokens = sum(self._count_tokens(doc.page_content) for doc in batch)
                logging.info(f"processing batch {i+1}/{len(batches)} with {len(batch)} docs ({batch_tokens:,} tokens)")
                # init
                _batch_instance = await asyncio.to_thread(
                    FAISS.from_documents,
                    batch,
                    embeddings
                )
                # create instance from first batch
                if _instance is None:
                    _instance = _batch_instance
                else:
                    # merge to existing instance
                    await asyncio.to_thread(
                        _instance.merge_from,
                        _batch_instance
                    )
                del _batch_instance
                gc.collect()
                # add a small delay to avoid rate limiting
                if i < len(batches) - 1:  # except last batch
                    await asyncio.sleep(1)
            if _instance:
                await asyncio.to_thread(_instance.save_local, storage_id)
                self._clear_cache(storage_id)
                logging.info(f"Successfully created {Faiss.__name__} index with {len(chunked_docs)} total documents")
            return storage_id
        except Exception as e:
            logging.error(f"{Faiss.__name__} create error: {e}")
            raise e
        finally:
            del documents, chunked_docs, _instance
            gc.collect()

    def get_loader(
        self,
        embeddings: Embeddings,
        storage_id: str,
        **kwargs
    ) -> FAISS:
        if storage_id not in self._CACHE:
            self._CACHE[storage_id] = FAISS.load_local(
                folder_path=storage_id,
                embeddings=embeddings,
                allow_dangerous_deserialization=True
            )
        return self._CACHE[storage_id]

    def supports_self_query(self) -> bool:
        return False
