import os
from dotenv import load_dotenv
import replicate
from GPT_api_client import call_chat_api

load_dotenv()
api_key = os.getenv("REPLICATE_API_KEY")
if api_key is None:
    raise ValueError("請先設定環境變數 REPLICATE_API_KEY")
os.environ["REPLICATE_API_TOKEN"] = api_key

def generate_image_from_diary(diary_text: str, output_path: str = "output.png") -> str:
    prompt = (
        f"An elderly man named 阿水伯 in a nursing home, "
        f"{diary_text}, anime style, soft lighting, Studio Ghibli vibe, "
        "high detail, heartwarming atmosphere"
    )

    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={"prompt": prompt}
    )

    with open(output_path, "wb") as f:
        f.write(output[0].read())

    return output_path
