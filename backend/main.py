import uvicorn
from fastapi import FastAPI,HTTPException
from fastapi.exceptions import RequestValidationError
from .settings import TORTOISE_ORM,ALLOWHOSTS
from tortoise.contrib.fastapi import register_tortoise
from API import permissions,role,user,relation,login,scope_auth_test
from tortoise.exceptions import OperationalError, DoesNotExist, IntegrityError, ValidationError
from utils import exception
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


#router
app.include_router(user.router, prefix='/user', tags=['用户API'])
app.include_router(role.router, prefix='/role', tags=['角色API'])
app.include_router(permissions.router, prefix='/permissions', tags=['权限API'])
app.include_router(relation.router,prefix='/user',tags=['关系API'])
app.include_router(login.router,prefix='/login',tags=['登录'])
app.include_router(scope_auth_test.router,prefix='/test',tags=['权限测试'])


# exception_handing
app.add_exception_handler(HTTPException, exception.http_error_handler)
app.add_exception_handler(RequestValidationError, exception.http422_error_handler)
app.add_exception_handler(exception.UnicornException, exception.unicorn_exception_handler)
app.add_exception_handler(DoesNotExist, exception.mysql_does_not_exist)
app.add_exception_handler(IntegrityError, exception.mysql_integrity_error)
app.add_exception_handler(ValidationError, exception.mysql_validation_error)
app.add_exception_handler(OperationalError, exception.mysql_operational_error)


#db
register_tortoise(
    app=app,
    config=TORTOISE_ORM
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWHOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, workers=1)
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, workers=1)



