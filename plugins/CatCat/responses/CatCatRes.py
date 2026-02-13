from ..utils.api_utils import call_free_chatgpt_api

def format_group_chat(messages):
    """
    将原始群聊记录转换为 API 接受的格式
    输入示例：
        [
            166658.6419105 manager(10101): init jisang
            166658.6430702 何山(7894652): @鸡桑 你是谁,
        ]
    """
    formatted_messages = ""
    for message in messages:
        formatted_messages += f"{' '.join(message.split()[1:])}\n"
    # print(formatted_messages)
    return [{"role": "user", "content": formatted_messages}]


async def cat_cat_response(api_key, chat_history, prompt):
    messages = [
        {"role": "system", "content": prompt},
        *format_group_chat(chat_history),
        {"role": "user", "content": "请直接用自然中文回复，不要输出JSON/代码块/前缀/解释，只输出正文。"}
    ]
    response = await call_free_chatgpt_api(messages, api_key=api_key)
    return response.strip('"') if response else ""
