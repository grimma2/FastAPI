from typing import List

from pydantic import BaseModel
from user.schemas import User


class ShowProduct(BaseModel):
    name: str
    price: float
    desc: str
    user: User
    image: str


class ShowCart(BaseModel):
    products: List[ShowProduct]
    user: User


class Message(BaseModel):
    text: str
