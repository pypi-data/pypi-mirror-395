from pydantic import BaseModel, Field

class NoopInput(BaseModel):
  pass
class DocumentRetrieverInput(BaseModel):
  query: str = Field(description="The search query string")
class ImageGeneratorInput(BaseModel):
  query: str = Field(description="description of the image to generate.")
  language: str = Field(description="Language of the query. Default is 'it'", default="it")
class LlmChainInput(BaseModel):
  input: str = Field(description="Input to the LLM chain")
class SearchOnlineInput(BaseModel):
  query: str = Field(description="The search query string")
class EmailSenderInput(BaseModel):
  email_subject: str = Field(description="The subject of the email to send")
  body: str = Field(description="The body of the email to send")
  to_email: str = Field(description="The recipient email address")
