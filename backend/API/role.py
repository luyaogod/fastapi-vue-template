from fastapi import APIRouter
from models.models import Role,Permission
from schemas import schemas
from fastapi import HTTPException,status
from utils.deserialize import util_list_queryset_validate_dump
from typing import List


router = APIRouter()


@router.post('',summary='创建角色')
async def create_role(data:schemas.RoleIn):
    result = await Role.create(**data.model_dump())
    return dict(result)


@router.post('/role_with_permission',summary='创建角色，可同时绑定权限')
async def create_role(data:schemas.RoleInWithPermission):
    new_role = await Role.create(**data.model_dump())
    print(new_role.pk)
    if data.permission_id !=[]:
        permissions = await Permission.filter(id__in=data.permission_id)
        await new_role.permission.add(*permissions)
        #return待处理
        return '创建成功，并绑定权限'
    else:
        return dict(new_role)


@router.post('/role_with_permission/{role_id}',summary='更新角色及权限')
async def create_or_put_role_with_permission(role_id:int,data:schemas.RoleInWithPermissionForPut):
    role = await Role.get_or_none(pk=role_id).prefetch_related('permission')
    if data.role_name != "":
        role.role_name = data.role_name
    else:
        pass
    if role:
        await role.permission.clear()
        permissions = await Permission.filter(id__in=data.permission_id)
        await role.permission.add(*permissions)
        await role.save()
        #return待处理
        return '更新成功'
    else:
        return '查无此角色'



@router.get('',summary='获取所有角色')
async def get_all_role():
    result = await Role.all().values()
    data_list = util_list_queryset_validate_dump(result,schemas.RoleOut)
    return data_list


@router.delete('/{role_id}',summary='删除角色')
async def delete_role(role_id):
    result =  await Role.get_or_none(pk = role_id)
    if result:
        await result.delete()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='查无此角色')