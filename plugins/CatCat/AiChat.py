from ncatbot.utils.logger import get_log
from ncatbot.core.message import GroupMessage
import asyncio
import os
import aiofiles
import json
import re

from .responses.CatCatRes import cat_cat_response

_log = get_log()


async def gene_response(
    api_key,
    msg: GroupMessage,
    cat_prompt,
    bot_uin,
    force_reply_override: bool = False,
    bot_aliases: list = None,
):
    """生成 AI 回复"""
    history_file = f"plugins/CatCat/logs/{msg.group_id}_{msg.sender.user_id}_history.log"

    os.makedirs(os.path.dirname(history_file), exist_ok=True)

    # 读取历史
    try:
        async with aiofiles.open(history_file, "r", encoding="utf-8") as f:
            lines = await f.readlines()
    except FileNotFoundError:
        lines = []

    # 解析本条消息文本
    text_content = ""
    force_reply = bool(force_reply_override)

    for message in msg.message:
        _log.info(f"[DBG] seg={message!r}")
        if hasattr(message, "msg_seg_type"):
            if message.msg_seg_type == "text":
                text_content += getattr(message, "text", "")
            elif message.msg_seg_type == "at":
                qq = getattr(message, "qq", None)
                _log.info(f"[DBG] at.qq={qq!r} (type={type(qq)}), bot_uin={bot_uin!r} (type={type(bot_uin)})")
                if str(qq) == str(bot_uin):
                    force_reply = True
        elif isinstance(message, dict):
            if message.get("type") == "text":
                text_content += message.get("data", {}).get("text", "")
            elif message.get("type") == "at":
                qq = message.get("data", {}).get("qq")
                _log.info(f"[DBG] at.qq={qq!r} (type={type(qq)}), bot_uin={bot_uin!r} (type={type(bot_uin)})")
                if str(qq) == str(bot_uin):
                    force_reply = True


    if bot_aliases:
        # 去掉以“鸡桑/艾草鸡桑”等为开头的前缀（含可选空格/标点）
        import re
        alias_pattern = "|".join(re.escape(a) for a in bot_aliases)
        text_content = re.sub(rf"^\s*(?:{alias_pattern})[\s,，:：]*", "", text_content)
        # 去掉消息中 @鸡桑 / @艾草鸡桑 等
        text_content = re.sub(rf"@(?:{alias_pattern})\s*", "", text_content)

    text_content = f"{msg.sender.nickname}({msg.sender.user_id}): {text_content}"

    # 写入历史
    current_line = f"{asyncio.get_event_loop().time()} {text_content}\n"
    async with aiofiles.open(history_file, "a", encoding="utf-8") as f:
        await f.write(current_line)

    _log.info(f"[DBG] force_reply={force_reply}, text_content={text_content!r}")
    if not force_reply:
        return None


    # 倒序去重取最近 10 条聊天记录（包含当前消息）
    result = []
    for line in reversed(lines + [current_line]):
        if len(result) >= 10:
            break
        try:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            this_content = parts[2]
            if not any(this_content in content for content in result):
                result.append(line)
        except Exception:
            continue
    chat_history = reversed(result)

    _log.info("开始生成 AI 回复…")

    response = await cat_cat_response(api_key, chat_history, cat_prompt)

    if not response:
        return None

    # 彻底不解析 JSON：但会剥离夹杂的 JSON 片段，避免污染展示
    reply_text = response
    if "needReply" in reply_text or "need_reply" in reply_text:
        reply_text = re.sub(r"\{[\s\S]*?\}", "", reply_text).strip()

    if not reply_text:
        return "鸡桑在呢，你想聊点什么？"

    # 写入 AI 回复历史
    async with aiofiles.open(history_file, "a", encoding="utf-8") as f:
        safe_response = reply_text.replace("\n", "\\")
        await f.write(f"{asyncio.get_event_loop().time()} 鸡桑({bot_uin}): {safe_response}\n")

    return reply_text
