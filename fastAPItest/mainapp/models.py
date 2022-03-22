import ormar

from typing import Optional

from config import MainMeta
from user.models import User


class DBProduct(ormar.Model):

    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255)
    price: float = ormar.Float(minimum=100.00)
    desc: str = ormar.String(max_length=255)
    user: User = ormar.ForeignKey(User)
    count: int = ormar.Integer()
    image: str


class DBCart(ormar.Model):

    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    products: Optional[DBProduct] = ormar.ForeignKey(DBProduct)
    user: User = ormar.ForeignKey(User)
