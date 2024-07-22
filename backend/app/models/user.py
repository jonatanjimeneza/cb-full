from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    company: str
    email: EmailStr
    password: str
    terms_accepted: bool

class UserInDB(UserCreate):
    hashed_password: str

class User(BaseModel):
    first_name: str
    last_name: str
    company: str
    email: EmailStr

class Email(BaseModel):
    email: EmailStr