from fastapi import HTTPException

from . import tokenizator
from google.oauth2 import id_token
from google.auth.transport import requests

from . import schemas, models


GOOGLE_CLIENT_ID = "662631671173-f18d9nv86u11ovasa1t2i3a6q2gbl5ua.apps.googleusercontent.com"


async def create_user(user: schemas.Token) -> models.User:
    _user = await models.User.objects.get_or_create(**user.dict(exclude={"token"}))
    return _user


async def google_auth(user: schemas.Token) -> tuple:
    try:
        idinfo = id_token.verify_oauth2_token(user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    user = await create_user(user)
    internal_token = tokenizator.create_token(user.id)
    return user.id, internal_token.get("access_token")
