from odmantic import Model, EmbeddedModel
from typing import Optional
from pydantic import EmailStr

class User(Model):
    username: str
    email: EmailStr
    hashed_password: str
    role: str
    is_active: bool = False
    is_verified: bool = False

class Token(Model):
    access_token: str
    token_type: str

class TokenData(Model):
    username: Optional[str] = None