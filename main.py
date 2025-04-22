# main.py
# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from models import User
from database import engine, SessionLocal, init_db, Session
from sqlmodel import select
from typing import Optional

# 启动时创建表
init_db()

app = FastAPI()
SECRET_KEY = "your-secret-key"  # 生产环境需改为环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # 密码哈希 [[7]]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 数据库依赖
def get_db():
    with SessionLocal() as db:
        yield db


# 密码验证函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 用户验证
def authenticate_user(db, username: str, password: str):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


# 生成JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 登录接口
@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 受保护的测试接口
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": f"Hello {username}"}


# 登出接口（需配合前端清除token）
@app.post("/logout")
async def logout():
    # JWT无状态需前端主动删除token，可选实现黑名单机制 [[6]]
    return {"message": "Logout successful"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")  # 启用调试日志 [[5]]  # 启动 FastAPI
# 运行 FastAPI 应用
# uvicorn main:app --reload
