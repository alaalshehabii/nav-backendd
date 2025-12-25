from pydantic import BaseModel, EmailStr

class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
