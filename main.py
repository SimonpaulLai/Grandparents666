import streamlit as st
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
