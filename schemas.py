from pydantic import BaseModel
from typing import Optional

from models import User


class SingUp(BaseModel):
    username: str
    email: str
    fullname: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'username': 'ilhomjon',
                'email': 'example@mail.ru',
                'fullname': "Ali Valiyev",
                'password': 'qwerty123',
                'is_staff': False,
                'is_active': True
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str


class ProductModel(BaseModel):
    name: str
    price: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'name': 'Kastyum',
                'price': 1000000
            }
        }


class UpdateProduct(BaseModel):
    id: int
    name: Optional[str]
    price: Optional[int]
