from typing import Annotated
from pydantic import BaseModel, ValidationError
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer,SecurityScopes
from fastapi import Depends,  HTTPException, status,Request
from settings import SECRET_KEY,ALGORITHM
from models.models import User,Permission


#auth-------------------------------------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login/token",
    scopes={"me": ""},
)


class TokenData(BaseModel):
    user_id: int
    scopes: list[str] = []


async def auth_dependence(
request:Request,security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id :
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, user_id=user_id)
    except (JWTError,ValidationError):
        raise credentials_exception
    user = await User.get(pk = token_data.user_id)
    if user.user_status == 2:
        raise credentials_exception
    if not user:
        raise credentials_exception
    print(user.super_admin)
    if  security_scopes.scopes and not user.super_admin:
        is_pass = await Permission.filter(
            role__user__id=user_id, scope__in=set(security_scopes.scopes)).all()
        if not is_pass:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    request.state.user_id = user_id
    request.state.super_admin = user.super_admin


