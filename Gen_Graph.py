import os
import replicate
from GPT_api_client import call_chat_api

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

    print("🔍 Replicate 回傳內容：", output)

    if isinstance(output, list):
        for item in output:
            if isinstance(item, str) and item.startswith("http"):
                return item

    raise ValueError("無法取得圖片網址（replicate 回傳格式不符）")
