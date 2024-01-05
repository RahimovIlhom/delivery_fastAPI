from fastapi import APIRouter

order_router = APIRouter(prefix='/order')


@order_router.get('/')
async def order_root():
    return {'message': 'Order root'}
