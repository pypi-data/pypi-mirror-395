# CosyVoice MCP Server

A Model Context Protocol (MCP) server for Alibaba Cloud's [CosyVoice](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list) text-to-speech service.

This server allows you to generate high-quality, expressive speech from text using Alibaba Cloud's state-of-the-art CosyVoice models (V2 and V3).

## Features

- **List Voices**: Retrieve a curated list of high-quality voices suitable for various scenarios (social, narration, customer service, etc.).
- **Speech Synthesis**: Convert text to speech with support for:
    - **Model Selection**: Choose between `cosyvoice-v2` (standard) and `cosyvoice-v3-flash` (emotional).
    - **Control Parameters**: Adjust volume, speech rate, and pitch rate.
    - **Emotion Control**: Use natural language instructions to control emotion (V3 models only).
        - Supported emotions: `neutral`, `fearful`, `angry`, `sad`, `surprised`, `happy`, `disgusted`.
        - Format: `"你说话的情感是<emotion>。"`
    - **SSML Support**: Use SSML tags (e.g., `<break time="2s"/>`) for precise pause control.
    - **File Saving**: Save generated audio directly to a local file path.

## Configuration

You need an Alibaba Cloud DashScope API Key. Set it as an environment variable:

```bash
export COSYVOICE_MCP_DASHSCOPE_API_KEY=your_api_key_here
```

(Alternatively, `DASHSCOPE_API_KEY` is also supported).

### Optional Configuration

- `COSYVOICE_DEFAULT_OUTPUT_DIR`: Set a default directory for saving generated audio files if `output_file` is not specified.

```bash
export COSYVOICE_DEFAULT_OUTPUT_DIR=~/Desktop/CosyVoiceOutput
```

## MCP Client Configuration

Add the following to your MCP client configuration (e.g., `claude_desktop_config.json`):

### Using `uvx` (Recommended)

You can run the server directly from PyPI using `uvx`:

```json
{
  "mcpServers": {
    "cosyvoice": {
      "command": "uvx",
      "args": [
        "voicemcpserver"
      ],
      "env": {
        "COSYVOICE_MCP_DASHSCOPE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Using `python`

```json
{
  "mcpServers": {
    "cosyvoice": {
      "command": "python3",
      "args": [
        "-m",
        "voicemcpserver"
      ],
      "cwd": "/path/to/voicemcpserver/src",
      "env": {
        "COSYVOICE_MCP_DASHSCOPE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Voices

### CosyVoice V3 Flash (Supports Emotion Instructions)
| ID | Name | Description | Tags |
|----|------|-------------|------|
| `longanyang` | 龙安洋 | 阳光大男孩，20~30岁 | Social, Young, Male |
| `longanhuan` | 龙安欢 | 欢脱元气女，20~30岁 | Social, Energetic, Female |

### CosyVoice V2 (Standard High Quality)
| ID | Name | Description | Tags |
|----|------|-------------|------|
| `longxiaochun_v2` | 龙小淳 | 亲切女声，客服/播报 | Customer Service, Female |
| `longxiaoxia_v2` | 龙小夏 | 活泼女声，社交/娱乐 | Social, Female |
| `longxiaobai_v2` | 龙小白 | 清澈男声，社交/娱乐 | Social, Male |
| `longxiaocheng_v2` | 龙小诚 | 沉稳男声，有声书/播报 | Audiobook, Male |
| `longwan_v2` | 龙婉 | 积极知性女，有声书/新闻 | Audiobook, Female |
| `longyingmu` | 龙应沐 | 优雅知性女，客服 | Customer Service, Female |
| `longhuhu` | 龙呼呼 | 天真烂漫女童 | Child, Female |
| `longanran` | 龙安燃 | 活泼质感女，直播带货 | Live Streaming, Female |
| `longanchong` | 龙安冲 | 激情推销男，直播带货 | Live Streaming, Male |

## Usage Examples

### Synthesize Speech (Basic)

```json
{
  "text": "你好，欢迎使用 CosyVoice。",
  "voice": "longxiaochun_v2",
  "output_file": "/Users/username/Desktop/hello.mp3"
}
```

### Synthesize Speech (Advanced Control)

```json
{
  "text": "今天天气真不错！<break time=\"1s\"/> 我们去公园玩吧。",
  "voice": "longanyang",
  "model": "cosyvoice-v3-flash",
  "volume": 80,
  "speech_rate": 1.1,
  "instruction": "你说话的情感是happy。",
  "output_file": "/Users/username/Desktop/happy.mp3"
}
```
