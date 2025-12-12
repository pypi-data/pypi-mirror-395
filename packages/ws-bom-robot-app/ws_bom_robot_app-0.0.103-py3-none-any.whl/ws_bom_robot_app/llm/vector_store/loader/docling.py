import os, logging, traceback
from typing import Any, Iterator, AsyncIterator, Optional, Union
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.runnables import run_in_executor
from docling.document_converter import DocumentConverter, InputFormat, PdfFormatOption, ImageFormatOption
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableStructureOptions, TableFormerMode
from langchain_community.document_loaders import UnstructuredFileLoader
from ws_bom_robot_app.llm.vector_store.db.base import VectorDBStrategy
from docling.datamodel.pipeline_options import TableStructureOptions, TableFormerMode, RapidOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, ImageFormatOption

def _doclingConverter() -> DocumentConverter:
  _pipeline_config = {
      "accelerator_options": AcceleratorOptions(
          device=AcceleratorDevice.AUTO,
          cuda_use_flash_attention2=False,
      ),
      "table_structure_options": TableStructureOptions(mode=TableFormerMode.ACCURATE),
  }
  _base_pipeline_options = PdfPipelineOptions(
      **_pipeline_config,
      do_ocr=False)  
  _ocr_pipeline_options = PdfPipelineOptions(
      **_pipeline_config,
      ocr_options=RapidOcrOptions(
         print_verbose=False,         
         text_score=0.5,
         #rapidocr_params={"det_use_cuda": True}
         ))  
  doc_converter = DocumentConverter(
      format_options={          
          InputFormat.PDF: PdfFormatOption(
              pipeline_options=_base_pipeline_options,
          ),
          InputFormat.IMAGE: ImageFormatOption(
              pipeline_options=_ocr_pipeline_options,
          ),
      }
  )
  for frm in [InputFormat.PDF, InputFormat.IMAGE]:
     doc_converter.initialize_pipeline(frm)
  return doc_converter

class DoclingLoader(BaseLoader):
  _doc_converter: Optional[DocumentConverter] = None
  def __init__(self, file_path: str | list[str], **kwargs: Any) -> None:
      self._file_paths = file_path if isinstance(file_path, list) else [file_path]
      if DoclingLoader._doc_converter is None:
          DoclingLoader._doc_converter = _doclingConverter()
      self._converter = DoclingLoader._doc_converter
      self._kwargs = kwargs
  def load(self) -> list[Document]:
      """Load data into Document objects."""
      return list(self.lazy_load())
  async def aload(self) -> list[Document]:
      """Load data into Document objects."""
      return [document async for document in self.alazy_load()]
  async def alazy_load(self) -> AsyncIterator[Document]:
      """A lazy loader for Documents."""
      iterator = await run_in_executor(None, self.lazy_load)
      done = object()
      while True:
          doc = await run_in_executor(None, next, iterator, done)  # type: ignore[call-arg, arg-type]
          if doc is done:
              break
          yield doc  # type: ignore[misc]
  def _fallback_loader(self, source: str, error: Exception = None) -> Iterator[Document]:
      if 'fallback' in self._kwargs:
          if issubclass(self._kwargs['fallback'], (BaseLoader, UnstructuredFileLoader)):
            logging.info(f"Using fallback loader {self._kwargs['fallback']} for {source}")
            try:
              loader: Union[BaseLoader, UnstructuredFileLoader] = self._kwargs['fallback'](
                  source,
                  **{k: v for k, v in self._kwargs.items() if k != 'fallback'}
                  )
              yield from loader.lazy_load()
            except Exception as e:
              logging.warning(f"Failed to load document from {source}: {e} | {traceback.format_exc()}")
          else:
              logging.warning(f"Invalid fallback loader {self._kwargs['fallback']}[{type(self._kwargs['fallback'])}] for {source}")
      else:
        logging.warning(f"Failed to load document from {source}: {error}")
  def lazy_load(self) -> Iterator[Document]:
      for source in self._file_paths:
          try:
            #manage only small file with header, preventing header stripping and improper chunking
            if (source.endswith('.csv') or source.endswith('.xlsx')) \
                and 'fallback' in self._kwargs \
                and os.path.getsize(source) > (VectorDBStrategy.MAX_TOKENS_PER_BATCH // 4): #rough token estimate
              yield from self._fallback_loader(source)
            else:
              _result = self._converter.convert(
                os.path.abspath(source),
                raises_on_error=True)
              doc = _result.document
              text = doc.export_to_markdown(image_placeholder="")
              yield Document(page_content=text, metadata={"source": source})
          except Exception as e:
             yield from self._fallback_loader(source,e)

