import os
import requests
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("請先設定環境變數 OPENAI_API_KEY")


def call_chat_api(messages, max_tokens=None, mode="simple"):
    """
    傳送 ChatGPT 請求並回傳回應文字。
    
    參數：
    - messages: list，ChatGPT 訊息格式
    - max_tokens: int，控制輸出長度（預設不限）
    - mode: str，'simple' 僅回傳文字，'debug' 顯示簡單 debug 資訊

    回傳：
    - str：GPT 回應文字（若失敗則為 None）
    """

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4o-mini",
        "temperature": 1.0,
        "messages": messages
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    if mode == "debug":
        print("📤 發送請求內容：")
        print(data)

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        res_json = response.json()

        if mode == "debug":
            print("📥 回應 JSON：")
            print(res_json)

        return res_json["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"❌ 錯誤：{e}")
        return None


# 測試用（單獨執行時）
if __name__ == "__main__":
    response = call_chat_api(
        messages=[{"role": "user", "content": "Morning~"}],
        max_tokens=50,
        mode="debug"
    )
    print(f"簡化回傳：{response}")
