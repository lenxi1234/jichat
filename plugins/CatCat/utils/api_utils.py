from ncatbot.utils.logger import get_log
import aiohttp
import json
import os
os.makedirs("plugins/CatCat/logs/free_api", exist_ok=True)

_log = get_log()

#FREE_CHATGPT_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
#FREE_CHATGPT_APIKEY = "sk-bf738eb69c5e4d17a0bdee420eb71e90"
#FREE_CHATGPT_MODEL = "qwen-flash-character"
FREE_CHATGPT_URL = "https://api.siliconflow.cn/v1/chat/completions"
FREE_CHATGPT_APIKEY = "sk-jdywgjxrnsbhaufvodxkavqzzumindeptwznbvpzyprthgcq"
FREE_CHATGPT_MODEL = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"

async def call_free_chatgpt_api(messages, api_key: str = None):
    key = api_key or FREE_CHATGPT_APIKEY
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    data = {
        "model": FREE_CHATGPT_MODEL,
        "messages": messages
    }

    try:
        async with aiohttp.ClientSession() as session:
            #（可选）记录请求调试日志
            with open("plugins/CatCat/logs/free_api/messages.log", "a", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.write("\n")

            async with session.post(FREE_CHATGPT_URL, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    # 返回第一个 choice 的内容
                    try:
                        return result["choices"][0]["message"]["content"]
                    except Exception as e:
                        _log.error(f"解析返回内容失败: {result}")
                else:
                    text = await response.text()
                    _log.error(f"免费 API 调用失败: {response.status}, {text}")
    except Exception as e:
        _log.error(f"请求免费 API 出错: {str(e)}")

    return ""
