import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/")
async def root(request: Request):
    data = await request.json()  # 获取事件数据
    print(data)
    return {}

if __name__ == "__main__":
    uvicorn.run(app, port=5700)