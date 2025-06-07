import streamlit as st
from Gen_Diary import generate_diary
from Gen_Emoji import generate_stamp
from Gen_Graph import generate_image_from_diary
from Gen_Image_Prompt import generate_image_prompt
from PIL import Image
import json

st.set_page_config(layout="wide")
st.title("📡 JSON API 接收")

# 接收 POST 資料
post_data = st.text_area("貼上 JSON 資料", height=300)

if st.button("處理資料"):
    try:
        data = json.loads(post_data)
        # 組合輸入資料
        user_input = f"今天{data['weather']}，{data['resident_name']}體溫{data['vitals']['體溫']}，脈搏{data['vitals']['脈搏']}，血壓{data['vitals']['血壓']}，" + \
                     "，".join(data['activities'])

        diary_text = generate_diary(user_input)
        stamp = generate_stamp(diary_text)
        image_prompt = generate_image_prompt(user_input, diary_text)
        image_path = generate_image_from_diary(image_prompt)

        with open(image_path, "rb") as img_file:
            encoded_image = img_file.read()

        result_json = {
            "diary": diary_text,
            "stamp": stamp,
            "graph": encoded_image.hex()  # 傳輸時通常使用 base64，但此處簡單示例用 hex
        }

        st.subheader("✅ 處理結果")
        st.json(result_json, expanded=True)

        st.image(Image.open(image_path), caption="Generated Image")

    except json.JSONDecodeError:
        st.error("JSON 格式錯誤，請重新檢查！")
