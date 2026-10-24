# MiniMax TTS MCP Server

让 Claude 能用 Cove 的声音说话！

## 部署

### 1. 配置
通过环境变量配置：

| 变量 | 必填 | 说明 |
|------|------|------|
| `MINIMAX_API_KEY` | 是 | MiniMax API Key |
| `MINIMAX_GROUP_ID` | 是 | MiniMax Group ID |
| `MINIMAX_API_HOST` | 否 | 默认 `https://api.minimaxi.chat`（国内版） |
| `PORT` | 否 | 监听端口，默认 `8000` |
| `LOG_LEVEL` | 否 | 日志级别，默认 `INFO` |

### 2. 运行
用仓库里的 `Dockerfile` 构建并运行（镜像会带上 `server.py` 和 `player.html`），或者直接：

```bash
pip install -r requirements.txt
python server.py
```

### 3. 接口

| 路径 | 说明 |
|------|------|
| `/sse` | MCP 连接地址（SSE） |
| `/messages/` | MCP 消息投递 |
| `/health` | 健康检查，返回 `ok` |
| `/audio` | 音频代理（带 CORS 头） |

### 4. 连接
在支持 MCP 的客户端里添加服务器，URL 填 `http(s)://<主机>:<端口>/sse`。

### 5. 使用
对 Claude 说：
> "用 Cove 的声音说：猫猫晚安"

## 工具

| 工具 | 说明 |
|------|------|
| `text_to_speech` | 合成语音，返回音频链接（24 小时有效） |
| `speak_player` | 合成语音，并在对话里显示播放器，直接点播放即可 |
| `list_voices` | 列出可用声音和情绪 |

播放器是一条无文字的语音条：Clawd 像素形象会跟随播放状态变化，波形可以点击或拖动跳转。

## 声音选项

| 参数 | 可选值 | 说明 |
|------|--------|------|
| voice | cove1, cove2, cove3 | 三个略有不同的声音版本 |
| speed | 0.5 - 2.0 | 语速 |
| emotion | neutral, happy, sad, angry, fearful, surprised, disgusted | 情绪 |

## 费用
MiniMax 新用户免费 1 万声贝（约 12 分钟语音）

## 源码与协议

本项目以 [AGPL-3.0](../LICENSE) 协议开源，源码：https://github.com/sue1231511/minimax

对话内播放器里的像素形象 Clawd 及其动画逻辑来自 [watersalt0305/operit-clawd](https://github.com/watersalt0305/operit-clawd)（AGPL-3.0，作者 watersalt0305 / Mishio）。Clawd 是 Anthropic 旗下 Claude Code 的吉祥物，形象归 Anthropic 所有；这里是非官方粉丝使用，与 Anthropic 无关。

AGPL-3.0 第 13 条要求：通过网络使用本服务的人必须能拿到对应源码。播放器页面底部已放置指向本仓库的"本服务源码"链接。如果你自行部署并修改了代码，请把链接换成你自己的仓库地址（`player.html` 里的 `link-src`）。
