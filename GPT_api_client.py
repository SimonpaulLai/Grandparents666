import os
import requests
from dotenv import load_dotenv
from rich import print
from rich.pretty import Pretty
from rich.panel import Panel

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("Render環境請設定 OPENAI_API_KEY")

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
        "model": "gpt-4o-mini",
        "store": False,
        "temperature": 1.0,
        "messages": messages
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    if mode == "debug":
        print(Panel.fit(Pretty({
            "url": url,
            "headers": headers,
            "data": data
        }), title="📤 Request Info"))

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        res_json = response.json()

        if mode == "debug":
            print(Panel.fit(Pretty(res_json), title="📥 Response JSON"))

        try:
            content = res_json["choices"][0]["message"]["content"]
            if mode == "debug":
                print(Panel.fit("文字回應：\n\n" + content.strip(), title="✨ AI 回應內容"))
            return content.strip()
        except Exception as e:
            print(f"[red]⚠️ 回應解析失敗：[bold]{e}[/bold][/red]")
            return None

    else:
        print(Panel.fit(f"{response.status_code}\n{response.text}", title="❌ 請求失敗"))
        return None


# 測試用（單獨執行時）
if __name__ == "__main__":
    response = call_chat_api(
        messages=[{"role": "user", "content": "Morning~"}],
        max_tokens=50,
        mode="debug"  # 或 "simple"
    )
    print(f"[bold green]簡化回傳（給外部用）:[/bold green] {response}")
