from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
class Page(BaseModel):
    items: list
    total: int
    page: int
    size: int
class ScheduleIn(BaseModel):
    report_id: int = Field(gt=0)
    frequency: str
    next_run_at: datetime
