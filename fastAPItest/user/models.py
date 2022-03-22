from typing import Type

import ormar
from config import MainMeta
from typing import Optional, Union, Dict


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    email = ormar.String(index=True, unique=True, nullable=False, max_length=255)
    avatar = ormar.String(max_length=500, nullable=True)
    is_active = ormar.Boolean(default=True, nullable=False)
    is_superuser = ormar.Boolean(default=False, nullable=False)


class Follower(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="user")
    subscriber: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="subscriber")
