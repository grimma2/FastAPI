from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    avatar: str


class UserOut(BaseModel):
    id: int
    username: str
    avatar: str


class Token(User):
    token: str


class ResponseToken(BaseModel):
    id: int
    token: str


class TokenPayload(BaseModel):
    user_id: int = None


class FollowerCreate(BaseModel):
    username: str


class FollowerList(BaseModel):
    user: UserOut
    subscriber: UserOut
