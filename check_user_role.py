from fastapi import Depends, HTTPException, status
from routers.auth import get_current_user
from pyd.base_models import UserBase

def require_admin(required_role: str):
    async def role_checker(current_user: UserBase = Depends(get_current_user)):
        if current_user.role.name != required_role: 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access restricted to {current_user.role.name} role"
            )
        return current_user
    return role_checker