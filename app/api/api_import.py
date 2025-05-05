# 测试FastAPI接口间调用
import httpx
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

@app.get("/get_current_time")
async def get_current_time():
    """
    获取当前时间
    """
    return {"current_time": datetime.utcnow().isoformat()}

@app.post("/process_data")
async def process_data(data: dict):
    """
    处理数据并返回结果
    """
    # 调用另一个接口获取当前时间
    current_time_response = await get_current_time()
    current_time = current_time_response["current_time"]
    return {
        "processed_data": data,
        "current_time": current_time,
        "message": "Data processed successfully"
    }
    
@app.post("/import_data")
async def import_data(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post("http://localhost:8000/process_data", json=data)
            res.raise_for_status()  # 检查HTTP错误
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Failed to process data")
    
    return {
        "imported_data": res.json(),
        "message": "Data imported successfully"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_import:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)  # 启用调试日志 [[5]]  # 启动 FastAPI