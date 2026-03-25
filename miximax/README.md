# MiniMax TTS MCP Server

让 Claude 能用 Cove 的声音说话！

## 部署步骤

### 1. 上传到 GitHub
创建一个新仓库，把这三个文件上传上去：
- `server.py`
- `requirements.txt`  
- `Dockerfile`

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
