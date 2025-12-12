from langchain_qdrant import QdrantVectorStore as QDRANT, FastEmbedSparse, RetrievalMode
from qdrant_client import QdrantClient
from langchain_core.documents import Document
from typing import Any, Optional
import asyncio, gc, logging, os
from langchain_core.embeddings import Embeddings
from ws_bom_robot_app.llm.utils.chunker import DocumentChunker
from ws_bom_robot_app.llm.vector_store.db.base import VectorDBStrategy


class Qdrant(VectorDBStrategy):
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
            _instance: QDRANT = None            
            if not os.path.exists(storage_id):
                os.makedirs(storage_id)

            for i, batch in enumerate(batches):
                batch_tokens = sum(self._count_tokens(doc.page_content) for doc in batch)
                logging.info(f"processing batch {i+1}/{len(batches)} with {len(batch)} docs ({batch_tokens:,} tokens)")
                # create instance from first batch
                if _instance is None:
                    _instance = await asyncio.to_thread(
                    QDRANT.from_documents,
                    documents=batch,
                    embedding=embeddings,
                    sparse_embedding=kwargs['sparse_embedding'] if 'sparse_embedding' in kwargs else FastEmbedSparse(),
                    collection_name="default",
                    path=storage_id,
                    retrieval_mode=RetrievalMode.HYBRID
                )
                else:
                    # merge to existing instance
                    await _instance.aadd_documents(batch)
                # add a small delay to avoid rate limiting
                if i < len(batches) - 1:  # except last batch
                    await asyncio.sleep(1)
            if _instance:                
                self._clear_cache(storage_id)
                logging.info(f"Successfully created {Qdrant.__name__} index with {len(chunked_docs)} total documents")
            return storage_id                
        except Exception as e:
            logging.error(f"{Qdrant.__name__} create error: {e}")
            raise e
        finally:
            del documents, chunked_docs, _instance
            gc.collect()

    def get_loader(
        self,
        embeddings: Embeddings,
        storage_id: str,
        **kwargs
    ) -> QDRANT:
        if storage_id not in self._CACHE:
            self._CACHE[storage_id] = QDRANT(
                client=QdrantClient(path=storage_id),
                collection_name="default",
                embedding=embeddings,
                sparse_embedding=FastEmbedSparse(),
                retrieval_mode=RetrievalMode.HYBRID,
            )
        return self._CACHE[storage_id]
