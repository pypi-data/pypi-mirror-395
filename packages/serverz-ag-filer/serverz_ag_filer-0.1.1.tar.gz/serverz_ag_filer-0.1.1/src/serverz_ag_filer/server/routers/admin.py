
# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import FastAPI, HTTPException, Header


# 模拟获取当前用户的依赖项
async def get_current_user(x_token: str = Header(...)):
    if x_token != "valid-secret-token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid X-Token header")
    return {"username": "admin", "roles": ["user", "admin"]}

# 模拟一个管理员权限检查的依赖项
async def verify_admin_role(user: dict = Depends(get_current_user)):
    if "admin" not in user.get("roles", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user


router = APIRouter(
    tags=["Admin"],
    dependencies=[Depends(get_current_user), Depends(verify_admin_role)] # 统一的依赖项列表
)



@router.get("/dashboard/")
async def get_admin_dashboard_data(user):
    # 这个函数会自动接收到 get_current_user 和 verify_admin_role 的结果（如果需要）
    # 但我们在这里不需要显式接收它们，因为它们只是做权限检查
    print(user,'user')
    return {"message": "Welcome to the admin dashboard!"}

@router.post("/settings/")
async def update_admin_settings(settings: dict):
    # 这个函数也会自动执行 get_current_user 和 verify_admin_role
    return {"message": "Admin settings updated", "settings": settings}

# 这个API也需要认证和管理员权限
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted by admin."}
