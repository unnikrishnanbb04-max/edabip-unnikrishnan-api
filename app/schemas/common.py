from pydantic import BaseModel, ConfigDict

class Pagination(BaseModel):
    items: list
    total: int
    page: int
    size: int

class MessageResponse(BaseModel):
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
