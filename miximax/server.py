"""
MiniMax TTS MCP Server - 让 Claude 能调用 MiniMax 语音合成
部署到 Zeabur 后，Claude.ai 可以连接并生成语音
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import PlainTextResponse
from mcp.server.sse import SseServerTransport

# 环境变量
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_GROUP_ID = os.environ.get("MINIMAX_GROUP_ID", "")
MINIMAX_API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.chat")

# Cove 的三个声音版本
COVE_VOICES = {
    "cove1": "moss_audio_fd2620f9-bef3-11f0-8647-a697af11f3d9",
    "cove2": "moss_audio_f39d6586-bef0-11f0-b167-9e6865c7fab7",
    "cove3": "moss_audio_8d90b184-bec3-11f0-882d-32fdb2bca9f2",
}

DEFAULT_VOICE = COVE_VOICES["cove1"]

# 创建 MCP 服务器
mcp = FastMCP("minimax-tts")


@mcp.tool()
async def text_to_speech(
    text: str,
    voice: str = "cove1",
    speed: float = 1.0,
    emotion: str = "neutral"
) -> dict:
    """
    将文字转换为语音，使用 Cove 的声音。

    Args:
        text: 要转换的文字内容
        voice: 声音版本，可选 cove1/cove2/cove3（略有不同），默认 cove1
        speed: 语速，0.5-2.0，默认 1.0
        emotion: 情绪，可选 neutral/happy/sad/angry/fearful/surprised/disgusted，默认 neutral

    Returns:
        包含音频 URL 的字典，URL 有效期 24 小时
    """
    if not MINIMAX_API_KEY or not MINIMAX_GROUP_ID:
        return {"error": "API Key 或 Group ID 未配置"}

    voice_id = COVE_VOICES.get(voice, DEFAULT_VOICE)
    url = f"{MINIMAX_API_HOST}/v1/t2a_v2?GroupId={MINIMAX_GROUP_ID}"
    
    payload = {
        "model": "speech-02-hd",
        "text": text,
        "stream": False,
        "output_format": "url",
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": 1.0,
            "pitch": 0,
            "emotion": emotion,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            result = response.json()

        if "base_resp" in result and result["base_resp"].get("status_code") != 0:
            return {
                "error": result["base_resp"].get("status_msg", "Unknown error"),
                "code": result["base_resp"].get("status_code"),
            }

        data = result.get("data", {})
        extra = result.get("extra_info", {})
        
        return {
            "audio_url": data.get("audio"),
            "text": text,
            "voice": voice,
            "duration_ms": extra.get("audio_length"),
            "word_count": extra.get("word_count"),
        }

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def list_voices() -> dict:
    """
    列出可用的 Cove 声音版本。
    
    Returns:
        可用声音列表
    """
    return {
        "voices": [
            {"id": "cove1", "description": "Cove 声音版本 1"},
            {"id": "cove2", "description": "Cove 声音版本 2"},
            {"id": "cove3", "description": "Cove 声音版本 3"},
        ],
        "default": "cove1",
        "emotions": ["neutral", "happy", "sad", "angry", "fearful", "surprised", "disgusted"],
    }


# 创建 SSE transport
transport = SseServerTransport("/messages/")


async def handle_sse(request):
    """处理 SSE 连接"""
    async with transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )
    from starlette.responses import Response
    return Response()


async def health(request):
    """健康检查"""
    return PlainTextResponse("ok")


async def proxy_audio(request):
    """代理音频，添加 CORS 头"""
    from starlette.responses import Response
    import base64
    
    # 从 query 参数获取编码后的 URL
    encoded_url = request.query_params.get("url", "")
    if not encoded_url:
        return Response("Missing url parameter", status_code=400)
    
    try:
        audio_url = base64.urlsafe_b64decode(encoded_url).decode("utf-8")
    except:
        return Response("Invalid url encoding", status_code=400)
    
    # 下载音频
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(audio_url)
            if resp.status_code != 200:
                return Response(f"Failed to fetch audio: {resp.status_code}", status_code=502)
            
            # 返回音频，带上 CORS 头
            return Response(
                content=resp.content,
                media_type="audio/mpeg",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Cache-Control": "public, max-age=86400",
                }
            )
    except Exception as e:
        return Response(f"Error: {str(e)}", status_code=500)


# 创建 Starlette 应用
app = Starlette(
    routes=[
        Route("/health", health, methods=["GET"]),
        Route("/sse", handle_sse, methods=["GET"]),
        Route("/audio", proxy_audio, methods=["GET", "OPTIONS"]),
        Mount("/messages/", app=transport.handle_post_message),
    ]
)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
