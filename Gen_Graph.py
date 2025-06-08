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

    # 假設 output 是 list of image URLs
    if isinstance(output, list) and isinstance(output[0], str):
        return output[0]

    raise ValueError("無法取得圖片網址")
