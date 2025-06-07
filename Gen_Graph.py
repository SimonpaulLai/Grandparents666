import os
import replicate
import requests
from dotenv import load_dotenv

# 載入 .env（若存在）
load_dotenv()

# 確保 REPLICATE_API_KEY 有設定
api_key = os.getenv("REPLICATE_API_KEY")
if not api_key:
    raise ValueError("請先在 .env 或 secrets.toml 中設定 REPLICATE_API_KEY")

# 設定 replicate token
os.environ["REPLICATE_API_TOKEN"] = api_key

def generate_image_from_diary(diary_text: str, output_path: str = "output.png") -> str:
    """
    根據日記內容，呼叫 Replicate API 生成圖片，儲存至本地，回傳檔案路徑。
    """
    prompt = (
        f"An elderly man in a nursing home, {diary_text}, "
        "anime style, soft lighting, Studio Ghibli vibe, "
        "high detail, heartwarming atmosphere"
    )

    try:
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": prompt}
        )

        # 通常 output[0] 是圖片 URL，下載它
        image_url = output[0]
        response = requests.get(image_url)

        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
        else:
            raise RuntimeError(f"圖片下載失敗，狀態碼：{response.status_code}")

    except Exception as e:
        print(f"[generate_image_from_diary] 發生錯誤：{e}")
        return None
