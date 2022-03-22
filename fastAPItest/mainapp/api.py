from fastapi import (
    APIRouter, HTTPException, Query, UploadFile, File, Request, Depends
)
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from config import app
from .models import DBProduct
from .services import load_images
from .schemas import Message
from config import templates

from user import models, auth

from uuid import uuid4

main_router = APIRouter()


@main_router.get('/products/{product_id}', responses={404: {'model': Message}})
async def get_product(request: Request, product_id: int):
    product = await DBProduct.objects.get(id=product_id)
    if product:
        return templates.TemplateResponse(
            'product.html', {'request': request, 'product': product}
        )
    else:
        return JSONResponse(status_code=404, content={'message': 'Item not found'})


@main_router.post('/product_form')
async def create_product(
        background_tasks: BackgroundTasks,
        desc: str,
        count: int,
        image: UploadFile = File(...),
        name: str = Query(..., max_length = 255),
        price: float = Query(..., gt = 100.00),
        user: models.User = Depends(auth.get_user)
):
    lim = image.content_type.split('/')[-1]
    if lim == 'png':
        file_name = f'media/{user.dict()["id"]}/{image.filename}/{uuid4()}.png'
        background_tasks.add_task(load_images, image, file_name)
    else:
        raise HTTPException(
            status_code=418, detail='as minimum one file from takes been not png'
        )

    return await DBProduct.objects.create(
        name=name, desc=desc, price=price, count=count,
        image=file_name, user=user
    )


@main_router.delete('/deleteproduct/{product_id}')
async def create_product(product_id: int, user: models.User = Depends(auth.get_user)):
    product = await DBProduct.objects.get_or_none(id=product_id)
    if product:
        await product.delete()
    return {}
