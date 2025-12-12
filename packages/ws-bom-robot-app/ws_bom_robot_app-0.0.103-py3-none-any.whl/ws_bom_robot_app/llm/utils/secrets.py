import json, os, logging
from typing import Union
class Secrets:
  @staticmethod
  def from_file(path: str) -> dict[str, Union[str, int, list]] | None:
    if os.path.exists(path):
      with open(path, 'r') as file:
        _content = file.read()
        try:
          return json.loads(_content)
        except json.JSONDecodeError:
          logging.error(f"Failed to parse secret file: {path}")
    else:
      logging.error(f"Secret file not found: {path}")
    return None
  @staticmethod
  def from_env(key: str) -> dict[str, Union[str, int, list]] | None:
    _content = os.getenv(key)
    if _content:
      try:
        return json.loads(_content)
      except json.JSONDecodeError:
        logging.error(f"Failed to parse environment variable: {key}")
    else:
      logging.error(f"Environment variable not found: {key}")
    return None
