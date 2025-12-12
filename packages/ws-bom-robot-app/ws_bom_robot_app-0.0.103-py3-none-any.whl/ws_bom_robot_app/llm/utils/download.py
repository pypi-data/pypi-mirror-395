import httpx
from typing import List,Optional
import os, logging, aiohttp, asyncio, hashlib, json
import uuid
from pydantic import BaseModel
import base64, requests, mimetypes
from urllib.parse import urlparse
from tqdm.asyncio import tqdm
from ws_bom_robot_app.config import config
import aiofiles

async def download_files(urls: List[str], destination_folder: str, authorization: str = None):
    tasks = [download_file(file, os.path.join(destination_folder, os.path.basename(file)), authorization=authorization) for file in urls]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    for i, result in enumerate(results):
        if not result:
            raise Exception(f"Download failed for file: {urls[i]}")

async def download_file(url: str, destination: str, chunk_size: int = 8192, authorization: str = None) -> Optional[str]:
  """
  Downloads a file from a given URL to a destination path asynchronously.

  Args:
      url: The URL of the file to download
      destination: The local path where the file should be saved
      chunk_size: Size of chunks to download (default: 8192 bytes)

  Returns:
      str: Path to the downloaded file if successful, None otherwise

  Raises:
      Various exceptions are caught and logged
  """
  try:
      # Ensure the destination directory exists
      os.makedirs(os.path.dirname(os.path.abspath(destination)), exist_ok=True)

      async with httpx.AsyncClient(timeout=30.0) as client:
          if authorization:
            headers = {'Authorization': authorization}
          async with client.stream("GET", url, headers=headers) as response:
              # Check if the request was successful
              if response.status_code != 200:
                  logging.error(f"Failed to download file. Status code: {response.status_code}")
                  return None

              # Get the total file size if available
              total_size = int(response.headers.get('content-length', 0))
              # Open the destination file and write chunks
              with open(destination, 'wb') as f:
                  with tqdm(
                      total=total_size,
                      desc="Downloading",
                      unit='B',
                      unit_scale=True,
                      unit_divisor=1024
                  ) as pbar:
                      async for chunk in response.aiter_bytes(chunk_size):
                          if chunk:
                              f.write(chunk)
                              pbar.update(len(chunk))

              logging.info(f"File downloaded successfully to {destination}")
              return destination

  except httpx.RequestError as e:
      logging.error(f"Network error occurred: {str(e)}")
      return None
  except asyncio.TimeoutError:
      logging.error("Download timed out")
      return None
  except IOError as e:
      logging.error(f"IO error occurred: {str(e)}")
      return None
  except Exception as e:
      logging.error(f"Unexpected error occurred: {str(e)}")
      return None
  finally:
      # If download failed and file was partially created, clean it up
      if os.path.exists(destination) and os.path.getsize(destination) == 0:
          try:
              os.remove(destination)
              logging.info(f"Cleaned up incomplete download: {destination}")
          except OSError:
              pass

class Base64File(BaseModel):
    """Base64 encoded file representation"""
    url: str
    base64_url: str
    base64_content: str
    name: str
    extension: str
    mime_type: str

    @staticmethod
    def _is_base64_data_uri(url: str) -> bool:
        """Check if URL is already a base64 data URI"""
        return (isinstance(url, str) and
                url.startswith('data:') and
                ';base64,' in url and
                len(url.split(',')) == 2)

    async def from_url(url: str) -> "Base64File":
      """Download file and return as base64 data URI"""
      def _cache_file(url: str) -> str:
          _hash = hashlib.md5(url.encode()).hexdigest()
          return os.path.join(config.robot_data_folder, config.robot_data_attachment_folder, f"{_hash}.json")
      async def from_cache(url: str) -> "Base64File":
        """Check if file is already downloaded and return data"""
        _file = _cache_file(url)
        if os.path.exists(_file):
          try:
            async with aiofiles.open(_file, 'rb') as f:
              content = await f.read()
            return Base64File(**json.loads(content))
          except Exception as e:
              logging.error(f"Error reading cache file {_file}: {e}")
              return None
        return None
      async def to_cache(file: "Base64File", url: str) -> None:
        """Save file to cache"""
        _file = _cache_file(url)
        try:
            async with aiofiles.open(_file, 'wb') as f:
                await f.write(file.model_dump_json().encode('utf-8'))
        except Exception as e:
            logging.error(f"Error writing cache file {_file}: {e}")

     # special case: base64 data URI
      if Base64File._is_base64_data_uri(url):
            mime_type = url.split(';')[0].replace('data:', '')
            base64_content = url.split(',')[1]
            extension=mime_type.split('/')[-1]
            name = f"file-{uuid.uuid4()}.{extension}"
            return Base64File(
              url=url,
              base64_url=url,
              base64_content=base64_content,
              name=name,
              extension=extension,
              mime_type=mime_type
            )

      # default download
      _error = None
      try:
          if _content := await from_cache(url):
              return _content
          async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            logging.info(f"Downloading {url} - Status: {response.status_code}")
            response.raise_for_status()
            content = response.read()
            # mime type detection
            mime_type = response.headers.get('content-type', '').split(';')[0]
            if not mime_type:
                mime_type, _ = mimetypes.guess_type(urlparse(url).path)
            if not mime_type:
                mime_type = 'application/octet-stream'
            # to base64
            base64_content = base64.b64encode(content).decode('utf-8')
            name = url.split('/')[-1]
            extension = name.split('.')[-1]
      except Exception as e:
          _error = f"Failed to download file from {url}: {e}"
          logging.error(_error)
          base64_content = base64.b64encode(_error.encode('utf-8')).decode('utf-8')
          name = "download_error.txt"
          mime_type = "text/plain"
          extension = "txt"

      _file = Base64File(
          url=url,
          base64_url= f"data:{mime_type};base64,{base64_content}",
          base64_content=base64_content,
          name=name,
          extension=extension,
          mime_type=mime_type
      )
      if not _error:
        await to_cache(_file, url)
      return _file
