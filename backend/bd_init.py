from tortoise import Tortoise, run_async
from settings import TORTOISE_ORM
from models import  models
from tortoise.exceptions import OperationalError

async def insert_permission():
    permissions = [
        {"scope": "scope_test_1"},
        {"scope": "scope_test_2"},
        {"scope": "scope_test_3"},
    ]
    for i in permissions:
        await models.Permission.create(**i)

async def insert_role():
    roles = [
        {"role_name":"role_test_1","permission":[1,2]},
        {"role_name": "role_test_2", "permission": [1, 3]},
        {"role_name": "role_test_3", "permission": [2, 3]},
    ]
    for i in  roles:
        role =  await models.Role.create(role_name=i['role_name'])
        permissions = await models.Permission.filter(id__in = i["permission"])
        await role.permission.add(*permissions)

async def insert_user():
    #password > 123456
    users = [
        # {"user_name":"admin","password":"$2b$12$QLIGQfKvrU24q4NbZIEgnu2EwdoWkAwSNOqqnC/kOOFy34Bfwyd1m","user_status":1,"super_admin":True,"role":[]},
        {"user_name": "userone", "password": "$2b$12$UH2HEyXn.JjGdQlX3rDf0OXTdRhZE9CpxWJzoiYStT/RSpqQx6lZ2", "user_status": 1,"role":[1,2]},
        {"user_name": "usertwo", "password": "$2b$12$hPyePcHasK.g.qIhNYk4feyM/J3xogDtT/xQMwBL8Gt5IFA1JZyq2", "user_status": 1, "role": [2]},
        {"user_name": "useruser", "password": "$2b$12$R3nqgFr6I4u51Aa3b8aAYOWJ2wdtLRU4amfUnC3krGecf5B.o8PZu", "user_status": 1, "role": []},
    ]
    for i in users:
        i_copy = i.copy()
        del i_copy["role"]

        user = await models.User.create(**i_copy)
        if i["role"]:
            roles = await  models.Role.filter(id__in=i["role"])
            await user.role.add(*roles)
        else:
            pass


async def main():
    await Tortoise.init(
        config=TORTOISE_ORM
    )

    try:
        user =  await models.User.get_or_none(pk = 1)
        print('- 已初始化')
    except OperationalError as e:
        print('- 未初始化')
        await Tortoise.generate_schemas()

        await insert_permission()
        await insert_role()
        await insert_user()
    
        await Tortoise.close_connections()
        print('- 初始化完成')
        
if __name__ == "__main__":
    run_async(main())

