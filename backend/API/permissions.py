from fastapi import APIRouter,Security
from models.models import Permission
from schemas import schemas
from fastapi import HTTPException,status
from utils.deserialize import util_list_queryset_validate_dump


router = APIRouter()


@router.post('',summary='创建权限')
async def create_permission(data:schemas.PermissionIn):
    result = await Permission.create(**data.model_dump())
    return dict(result)


@router.get('',summary='获取所有权限')
async def get_all_permission():
    result = await Permission.all().values()
    data_list = util_list_queryset_validate_dump(result,schemas.PermissionOut)
    return data_list


@router.delete('/{permission_id}',summary='删除权限')
async def delete_permission(permission_id):
    result =  await Permission.get_or_none(pk = permission_id)
    if result:
        await result.delete()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='查无此权限')