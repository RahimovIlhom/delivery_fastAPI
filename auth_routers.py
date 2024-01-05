from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

from database import session, engine
from models import User
from schemas import SingUp

auth_router = APIRouter(prefix='/auth')

session = session(bind=engine)


@auth_router.get('/')
async def auth_root():
    return {'message': 'Auth root'}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SingUp):
    check_username = session.query(User).filter(
        User.username == user.username).first()  # User.objects.filter(username = username)
    if check_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday nomli foydalanuvchi bor')
    check_email = session.query(User).filter(
        User.email == user.email).first()  # User.objects.filter(username = username)
    if check_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday emailli foydalanuvchi bor')

    new_user = User(
        username=user.username,
        email=user.email,
        fullname=user.fullname,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active,
    )
    session.add(new_user)
    session.commit()

    data = user
    response = {
        'ok': True,
        'message': "Foydalanuvchi saqlandi!",
        'data': data
    }
    return response
