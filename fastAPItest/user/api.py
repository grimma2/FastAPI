from fastapi import APIRouter, Request, Depends

from typing import List
from . import schemas, services, models, auth
from config import templates


user_router = APIRouter(tags=['auth'])


@user_router.get('/')
async def render_google_auth(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@user_router.post('/google/auth', response_model=schemas.ResponseToken)
async def end_google_auth(user: schemas.Token):
    user_id, token = await services.google_auth(user)
    return schemas.ResponseToken(token=token, id=user_id)


@user_router.post('/', status_code=201)
async def add_follower(
        schema: schemas.FollowerCreate, user: models.User = Depends(auth.get_user)
):
    host = await models.User.objects.get(username=schema.username)
    return await models.Follower.objects.create(subscriber=user.dict(), user=host)


@user_router.get('/', response_model=List[schemas.FollowerList])
async def my_list_following(user: models.User = Depends(auth.get_user)):
    return await models.Follower.objects.select_related(
        ['user', 'subscriber']
    ).filter(subscriber=user.id).all()


@user_router.delete('/{username}', status_code=204)
async def delete_follower(username: str, user: models.User = Depends(auth.get_user)):
    follower = await models.Follower.objects.get_or_none(
        user__username=username, subscriber=user.id)
    if follower:
        await follower.delete()
    return {}


@user_router.get('/me', response_model=List[schemas.FollowerList])
async def my_list_follower(user: models.User = Depends(auth.get_user)):
    return await models.Follower.objects.select_related(
        ['user', 'subscriber']
    ).filter(user=user.id).all()
