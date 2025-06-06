from GPT_api_client import call_chat_api

def generate_stamp(diary_text: str, mode: str = "simple") -> str:
    """
    根據日記內容，回傳代表這一天的 emoji 或數字。

    優先順序：
    1. 出門就醫：🏥、🚗、🚌 等
    2. 活動參與：🎤、🎂、🙏 等
    3. 情緒強烈：😆、😭、😡 等
    4. 其他情況：直接回傳日期數字（例如 '16'）

    回傳格式：
    - 僅回傳一個 emoji 或數字，不含說明或標點。
    """

    system_prompt = {
        "role": "system",
        "content": (
            "你是一個貼圖產生小幫手，根據每篇日記內容，挑選一個最適合代表這一天的貼圖。\n"
            "請依照以下優先順序選擇：\n"
            "1. 如果有去醫院、診所或任何外出，請挑選該地點代表性的貼圖（如🏥、🚗、🚌等）。\n"
            "2. 如果有活動，請挑選該活動代表性的貼圖（如🎂、🎤、🙏等）。\n"
            "3. 如果情緒有非常激烈的起伏，請挑選該情緒表情符號（如😆、😭、😡等）。\n"
            "4. 其他情況，請回傳該日的日期數字（如『16』）。\n\n"
            "請**只回覆一個 emoji 或數字，不要加任何說明文字、標點或其他語句**。"
        )
    }

    messages = [
        system_prompt,
        {"role": "user", "content": diary_text.strip()}
    ]

    return call_chat_api(messages=messages, mode=mode).strip()
