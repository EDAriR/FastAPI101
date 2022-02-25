from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from User.user import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
from jose import jwt, JWTError

router = APIRouter(
    prefix="/oauth",
    tags=["oauth"],
    responses={404: {"description": "Not found"}}
)


class NewUser(BaseModel):
    username: str
    password: str


crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


def get_password_hash(password):
    return crypt_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/signup")
async def sign_up(newUser: NewUser):
    user = User(username=newUser.username,
                password=get_password_hash(newUser.password))
    user.save()
    return {"message": "Created user successfully!"}


# run the following on terminal to generate a secret key
# openssl rand -hex 32
SECRET_KEY = "3e8a3f31aab886f8793176988f8298c9265f84b8388c9fef93635b08951f379b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


def authenticate(username, password):
    try:
        user = get_user(username)
        password_check = verify_password(password, user['password'])
        return password_check
    except User.DoesNotExist:
        return False


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if authenticate(username, password):
        access_token = create_access_token(
            data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")


class TokenData(BaseModel):
    username: Optional[str] = None


def get_user(username: str):
    try:
        user = json.loads(User.objects.get(username=username).to_json())
        return user
    except User.DoesNotExist:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):

    print('get_current_user -----')

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.get("/detail")
async def user_detail(current_user: User = Depends(get_current_user)):
    return {"name": "Danny", "email": "danny@tutorialsbuddy.com"}
