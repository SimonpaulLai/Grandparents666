from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Gen_Diary import generate_diary
from Gen_Emoji import generate_stamp
from Gen_Graph import generate_image_from_diary
from Gen_Image_Prompt import generate_image_prompt

app = FastAPI()

@app.post("/generate_diary")
async def generate_diary_endpoint(request: Request):
    data = await request.json()

    user_input = data.get('user_input', '')
    
    # 產生日記內容
    diary_text = generate_diary(user_input)

    # 產生貼圖
    stamp = generate_stamp(diary_text)

    # 產生圖片 prompt
    image_prompt = generate_image_prompt(user_input, diary_text)

    # 產生圖片 (儲存於 Render 的暫存資料夾)
    image_path = "/tmp/output.png"
    generate_image_from_diary(image_prompt, output_path=image_path)

    response_data = {
        "diary": diary_text,
        "stamp": stamp,
        "image_prompt": image_prompt
        # 若需要提供圖片下載，可額外實作 URL 提供功能
    }

    return JSONResponse(response_data)
