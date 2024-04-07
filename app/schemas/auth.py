from pydantic import BaseModel

class SignupRequest(BaseModel):
    username: str
    password1: str
    password2: str
    email: str


class LoginRequest(BaseModel):
    email: str
    password: str