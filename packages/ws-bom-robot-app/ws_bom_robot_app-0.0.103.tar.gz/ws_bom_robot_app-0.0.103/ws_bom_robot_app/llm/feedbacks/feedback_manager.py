from ws_bom_robot_app.llm.models.feedback import NebulyFeedbackPayload, NebulyFeedbackAction, NebulyFeedbackMetadata
from ws_bom_robot_app.config import config
from pydantic import BaseModel, Field
from typing import Optional
import requests

class FeedbackConfig(BaseModel):
    """
    FeedbackConfig is a model that represents the configuration for feedback management.
    It includes the API key and the URL for the feedback service.
    """
    api_key: str = Field(..., description="The API key for authentication")
    provider: str = Field(..., description="The provider of the feedback service")
    user_id: str = Field(..., description="The user ID for the feedback service")
    message_input: Optional[str] = Field(default=None, description="The input message to which the feedback refers")
    message_output: Optional[str] = Field(default=None, description="The output message to which the feedback refers")
    comment: str = Field(..., description="The comment provided by the user")
    rating: int = Field(..., description="The rating given by the user (from 1 to 5)", ge=1, le=5)
    anonymize: bool = Field(False, description="Boolean flag. If set to true, PII will be removed from the text field")
    timestamp: str = Field(..., description="The timestamp of the feedback event")
    message_id: Optional[str] = Field(default=None, description="The message ID for the feedback")

class FeedbackInterface:
    def __init__(self, config: FeedbackConfig):
      self.config = config

    def send_feedback(self):
      raise NotImplementedError

class NebulyFeedback(FeedbackInterface):
    def __init__(self, config: FeedbackConfig):
      super().__init__(config)
      self.config = config

    def send_feedback(self) -> str:
      if not self.config.api_key:
        return "Error sending feedback: API key is required for Nebuly feedback"
      headers = {
        "Authorization": f"Bearer {self.config.api_key}",
        "Content-Type": "application/json"
      }
      action = NebulyFeedbackAction(
        slug="rating",
        text=self.config.comment,
        value=self.config.rating
      )
      metadata = NebulyFeedbackMetadata(
        end_user=self.config.user_id,
        timestamp=self.config.timestamp,
        anonymize=self.config.anonymize
      )
      payload = NebulyFeedbackPayload(
        action=action,
        metadata=metadata
      )
      url = f"{config.NEBULY_API_URL}/event-ingestion/api/v1/events/feedback"
      response = requests.request("POST", url, json=payload.model_dump(), headers=headers)
      if response.status_code != 200:
        raise Exception(f"Error sending feedback: {response.status_code} - {response.text}")
      return response.text

class FeedbackManager:
    #class variables (static)
    _list: dict[str,FeedbackInterface] = {
        "nebuly": NebulyFeedback,
    }
