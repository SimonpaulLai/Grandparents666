from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/test")
async def receive_json(request: Request):
    data = await request.json()  # 取得 JSON 請求內容
    print("收到的 JSON 資料：", data)  # 印在後台，方便 debug

    return JSONResponse(content={"status": "received", "data": data})
