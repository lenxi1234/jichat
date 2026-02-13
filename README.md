# Jichat QQ 机器人

基于 NcatBot + NapCat 的 QQ 群聊机器人，包含 AI 对话插件与若干功能插件（如禁漫下载、二次元图片等）。

## 功能概览

- **AI 对话（鸡桑）**
  - 群内 @鸡桑 或消息包含“鸡桑”触发
  - 触发后 10 秒内继续聊天无需关键词
  - 10 秒未继续发言则回到关键词触发
  - 按人独立历史（同群不同人互不干扰）
- **固定话术**
  - 发送“鸡桑艾草”触发固定回复（不会触发 AI）
- **菜单**
  - 群聊输入 `/菜单` 查看功能与规则
- **管理员指令（私聊）**
  - `prompt` 查看当前 prompt
  - `set_prompt <内容>` 修改 prompt
  - `reload_prompt` 重新加载 prompt 文件
  - `clear_log` 清空 `messages.log`
  - `clear_history_log` 清空所有历史记录

## 目录结构

```
jichat/
  main.py                         # 主程序入口
  plugins/
    CatCat/                        # AI 对话插件
      main.py
      AiChat.py
      responses/CatCatRes.py
      utils/api_utils.py
      config/
        config.yaml
        cat_prompt.txt
      logs/
        *_history.log              # 群/人对话历史
        free_api/messages.log      # 请求调试日志
```

## 运行前准备

1. 安装 Python 依赖（示例）  
   - `ncatbot`、`aiohttp`、`aiofiles`、`PyYAML`
2. 配置 NapCat 与 NcatBot
3. 配置 AI API
   - 修改 `plugins/CatCat/config/config.yaml` 的 `api_key`

## 启动

在 `jichat` 目录下运行：

```
python main.py
```

## 关键配置

- **机器人 QQ / Root**
  - 在 `main.py` 的 `bot.run(bt_uin=..., root=...)` 中配置
- **AI API**
  - `plugins/CatCat/utils/api_utils.py` 中配置 URL、model
  - `plugins/CatCat/config/config.yaml` 中配置 `api_key`
- **人设与输出风格**
  - `plugins/CatCat/config/cat_prompt.txt`

## 说明

- `messages.log` 是每次请求发送给模型的完整 payload 记录（调试用）。  
  可通过管理员指令 `clear_log` 清空。
- 对话历史写在 `plugins/CatCat/logs/*_history.log`，可通过 `clear_history_log` 清空。

## 常见问题

**1. 401 “Api key is invalid”**  
确认 API Key 是否正确、是否有该模型权限、URL 是否匹配平台。

**2. AI 回复不稳定 / 不连贯**  
检查 prompt 是否过长、历史是否过多，必要时清空历史或缩短 prompt。
