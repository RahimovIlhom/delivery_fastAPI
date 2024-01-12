from fastapi import APIRouter, status, Security
from fastapi.exceptions import HTTPException
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from werkzeug.security import generate_password_hash, check_password_hash

from database import session, engine
from models import User
from schemas import SingUp, LoginModel

auth_router = APIRouter(prefix='/auth')

session = session(bind=engine)


access_security = JwtAccessBearer(secret_key="2098b126a4c53821530d867da4e00812229ed918c0e57fd0fb2773585c13a766",
                                  auto_error=True)


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

# identifikatsiya - Foydalanuvchini aniqlash
# authentifikatsiya - haqiqiyligini tekshirish
# autorizatsiya - Avtorizatsiya sizning shaxsingiz tizim tomonidan muvaffaqiyatli
# tasdiqlanganidan so'ng amalga oshiriladi.


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel):
    current_user = session.query(User).filter(User.username == user.username).first()  # identifikatsiya
    if current_user is not None:
        if check_password_hash(current_user.password, user.password):
            subject = {'username': current_user.username}
            access_token = access_security.create_access_token(subject=subject)
            refresh_token = access_security.create_refresh_token(subject=subject)
            data = {
                'ok': True,
                'message': 'Login successfull',
                'access': access_token,
                'refresh': refresh_token,
            }
            return data
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Username or password invalid')


@auth_router.get('/profile')
async def read_current_user(credentials: JwtAuthorizationCredentials = Security(access_security)):
    return credentials
