from pydantic import BaseModel,Field
from typing import List,Union,Optional

class UserBase(BaseModel):
    user_name:str = Field(description='用户名',min_length=3,max_length=20)



class UserIn(UserBase):
    password:str = Field(description='密码',min_length=6)
    super_admin:Optional[bool] = Field(default=False,description="false为普通用户,true为超级管理员")


class UserOut(UserBase):
    id:int = Field(description='pk')
    user_status:Optional[int] = None
    super_admin:Optional[bool] = None


class RoleIn(BaseModel):
    role_name:str = Field(description='用户名')


class RoleOut(RoleIn):
    id:int = Field(description='pk')


class RoleOutWithPermission(RoleOut):
    permission:List


class RoleInWithPermission(BaseModel):
    role_name:Optional[str]
    permission_id: Optional[List[int]] = Field(default=[])


class RoleInWithPermissionForPut(BaseModel):
    role_name:Optional[str] = Field(default="")
    permission_id:Optional[List[int]]


class PermissionIn(BaseModel):
    scope:str = Field(description='用户名')


class PermissionOut(PermissionIn):
    id:int = Field(description='pk')


class RelationRolePermissionIn(BaseModel):
    role_id:int
    permission_id:List[int]


class RelationUserRoleIn(BaseModel):
    user_id:int
    role_id:List[int]


#token
class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: list[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str

