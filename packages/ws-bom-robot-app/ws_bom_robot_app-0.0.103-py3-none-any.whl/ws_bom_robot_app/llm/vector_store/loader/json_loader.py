import json
from typing import Optional
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader

class JsonLoader(BaseLoader):
  def __init__(self, file_path: str, meta_fields:Optional[list[str]] = [],encoding: Optional[str] = "utf-8"):
    self.file_path = file_path
    self.meta_fields = meta_fields
    self.encoding = encoding

  def load(self) -> list[Document]:
    with open(self.file_path, "r", encoding=self.encoding) as file:
      data = json.load(file)
    _list = data if isinstance(data, list) else [data]
    return [
      Document(
        page_content=json.dumps(item),
        metadata={
          "source": self.file_path,
          **{field: item.get(field) for field in self.meta_fields if item.get(field)}
        }
      )
      for item in _list
    ]
