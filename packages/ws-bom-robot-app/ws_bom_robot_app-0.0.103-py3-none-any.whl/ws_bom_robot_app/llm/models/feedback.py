from pydantic import BaseModel, Field

class NebulyFeedbackAction(BaseModel):
    """
    FeedbackAction is a model that represents the action taken by the user
    in response to the feedback provided by the LLM.
    """
    slug: str = Field("rating", description="A string identifier for the feedback action",
             enum=["thumbs_up", "thumbs_down", "copy_input", "copy_output", "paste", "rating"])
    text: str = Field(..., description="The text content of the feedback")
    value: int = Field(..., description="A numeric value associated with the feedback")

class NebulyFeedbackMetadata(BaseModel):
  """
  FeedbackMetadata is a model that represents the metadata associated with user feedback.
  This includes information about the interaction and the user who provided feedback.
  """
  input: str = Field(None, description="The input of the interactions to which the action refers to")
  output: str = Field(None, description="The output of the interactions to which the action refers to")
  end_user: str = Field(..., description="The identifier used for the end-user")
  timestamp: str = Field(..., description="The timestamp of the action event")
  anonymize: bool = Field(False, description="Boolean flag. If set to true, PII will be removed from the text field")

class NebulyFeedbackPayload(BaseModel):
  """
  NebulyFeedback is a model that combines feedback action and metadata.
  It represents a complete feedback entry from a user interaction with the LLM.
  """
  action: NebulyFeedbackAction = Field(..., description="The action taken by the user as feedback")
  metadata: NebulyFeedbackMetadata = Field(..., description="Metadata associated with the feedback")
