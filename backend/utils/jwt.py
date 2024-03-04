from passlib.context import CryptContext
from typing import Union
from jose import  jwt
from datetime import datetime, timedelta, timezone
from fastapi import  HTTPException
from settings import SECRET_KEY,ALGORITHM
from models.models import User




#hashtools-------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#hash校验工具
def util_verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


#hash创建工具
def util_get_password_hash(password):
    return pwd_context.hash(password)

async def  util_validate_user(username,password):
    user = await User.get_or_none(user_name = username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not util_verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user

#jwt_token_maker-------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

