import uuid
from datetime import datetime
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from typing import Optional

class AgentContext(BaseModel):
    class _i18n(BaseModel):
        lg: Optional[str] = "en"
        country: Optional[str] = "US"
        timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S %A"))
        timezone: Optional[str] = "UTC"
        model_config = ConfigDict(extra='allow')
    class _user(BaseModel):
        id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        first_name: Optional[str] = Field(None, validation_alias=AliasChoices("firstName","first_name"))
        last_name: Optional[str] = Field(None, validation_alias=AliasChoices("lastName","last_name"))
        country: Optional[str] = ''
        email: Optional[str] = ''
        phone: Optional[str] = ''
        role: Optional[list] = [] #i.e. ["admin","user","guest"]
        department: Optional[list] = [] #i.e. ["R&D","IT","HR"]
        permission: Optional[list] = [] #i.e. ["read","write","delete","execute"]
        model_config = ConfigDict(extra='allow')
    i18n: _i18n = Field(default_factory=_i18n)
    user: Optional[_user] =Field(default_factory=_user)
    model_config = ConfigDict(extra='allow')
