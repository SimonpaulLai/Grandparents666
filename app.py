import streamlit as st
from Gen_Diary import generate_diary
from Gen_Emoji import generate_stamp
from Gen_Graph import generate_image_from_diary
from Gen_Image_Prompt import generate_image_prompt
from PIL import Image

st.title("🌿 溫馨日記 App")

user_input = st.text_area("輸入今天的簡單描述：", "今天下雨，阿水伯血壓198/70，有去參加音樂課，下午心情好像不錯。")

if st.button("生成日記與圖片"):
    with st.spinner("正在生成中，請稍候..."):
        try:
            diary_text = generate_diary(user_input)
            stamp = generate_stamp(diary_text)
            image_prompt = generate_image_prompt(user_input, diary_text)    
            image_path = generate_image_from_diary(image_prompt)

            st.subheader("📘 日記內容")
            st.write(diary_text)

            st.subheader("🧩 代表貼圖")
            st.write(stamp)

            st.subheader("📷 圖片預覽")
            image = Image.open(image_path)
            st.image(image, caption="今日圖片")
        except Exception as e:
            st.error(f"⚠️ 發生錯誤：{e}")
