from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Gen_Diary import generate_diary
from Gen_Emoji import generate_stamp
from Gen_Graph import generate_image_from_diary
from Gen_Image_Prompt import generate_image_prompt

app = FastAPI()

# 設定允許的來源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或改成 ["https://yourusername.github.io"] 比較安全
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_diary")
async def generate_diary_endpoint(request: Request):
    data = await request.json()

    user_input = data.get('user_input', '')

    # 產生日記內容
    diary_text = generate_diary(user_input+'若無提及，今天預設是6/9，天氣晴')

    # 產生貼圖
    stamp = generate_stamp(diary_text)

    # 產生圖片 prompt
    image_prompt = generate_image_prompt(user_input, diary_text)

    # 產生圖片（獲得圖片網址）
    image_base64 = generate_image_from_diary(image_prompt)

    response_data = {
        "diary": diary_text,
        "stamp": stamp,
        "image_base64": image_base64
    }

    return JSONResponse(response_data)
