from fastapi import APIRouter,Request,Security
from dependencies import auth_dependence


router = APIRouter()


@router.get('/super_admin',summary='超级管理员权限测试',dependencies=[Security(auth_dependence)])
async def super_admin_test(request:Request):
    if  request.state.super_admin:
        return "超级管理员"
    return "普通用户"


@router.get('/scope_test',summary='scope权限测试',dependencies=[Security(auth_dependence,scopes=["use_test"])])
async def super_admin_test():
    return "权限通过"