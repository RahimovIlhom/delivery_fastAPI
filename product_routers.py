from fastapi import APIRouter, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from fastapi.exceptions import HTTPException

from auth_routers import access_security
from database import session, engine
from models import Product, User
from schemas import ProductModel

product_router = APIRouter(prefix='/product')
session = session(bind=engine)


@product_router.post('/add', status_code=201)
async def app_product(product: ProductModel, credentials: JwtAuthorizationCredentials = Security(access_security)):
    if len(product.name) > 2:
        if product.price > 5000:
            username = credentials['username']
            current_user = session.query(User).filter(User.username == username).first()
            if current_user.is_staff:
                new_product = Product(name=product.name, price=product.price)
                session.add(new_product)
                session.commit()
                data = {
                    'ok': True,
                    'message': 'Product qo\'shildi',
                    'data': product
                }
                return data
            else:
                return HTTPException(status_code=404)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Product qo\'shilmadi')

