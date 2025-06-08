import os
import replicate
from GPT_api_client import call_chat_api
import base64

api_key = os.getenv("REPLICATE_API_KEY")
if api_key is None:
    raise ValueError("Render環境請設定 REPLICATE_API_KEY")
os.environ["REPLICATE_API_TOKEN"] = api_key

def generate_image_from_diary(diary_text: str, output_path: str = "/tmp/output.png") -> str:
    prompt = (
        f"An elderly man named 阿水伯 in a nursing home, "
        f"{diary_text}, anime style, soft lighting, Studio Ghibli vibe, "
        "high detail, heartwarming atmosphere"
    )

    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={"prompt": prompt}
    )

    # 取得第一個圖片 stream（FileOutput）
    file_like = output[0]

    # 讀取二進位圖片資料
    image_bytes = file_like.read()

    # 編碼成 base64 字串
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # 加上標頭，讓前端可以直接顯示
    data_url = f"data:image/png;base64,{image_base64}"

    return data_url
