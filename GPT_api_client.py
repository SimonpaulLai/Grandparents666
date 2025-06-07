import os
import requests
import streamlit as st
from dotenv import load_dotenv

# 載入 .env（本地測試用），雲端部署時會自動用 st.secrets
load_dotenv()

# 優先使用 st.secrets，其次用 os.environ（方便本地與雲端都能跑）
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
print(api_key)
if api_key is None:
    raise ValueError("❌ 請先設定環境變數 OPENAI_API_KEY")


def call_chat_api(messages, max_tokens=None, mode="simple"):
    """
    傳送 ChatGPT 請求並回傳回應文字。
    
    參數：
    - messages: list，ChatGPT 訊息格式
    - max_tokens: int，控制輸出長度（預設不限）
    - mode: str，'simple' 僅回傳文字，'debug' 顯示詳細資訊

    回傳：
    - str：GPT 回應文字（若失敗則為 None）
    """

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",  # 若你用的是 Plus 可改 gpt-4o，免費方案請用 gpt-3.5-turbo
        "temperature": 1.0,
        "messages": messages
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    if mode == "debug":
        st.subheader("📤 Request Info")
        st.json({
            "url": url,
            "headers": {k: ("***" if k == "Authorization" else v) for k, v in headers.items()},
            "data": data
        })

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        res_json = response.json()

        if mode == "debug":
            st.subheader("📥 Response JSON")
            st.json(res_json)

        try:
            content = res_json["choices"][0]["message"]["content"]
            if mode == "debug":
                st.success("✨ AI 回應內容")
                st.markdown(content.strip())
            return content.strip()
        except Exception as e:
            st.error(f"⚠️ 回應解析失敗：{e}")
            return None

    else:
        st.error(f"❌ 請求失敗：{response.status_code}")
        st.text(response.text)
        return None


# ⚙️ 測試用（僅限本地 CLI 環境，不適用 Streamlit）
if __name__ == "__main__":
    res = call_chat_api(
        messages=[{"role": "user", "content": "Hello from Streamlit version"}],
        mode="debug"
    )
    print("簡化回傳:", res)
