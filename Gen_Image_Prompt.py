from GPT_api_client import call_chat_api

def generate_image_prompt(user_input: str, diary_text: str, mode: str = "fast") -> str:
    """
    根據使用者描述與日記內容，生成代表性的英文圖片描述。

    規則：
    - 聚焦於 user_input，避免虛構內容
    - 圖像畫面應簡單、有代表性
    - 使用 general 描述（如 an elderly man），不要出現真名
    - 僅輸出英文圖片 prompt，不加說明文字

    回傳範例：
    - "An elderly man walking with a cane in the rain, soft blurry hospital in background"
    """

    system_prompt = {
        "role": "system",
        "content": (
            "你是一位圖片生成助手，專門協助從長輩日記中，提取一個**簡單、代表性的畫面**來製作圖片。\n"
            "規則如下：\n"
            "1. 請以 `user_input`（原始描述）為核心資訊，避免加入幻覺內容。\n"
            "2. 圖片畫面請盡量簡單，例如：\n"
            "   - 醫院場景：可以只出現背影與醫院指標（醫院建築模糊當背景）\n"
            "   - 吃飯：手拿著餐點、在桌上（不用出現整個人）\n"
            "   - 活動：只拍某個特定動作（唱歌的麥克風、跳舞的手腳）\n"
            "3. 請輸出為一段簡短的英文描述，格式適合拿去做圖，例如：\n"
            "   - 'An elderly man walking with a cane in the rain, soft blurry hospital in background'\n"
            "   - 'A hand holding a bowl of noodles on a wooden table, anime style'\n"
            "   - 'An elderly man singing with a microphone on stage, colorful lighting'\n"
            "4. 不要描述具體長輩姓名，只用 general terms like 'an elderly man/woman'\n"
            "5. 最後請**只輸出英文 prompt 本身**，不要說明文字或其他語句。"
        )
    }

    messages = [
        system_prompt,
        {
            "role": "user",
            "content": f"原始描述（user_input）:\n{user_input.strip()}\n\n日記內容:\n{diary_text.strip()}"
        }
    ]

    return call_chat_api(messages=messages, max_tokens=150, mode=mode).strip()
