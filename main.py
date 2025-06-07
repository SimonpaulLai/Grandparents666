import os
from dotenv import load_dotenv
import streamlit as st
import openai

# ✅ 載入 .env（如果有）
load_dotenv()

# ✅ 嘗試讀取 Streamlit secrets 和環境變數
streamlit_key = None
try:
    streamlit_key = st.secrets.get("OPENAI_API_KEY")
except Exception:
    pass

env_key = os.getenv("OPENAI_API_KEY")
active_key = streamlit_key or env_key

# ✅ 驗證 API KEY 是否存在
if not active_key:
    st.error("❌ 找不到 OPENAI_API_KEY，請確認 .env 或 .streamlit/secrets.toml 已設定。")
    st.stop()

# ✅ 嘗試呼叫 OpenAI 進行測試連線
openai.api_key = active_key
try:
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "ping"}]
    )
except openai.error.AuthenticationError:
    st.error("❌ OpenAI API Key 無效，請確認你的 key 是否正確或已過期。")
    st.stop()
except openai.error.RateLimitError:
    st.warning("⚠️ OpenAI API 配額或速率限制超過，請稍後再試。")
    st.stop()
except Exception as e:
    st.error(f"❌ 發生未知錯誤：{str(e)}")
    st.stop()

# ✅ 如果 Key 通過驗證，才繼續載入主要模組
from Gen_Diary import generate_diary
from Gen_Emoji import generate_stamp
from Gen_Graph import generate_image_from_diary
from Gen_Image_Prompt import generate_image_prompt

st.set_page_config(page_title="🌿 溫馨日記 App", page_icon="📘")

st.title("📘 溫馨日記生成器")
user_input = st.text_area("請輸入今天的狀況：", height=150, placeholder="例如：今天下雨，阿水伯血壓198/70，有去參加音樂課...")

if st.button("生成日記"):
    if not user_input.strip():
        st.warning("請先輸入一些內容！")
    else:
        diary_text = generate_diary(user_input)
        st.success("✅ 日記生成成功！")
        st.markdown(f"**📘 日記內容：**\n\n{diary_text}")

        stamp = generate_stamp(diary_text)
        st.markdown(f"**🧩 今日代表貼圖：** {stamp}")

        prompt = generate_image_prompt(user_input, diary_text)
        st.markdown(f"**🎯 圖片描述：**\n\n`{prompt}`")

        with st.spinner("🎨 正在生成圖片，請稍候..."):
            image_path = generate_image_from_diary(prompt)
            if image_path:
                st.image(image_path, caption="🖼️ 代表畫面", use_column_width=True)
