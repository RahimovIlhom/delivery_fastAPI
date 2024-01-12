from fastapi import FastAPI

from auth_routers import auth_router
from order_routers import order_router
from product_routers import product_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)


@app.get('/')
async def main_root():
    return {'message': "Home Page"}

