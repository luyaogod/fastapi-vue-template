from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,APIRouter
from schemas.schemas import Token,UserOut
from utils.jwt import create_access_token,util_validate_user
from utils.deserialize import util_list_queryset_validate_dump
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import schemas



router = APIRouter()
@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    print(form_data.username)
    print(form_data.password)
    user = await util_validate_user(form_data.username,form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #neederrorhandle
    user_data =  UserOut(**dict(user)).model_dump()
    result = await user.role.all().values()
    data_list = util_list_queryset_validate_dump(result, schemas.RoleIn)
    data_list_out = []
    for i in data_list:
        data_list_out.append(i["role_name"])
    user_data['role'] = data_list_out
    print(user_data)
    access_token = create_access_token(
        data= user_data,expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")