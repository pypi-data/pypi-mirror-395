from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
import logging

class DocumentChunker:
  _MAX_CHUNK_SIZE = 10_000
  @staticmethod
  def chunk(documents: list[Document]) -> list[Document]:
      text_splitter = CharacterTextSplitter(chunk_size=DocumentChunker._MAX_CHUNK_SIZE, chunk_overlap=int(DocumentChunker._MAX_CHUNK_SIZE * 0.02))
      chunked_documents = []
      for doc in documents:
          if len(doc.page_content) <= DocumentChunker._MAX_CHUNK_SIZE:
              chunked_documents.append(doc)
              continue
          chunks = text_splitter.split_text(doc.page_content)
          for chunk in chunks:
              chunked_documents.append(
                  Document(page_content=chunk, metadata=doc.metadata)
              )
      return chunked_documents
