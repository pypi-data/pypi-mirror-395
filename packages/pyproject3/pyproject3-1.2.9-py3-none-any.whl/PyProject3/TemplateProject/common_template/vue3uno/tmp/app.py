"""FastAPI Mock 后端 - 对接前端用户管理功能"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(title="Vue3 CMS Mock API", version="1.0.0")

# 配置 CORS，允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 数据模型 ====================


class User(BaseModel):
    id: int
    username: str
    email: str
    role: str  # 'admin' | 'user'
    status: str  # 'active' | 'inactive'
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "user"
    status: Optional[str] = "active"


class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None


class GetUserInfoRequest(BaseModel):
    username: str
    token: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: dict


class BatchDeleteRequest(BaseModel):
    ids: List[int]


class hajimiParams(BaseModel):
    id: int
    hajimi_name: str = ""
    hajimi_age: int = 0
    hajimi_breed: str = ""
    hajimi_color: str = ""
    hajimi_gender: str = ""
    hajimi_weight: int = 0
    hajimi_height: int = 0
    hajimi_health: str = ""
    hajimi_vaccination: str = ""
    hajimi_vaccination_date: str = ""
    hajimi_vaccination_place: str = ""
    hajimi_photo: str = ""


class hajimiResponse(BaseModel):
    code: int
    message: str
    data: hajimiParams

# ==================== Mock 数据存储 ====================


# 内存中的用户数据（实际项目中应该使用数据库）
mock_users = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "status": "active",
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T10:00:00",
    },
    {
        "id": 2,
        "username": "user1",
        "email": "user1@example.com",
        "role": "user",
        "status": "active",
        "created_at": "2024-01-02T11:00:00",
        "updated_at": "2024-01-02T11:00:00",
    },
    {
        "id": 3,
        "username": "user2",
        "email": "user2@example.com",
        "role": "user",
        "status": "inactive",
        "created_at": "2024-01-03T12:00:00",
        "updated_at": "2024-01-03T12:00:00",
    },
]

# 用户密码存储（实际项目中应该加密存储）
user_passwords = {
    1: "admin123",
    2: "user123",
    3: "user123",
}

# 下一个用户 ID
next_user_id = 4

# ==================== 工具函数 ====================


def get_current_time():
    """获取当前时间字符串"""
    return datetime.now().isoformat()


def find_user_by_id(user_id: int):
    """根据 ID 查找用户"""
    for user in mock_users:
        if user["id"] == user_id:
            return user
    return None


def get_next_user_id():
    """获取下一个用户 ID"""
    global next_user_id
    current_id = next_user_id
    next_user_id += 1
    return current_id

# ==================== 狗狗管理 API ====================


@app.get("/hajimi/info")
def get_hajimi_info():
    """获取狗狗信息"""
    hajimi_info = {
        "id": 1,
        "hajimi_name": "旺财",
        "hajimi_age": 3,
        "hajimi_breed": "金毛",
        "hajimi_color": "金色",
        "hajimi_gender": "公",
        "hajimi_weight": 30,
        "hajimi_height": 100,
        "hajimi_health": "健康",
        "hajimi_vaccination": "是",
        "hajimi_vaccination_date": "2025-01-01",
        "hajimi_vaccination_place": "宠物医院",
        "hajimi_photo": "https://picsum.photos/200/300",
    }
    return {
        "code": 200,
        "message": "获取狗狗信息成功",
        "data": hajimi_info,
    }


@app.post("/hajimi/info")
def update_hajimi_info(hajimi_info: hajimiParams):
    """更新狗狗信息"""
    print(hajimi_info)
    hajimi_info.hajimi_name = "旺财哈哈哈哈"

    return {
        "code": 200,
        "message": "更新狗狗信息成功",
        "data": hajimi_info,
    }
# ==================== 用户管理 API ====================


@app.get("/users")
def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    username: Optional[str] = Query(None, description="用户名搜索"),
    email: Optional[str] = Query(None, description="邮箱搜索"),
    status: Optional[str] = Query(None, description="状态筛选"),
):
    """获取用户列表（支持分页和搜索）"""
    # 过滤用户
    filtered_users = mock_users.copy()

    if username:
        filtered_users = [
            u for u in filtered_users if username.lower() in u["username"].lower()]

    if email:
        filtered_users = [
            u for u in filtered_users if email.lower() in u["email"].lower()]

    if status:
        filtered_users = [u for u in filtered_users if u["status"] == status]

    # 分页
    total = len(filtered_users)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_users = filtered_users[start:end]

    return {
        "items": paginated_users,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """获取用户详情"""
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@app.post("/users")
def create_user(user_data: CreateUserRequest):
    """创建用户"""
    # 检查用户名是否已存在
    if any(u["username"] == user_data.username for u in mock_users):
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 检查邮箱是否已存在
    if any(u["email"] == user_data.email for u in mock_users):
        raise HTTPException(status_code=400, detail="邮箱已存在")

    # 创建新用户
    new_user = {
        "id": get_next_user_id(),
        "username": user_data.username,
        "email": user_data.email,
        "role": user_data.role or "user",
        "status": user_data.status or "active",
        "created_at": get_current_time(),
        "updated_at": get_current_time(),
    }

    mock_users.append(new_user)
    user_passwords[new_user["id"]] = user_data.password

    return new_user


@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: UpdateUserRequest):
    """更新用户"""
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 检查用户名是否已被其他用户使用
    if user_data.username and user_data.username != user["username"]:
        if any(u["username"] == user_data.username and u["id"] != user_id for u in mock_users):
            raise HTTPException(status_code=400, detail="用户名已存在")

    # 检查邮箱是否已被其他用户使用
    if user_data.email and user_data.email != user["email"]:
        if any(u["email"] == user_data.email and u["id"] != user_id for u in mock_users):
            raise HTTPException(status_code=400, detail="邮箱已存在")

    # 更新用户信息
    if user_data.username:
        user["username"] = user_data.username
    if user_data.email:
        user["email"] = user_data.email
    if user_data.role:
        user["role"] = user_data.role
    if user_data.status:
        user["status"] = user_data.status
    if user_data.password:
        user_passwords[user_id] = user_data.password

    user["updated_at"] = get_current_time()

    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """删除用户"""
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    mock_users.remove(user)
    if user_id in user_passwords:
        del user_passwords[user_id]

    return {"message": "用户删除成功"}


@app.delete("/users/batch")
def batch_delete_users(request: BatchDeleteRequest):
    """批量删除用户"""
    deleted_count = 0
    for user_id in request.ids:
        user = find_user_by_id(user_id)
        if user:
            mock_users.remove(user)
            if user_id in user_passwords:
                del user_passwords[user_id]
            deleted_count += 1

    return {"message": f"成功删除 {deleted_count} 个用户", "deleted_count": deleted_count}

# ==================== 认证 API ====================


@app.post("/auth/login")
def login(login_data: LoginRequest):
    """用户登录"""
    # 查找用户
    user = None
    for u in mock_users:
        if u["username"] == login_data.username:
            user = u
            break

    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 验证密码（实际项目中应该使用加密密码）
    if user["id"] not in user_passwords or user_passwords[user["id"]] != login_data.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 生成 token（实际项目中应该使用 JWT）
    token = f"mock_token_{user['id']}_{datetime.now().timestamp()}"

    # 保存 token 到用户对象中，用于后续验证
    user["token"] = token

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
        },
    }


@app.post("/auth/logout")
def logout():
    """用户登出"""
    return {"message": "登出成功"}


@app.post("/auth/me")
def get_current_user(request: GetUserInfoRequest):
    """获取当前用户信息。通过POST body传入username和token，查询用户信息  

    Args:
        request: 包含username和token的请求体
    Returns:
        User: 用户信息
    """

    for user in mock_users:
        if user["username"] == request.username and user.get("token") == request.token:
            # 返回用户信息（不包含token和password）
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "status": user.get("status", "active"),
                "created_at": user.get("created_at"),
            }
    raise HTTPException(status_code=404, detail="用户不存在")


# ==================== 健康检查 ====================
@app.get("/")
def index():
    """根路径"""
    return {"message": "Vue3 CMS Mock API", "version": "1.0.0"}


@app.get("/ping")
def ping():
    """健康检查"""
    return {"message": "pong"}

# ==================== 启动服务 ====================


if __name__ == "__main__":
    PORT = 8001
    print("=" * 50)
    print("Vue3 CMS Mock API 启动中...")
    print("API 文档地址: http://127.0.0.1:%s/docs" % PORT)
    print("API 地址: http://127.0.0.1:%s" % PORT)
    print("=" * 50)

    try:
        # 使用 import string 以支持 reload（避免警告）
        # log_level="debug" 可以显示更详细的日志
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=PORT,
            reload=True,
            log_level="info",  # 可选: "debug", "info", "warning", "error"
        )
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"\n启动失败: {e}")
        import traceback
        traceback.print_exc()
