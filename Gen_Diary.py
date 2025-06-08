from GPT_api_client import call_chat_api

# 長輩資料
resident_profile = {
    "name": "阿水伯",
    "gender": "男性",
    "age": 87,
    "nickname": "阿水伯",
    "personality": ["健談", "喜歡聊天", "對人很客氣"],
    "health_status": "身體偏瘦但精神不錯，行動需拐杖輔助。",
    "interests": ["唱歌", "看報紙", "早上散步"],
    "family_relation": {
        "name": "阿嬌姐",
        "relation": "女兒"
    }
}

# 機構資料
facility_profile = {
    "name": "清福養老院",
    "location": "新北市三峽區",
    "description": "位於三峽郊區、三峽河附近、空氣清新，建築為十層樓大樓，空間大，像醫院結合旅館，氣氛溫馨。",
    "layout": {
        "floors": 10,
        "areas": ["溫馨花園", "大廳", "表演廳", "電影院", "醫院", "交誼廳", "復健室", "餐廳", "多功能活動室"]
    },
    "room_types": ["雙人房", "四人房", "靠窗房型"],
    "daily_routine_hint": "早上會巡房，中午前後用餐，下午有活動，傍晚可以散步"
}

# 工作人員
staff_profiles = [
    {
        "name": "小芳",
        "role": "社工師",
        "description": "每天幫忙策劃、帶活動，善於活躍氣氛、關心長輩心理健康，個性活潑。",
        "language_style": "台語混中文，有親切感"
    },
    {
        "name": "阿豪",
        "role": "護理師",
        "description": "來自印尼，中文學習中，年輕但很有耐心，會仔細幫長輩量血壓、問候狀況。"
    }
]

# 體徵參考
vitals_reference = {
    "temperature": {
        "normal": "36.5 ± 0.3",
        "high": "37.5 以上",
        "low": "35.5 以下",
        "note": "80歲以上長者若無明顯臨床症狀，收縮壓控制目標可小於150 mmHg。"
    },
    "pulse": {
        "normal": "60-80",
        "note": "偏高可能為活動後，偏低需觀察精神狀況"
    },
    "blood_pressure": {
        "normal": "120/80 附近",
        "high": "收縮壓 > 140",
        "low": "收縮壓 < 100"
    }
}

# 角色人設
persona = {
    "name": "里長伯",
    "age_range": "50-60",
    "style": "國台語混用、親切、實在、愛講重點、生活化",
    "catchphrases": ["啊", "嘿", "誒", "吼", "唉呀", "咱"],
    "description": "在地里長，熱心助人，每天關心長輩狀況，常和家屬聊天報告生活點滴。",
    "sample_speech": "啊今天天氣不錯誒，你們家阿水伯吼，今仔日看起來精神真好嘿～"
}

# 天氣詞彙
weather_descriptions = {
    "晴天": "太陽露臉，整間院內都暖洋洋的誒",
    "陰天": "今仔日天色灰灰的，不過也沒落雨啦",
    "下雨": "滴滴答答落雨，咱中庭稍微濕濕的",
    "寒冷": "冷颼颼的，阿水伯今天穿了兩件外套",
    "炎熱": "吼～熱吱吱誒，大家都躲在陰影底下乘涼"
}

def generate_diary(user_input: str, mode: str = "debug") -> str:
    system_background = f"""
    長輩基本資料如下：
    {resident_profile}

    療養院環境如下：
    {facility_profile}

    里長伯角色描述如下：
    {persona}

    其他參考資料如下：
    - 工作人員：{staff_profiles}
    - 體徵參考：{vitals_reference}
    - 天氣描述：{weather_descriptions}
    """

    # 對話訊息
    messages = [
        {
            "role": "system",
            "content": (
                f"{system_background}\n\n"
                "你是一位住在在地養老院的『里長伯』，平常會幫忙觀察長輩的生活，"
                "然後用親切、自然的方式寫成回報日記，像是要講給家屬聽一樣。"
                "請使用你熟悉的語氣（國台語混用），注意長輩的身體狀況、情緒、活動。"
                "請依據提供的資訊，寫一篇短日記，不要虛構資料、不要寫太長，控制在150字內。"
            )
        },
        {
            "role": "user",
            "content": (
                f"{user_input}"
         )
        }
    ]
    return call_chat_api(messages=messages, mode='simple').strip()

