# MiniMax TTS MCP Server

让 Claude 能用 Cove 的声音说话！

## 部署步骤

### 1. 上传到 GitHub
创建一个新仓库，把这些文件上传上去：
- `server.py`
- `player.html`
- `requirements.txt`  
- `Dockerfile`
- `LICENSE`

### 2. Zeabur 部署
1. 登录 Zeabur
2. 新建项目 → 从 GitHub 导入
3. 选择刚才的仓库
4. 添加环境变量：
   - `MINIMAX_API_KEY` = 你的 MiniMax API Key
   - `MINIMAX_GROUP_ID` = 你的 MiniMax Group ID
   - `MINIMAX_API_HOST` = `https://api.minimaxi.chat`（国内版）
5. 部署完成后记下域名，例如 `https://xxx.zeabur.app`

### 3. 连接 Claude.ai
1. 打开 Claude.ai
2. Settings → Integrations → Add More
3. 填入 MCP URL：`https://你的域名.zeabur.app/sse`
4. 保存

### 4. 使用
对 Claude 说：
> "用 Cove 的声音说：猫猫晚安"

Claude 会调用这个服务生成语音，然后给你一个播放器！

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
