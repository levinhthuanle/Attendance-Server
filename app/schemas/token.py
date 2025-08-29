from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    model_config = ConfigDict(from_attributes=True)

class TokenRefresh(BaseModel):
    refresh_token: str
