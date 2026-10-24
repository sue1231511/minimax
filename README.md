# MiniMax TTS MCP Server

让 Claude 用 Cove 的声音说话的 MCP 服务器，基于 MiniMax 语音合成。在对话里会直接显示一条语音条，点一下就能听，不用打开链接。

语音条里有一只会跟着播放状态变化的像素小螃蟹 Clawd：加载时东张西望，播放时说话，播完开心，出错难过。

## 功能

| 工具 | 说明 |
|------|------|
| `speak_player` | 合成语音，并在对话里显示语音条（波形、点击或拖动跳转） |
| `text_to_speech` | 合成语音，返回音频链接（24 小时有效） |
| `list_voices` | 列出可用声音和情绪 |

声音：`cove1` / `cove2` / `cove3`。语速 0.5 到 2.0。情绪：`neutral` `happy` `sad` `angry` `fearful` `surprised` `disgusted`。

## 快速开始

需要 MiniMax 的 API Key 和 Group ID。

```bash
docker build -t minimax-tts ./miximax
docker run -p 8000:8000 \
  -e MINIMAX_API_KEY=你的Key \
  -e MINIMAX_GROUP_ID=你的GroupID \
  minimax-tts
```

然后在支持 MCP 的客户端里添加服务器，地址填 `http(s)://<主机>:8000/sse`，再对 Claude 说：

> 用 Cove 的声音说：猫猫晚安

完整的环境变量、接口和说明见 [`miximax/README.md`](miximax/README.md)。

## 协议与致谢

本项目以 [AGPL-3.0](LICENSE) 协议开源。

语音条里的像素形象 Clawd 及其动画逻辑来自 [watersalt0305/operit-clawd](https://github.com/watersalt0305/operit-clawd)（AGPL-3.0，作者 watersalt0305 / Mishio）。Clawd 是 Anthropic 旗下 Claude Code 的吉祥物，形象归 Anthropic 所有；这里是非官方粉丝使用，与 Anthropic 无关。
