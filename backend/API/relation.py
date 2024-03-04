from fastapi import APIRouter
from models.models import Role,Permission,User
from schemas import schemas
from utils.deserialize import util_list_queryset_validate_dump
from tortoise.query_utils import Prefetch



router = APIRouter()

#role_permissions--------------------------------------------------------------
@router.post('/role_permission',summary='角色绑定权限')
async def create_role_permission(data:schemas.RelationRolePermissionIn):
    role = await Role.get_or_none(pk = data.role_id)
    await role.permission.clear()
    permissions = await Permission.filter(id__in= data.permission_id)
    await role.permission.add(*permissions)
    return 'CreateRolePermission'


@router.get('/role_permission/{role_id}',summary='查询角色所有权限')
async def get_all_role_permissions(role_id:int):
    role = await Role.get_or_none(pk = role_id)
    result =  await role.permission.all().values()
    data_list = util_list_queryset_validate_dump(result,schemas.PermissionOut)
    return (data_list)


@router.delete('/role_permission/clear/{role_id}',summary='清空角色权限')
async def clear_role_permissions(role_id:int):
    role = await Role.get_or_none(pk = role_id)
    await role.permission.clear()
    return "ClearRolePermission"
#------------------------------------------------------------------------------


#user_roles--------------------------------------------------------------------
@router.post('/user_role',summary='用户绑定角色')
async def createUserRole(data:schemas.RelationUserRoleIn):
    user = await User.get_or_none(pk = data.user_id)
    await user.role.clear()
    role = await Role.filter(id__in= data.role_id)
    await user.role.add(*role)
    return 'CreateUserRole'


@router.get('/user_role/{role_id}',summary='查询用户所有角色')
async def getAllUserRole(user_id:int):
    user = await User.get_or_none(pk = user_id)
    result =  await user.role.all().values()
    data_list = util_list_queryset_validate_dump(result,schemas.RoleOut)
    return (data_list)


@router.delete('/user_role/clear/{role_id}',summary='清空用户所有角色')
async def clearUserRole(role_id:int):
    user = await User.get_or_none(pk = role_id)
    await user.role.clear()
    return "ClearRolePermission"
#------------------------------------------------------------------------------
@router.get('/user_permission/{user_id}',summary='查询用户所有权限')
async def getAllUserRole(user_id:int):
    data = await Permission.filter(role__user__id=user_id).all().values_list()
    return data

@router.get('/all_role_permissions',summary='查询所有角色和其对应的权限')
async def getAllRolePermission():
    roles = await Role.all().prefetch_related("permission")
    rep_data = []
    for role in roles:
        role_dict = dict(role)
        role_dict['permission'] = [schemas.PermissionOut(**dict(permission)).model_dump() for permission in role.permission]
        role_dict_out = schemas.RoleOutWithPermission(**role_dict)
        rep_data.append(role_dict_out)
    return rep_data

