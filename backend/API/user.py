from fastapi import APIRouter
from models.models import User
from schemas import schemas
from fastapi import HTTPException,status
from utils.deserialize import util_list_queryset_validate_dump
from utils.jwt import util_get_password_hash


router = APIRouter()


@router.post('',summary='创建用户(用户注册)')
async def create_user(data:schemas.UserIn):
    data.password = util_get_password_hash(data.password)
    result = await User.create(**data.model_dump())
    return dict(result)


@router.get('',summary='获取所有用户')
async def get_all_user():
    result = await User.all().values()
    data_list =  util_list_queryset_validate_dump(result,schemas.UserOut)
    return data_list


@router.delete('/{user_id}',summary='删除用户')
async def delete_user(user_id):
    result =  await User.get_or_none(pk = user_id)
    if result:
        await result.delete()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='查无此用户')


