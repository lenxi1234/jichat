from ncatbot.plugin import BasePlugin
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.plugin_system import group_only, private_only
from ncatbot.utils import ncatbot_config
from ncatbot.utils.logger import get_log

from .AiChat import gene_response
import asyncio
import os
import glob
import yaml

_log = get_log()

api_key = ""
cat_prompt = ""
super_user = ""
auto_reply_until = {}


class CatCat(BasePlugin):
    name = "CatCat"
    version = "1.0.4"

    @group_only
    async def handle_group_message(self, msg: GroupMessage):
        try:
            keywords = ["鸡桑"]
            bot_aliases = ["鸡桑"]
            raw = msg.raw_message or ""
            now = asyncio.get_event_loop().time()
            if raw == "鸡桑艾草" or raw == "@鸡桑" :
                # 交给主程序的固定话术处理，AI 不回复
                return
            if raw == "鸡桑":
                return
            has_keyword = any(k in raw.lower() if k.isascii() else k in raw for k in keywords)

            # 仍然支持 @ 触发（统一注册里 @ 过滤器不可用时，手动判断）
            def _is_at_bot(seg):
                if hasattr(seg, "msg_seg_type"):
                    return seg.msg_seg_type == "at" and str(getattr(seg, "qq", "")) == str(msg.self_id)
                if isinstance(seg, dict):
                    return seg.get("type") == "at" and str(seg.get("data", {}).get("qq")) == str(msg.self_id)
                return False

            at_bot = any(_is_at_bot(seg) for seg in msg.message)
            if not at_bot and raw:
                at_bot = any(f"@{name}" in raw for name in bot_aliases)

            user_key = f"{msg.group_id}:{msg.sender.user_id}"
            active_until = auto_reply_until.get(user_key, 0)
            auto_active = now <= active_until

            if not has_keyword and not at_bot and not auto_active:
                return

            _log.info(f"[DBG] on_group_message in, group={msg.group_id}, uin={msg.self_id}")
            _log.info(f"[DBG] raw_message={msg.raw_message!r}")
            _log.info(f"[DBG] message_segments={msg.message!r}")  # 看看at段长什么样

            if has_keyword or at_bot:
                auto_reply_until[user_key] = now + 20
            elif auto_active:
                # 自动回复模式中，只要该用户继续发言就续期
                auto_reply_until[user_key] = now + 20

            response = await gene_response(
                api_key,
                msg,
                cat_prompt,
                msg.self_id,
                force_reply_override=(has_keyword or at_bot or auto_active),
                bot_aliases=bot_aliases,
            )

            _log.info(f"[DBG] gene_response returned: {response[:80]!r}" if response else "[DBG] gene_response returned empty")
            if response:
                await self.api.post_group_msg(msg.group_id, text=response)
        except Exception:
            _log.exception("[DBG] on_group_message crashed")


    @private_only
    async def handle_private_message(self, msg: PrivateMessage):
        global cat_prompt
        is_manager = str(msg.user_id) == str(super_user)
        is_root = str(msg.user_id) == str(ncatbot_config.root)
        if not (is_manager or is_root):
            return
        if msg.raw_message == "prompt":
            await self.api.post_private_msg(msg.user_id, text=cat_prompt)
        elif msg.raw_message.startswith("set_prompt"):
            cat_prompt = msg.raw_message[10:]
            with open("plugins/CatCat/config/cat_prompt.txt", "w", encoding="utf-8") as f:
                f.write(cat_prompt.strip())
            await self.api.post_private_msg(msg.user_id, text="设置成功")
        elif msg.raw_message == "clear_log":
            log_path = "plugins/CatCat/logs/free_api/messages.log"
            try:
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write("")
                await self.api.post_private_msg(msg.user_id, text="messages.log 已清空")
            except Exception as e:
                await self.api.post_private_msg(msg.user_id, text=f"清空失败: {e}")
        elif msg.raw_message == "reload_prompt":
            try:
                with open("plugins/CatCat/config/cat_prompt.txt", "r", encoding="utf-8") as f:
                    cat_prompt = f.read()
                await self.api.post_private_msg(msg.user_id, text="prompt 已重新加载")
            except Exception as e:
                await self.api.post_private_msg(msg.user_id, text=f"重载失败: {e}")
        elif msg.raw_message == "clear_history_log":
            try:
                history_paths = glob.glob("plugins/CatCat/logs/*_history.log")
                for p in history_paths:
                    with open(p, "w", encoding="utf-8") as f:
                        f.write("")
                await self.api.post_private_msg(
                    msg.user_id, text=f"历史日志已清空，共 {len(history_paths)} 个文件"
                )
            except Exception as e:
                await self.api.post_private_msg(msg.user_id, text=f"清空失败: {e}")

    async def on_load(self):
        global api_key, super_user, cat_prompt
        with open("plugins/CatCat/config/config.yaml", "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            api_key = config_data["api_key"]
            super_user = config_data["manager_id"]

        with open("plugins/CatCat/config/cat_prompt.txt", "r", encoding="utf-8") as f:
            cat_prompt = f.read()

        _log.info(f"{self.name} 插件加载完成")
