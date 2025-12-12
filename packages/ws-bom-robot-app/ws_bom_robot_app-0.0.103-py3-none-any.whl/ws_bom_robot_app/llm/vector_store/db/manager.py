from ws_bom_robot_app.llm.vector_store.db.base import VectorDBStrategy
from ws_bom_robot_app.llm.vector_store.db.chroma import Chroma
from ws_bom_robot_app.llm.vector_store.db.faiss import Faiss
from ws_bom_robot_app.llm.vector_store.db.qdrant import Qdrant

class VectorDbManager:
  _list: dict[str, VectorDBStrategy] = {
    "chroma": Chroma(),
    "faiss": Faiss(),
    "qdrant": Qdrant()
  }

  @classmethod
  def get_strategy(cls, name: str) -> VectorDBStrategy:
      return cls._list.get(name.lower(), Faiss())
