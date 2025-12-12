# Voice definitions for CosyVoice
# Source: https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list

VOICES = [
    # CosyVoice V3 Flash Voices
    {
        "id": "longanyang",
        "name": "龙安洋",
        "description": "阳光大男孩，20~30岁，适合社交陪伴",
        "model": "cosyvoice-v3-flash",
        "language": ["zh", "en"],
        "tags": ["male", "young", "social"]
    },
    {
        "id": "longanhuan",
        "name": "龙安欢",
        "description": "欢脱元气女，20~30岁，适合社交、剧情",
        "model": "cosyvoice-v3-flash",
        "language": ["zh", "en"],
        "tags": ["female", "young", "energetic"]
    },

    # CosyVoice V2 Voices (Standard)
    # Social / General
    {
        "id": "longxiaochun_v2",
        "name": "龙小淳",
        "description": "亲切女声，20~30岁，适合客服、播报",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["female", "young", "customer_service"]
    },
    {
        "id": "longxiaoxia_v2",
        "name": "龙小夏",
        "description": "活泼女声，20~30岁，适合社交、娱乐",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["female", "young", "social"]
    },
    {
        "id": "longxiaobai_v2",
        "name": "龙小白",
        "description": "清澈男声，20~30岁，适合社交、娱乐",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["male", "young", "social"]
    },

    # Audiobook / Narration
    {
        "id": "longxiaocheng_v2",
        "name": "龙小诚",
        "description": "沉稳男声，20~30岁，适合有声书、播报",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["male", "young", "audiobook"]
    },
    {
        "id": "longwan_v2",
        "name": "龙婉",
        "description": "积极知性女，20~30岁，适合有声书、新闻",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["female", "young", "audiobook"]
    },

    # Customer Service
    {
        "id": "longyingmu",
        "name": "龙应沐",
        "description": "优雅知性女，适合客服",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["female", "customer_service"]
    },
    
    # Children
    {
        "id": "longhuhu",
        "name": "龙呼呼",
        "description": "天真烂漫女童，适合儿童内容",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["female", "child"]
    },

    # Live Streaming
    {
        "id": "longanran",
        "name": "龙安燃",
        "description": "活泼质感女，适合直播带货",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["female", "live_streaming"]
    },
    {
        "id": "longanchong",
        "name": "龙安冲",
        "description": "激情推销男，适合直播带货",
        "model": "cosyvoice-v2",
        "language": ["zh", "en"],
        "tags": ["male", "live_streaming"]
    },
    
    # Add more voices as needed
]

def get_voice_by_id(voice_id):
    for voice in VOICES:
        if voice["id"] == voice_id:
            return voice
    return None
