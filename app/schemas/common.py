from pydantic import BaseModel, ConfigDict

class Pagination(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list
    total: int
    page: int
    size: int

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str

class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str
    role: str
    user_id: int
    name: str