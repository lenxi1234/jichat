from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.logger import get_log

bot = BotClient()
_log = get_log()
INTRO_GROUP_ID = "1003906941"

# ========== 菜单功能 ===pip=======
@bot.on_group_message()
async def on_group_message(msg: GroupMessage):
    if msg.raw_message == "/菜单" or msg.raw_message == "鸡桑" or msg.raw_message == "@鸡桑":
        menu_text = """
🤖 鸡桑机器人功能菜单 🤖
        
📚 禁漫本子下载 (JmComicPlugin)  
• /jm <本子ID> - 下载禁漫本子并发送PDF
• /jmzip <本子ID> - 下载禁漫本子并发送ZIP(失败回退PDF)
• 例如: /jm 114514

🎨 二次元图片 (Lolicon)
• /loli [数量] [标签] - 发送随机二次元图片
• /r18 [数量] [标签] - 发送R18图片(需权限)
• 示例: /loli 3 萝莉、/loli 白丝

🐔 艾草的鸡桑
发送“鸡桑艾草”获取特殊回复

🐔 ai鸡桑
@鸡桑 或者 聊天中带有“鸡桑”
即可收到 ai鸡桑的回复
⏱ 自动回复规则
触发后10秒内继续聊天无需关键词
超过10秒未回复需再次触发
"""
        
        await msg.reply(text=menu_text)
    # 新增功能：艾草回复
    elif msg.raw_message == "鸡桑艾草":
        await msg.reply(text="哦齁齁齁哦~呀咩咯~")

@bot.on_private_message()
async def on_private_message(msg: PrivateMessage):
    if msg.raw_message == "/菜单":
        menu_text = """
🤖 鸡桑机器人功能菜单 🤖
        
📚 禁漫本子下载 (JmComicPlugin)  
• /jm <本子ID> - 下载禁漫本子并发送PDF
• /jmzip <本子ID> - 下载禁漫本子并发送ZIP(失败回退PDF)
• 例如: /jm 114514

🎨 二次元图片 (Lolicon)
• /loli [数量] [标签] - 发送随机二次元图片
• /r18 [数量] [标签] - 发送R18图片(需权限)
• 示例: /loli 3 萝莉、/loli 白丝

🐔 艾草的鸡桑
发送“鸡桑艾草”获取特殊回复

🐔 ai鸡桑
@鸡桑 或者 聊天中带有“鸡桑”
即可收到 ai鸡桑的回复

⏱ 自动回复规则
触发后10秒内继续聊天无需关键词
超过10秒未回复需再次触发

🛠 管理员指令（私聊使用）
• prompt - 查看当前 prompt
• set_prompt <内容> - 修改 prompt
• reload_prompt - 重新加载 prompt 文件
• clear_log - 清空 messages.log
• clear_history_log - 清空所有历史记录
"""
        
        await msg.reply(text=menu_text)
    # 新增功能：艾草回复
    elif msg.raw_message == "鸡桑艾草":
        await msg.reply(text="哦齁齁齁哦~呀咩咯~")

@bot.on_startup()
async def on_startup(event):
    intro_text = (
        "大家好呀，我是鸡桑~我上线啦！\n"
        "我可以帮你下本子和涩图，陪你聊天、讲笑话，也支持群内关键词“鸡桑”或者@我 触发 AI 回复。\n"
        "输入“/菜单”可以查看完整功能哦。"
    )
    await bot.api.post_group_msg(INTRO_GROUP_ID, text=intro_text)

# ========== 启动 BotClient==========
if __name__ == "__main__":
    bot.run(bt_uin="3876282392", root = "3182186232") # 这里写 Bot 的 QQ 号
