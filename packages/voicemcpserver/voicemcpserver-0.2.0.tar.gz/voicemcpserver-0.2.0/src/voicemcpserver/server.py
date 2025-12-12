import os
import asyncio
import sys
import logging

# Configure logging to stderr to avoid interfering with MCP protocol on stdout
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
from typing import Optional
from dotenv import load_dotenv
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configure API Key
api_key = os.getenv("COSYVOICE_MCP_DASHSCOPE_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    logging.warning("DashScope API Key not found. Please set COSYVOICE_MCP_DASHSCOPE_API_KEY or DASHSCOPE_API_KEY.")
else:
    dashscope.api_key = api_key

# Initialize MCP Server
mcp = FastMCP("CosyVoice")

from .voices import VOICES, get_voice_by_id

@mcp.tool()
def list_voices() -> str:
    """
    List available voices for speech synthesis.
    Returns a JSON string containing the list of voices.
    """
    import json
    return json.dumps(VOICES, ensure_ascii=False, indent=2)

@mcp.tool()
def synthesize_speech(
    text: str, 
    voice: str = "longxiaochun_v2", 
    model: str = "cosyvoice-v2", 
    format: str = "mp3", 
    output_file: Optional[str] = None,
    volume: int = 50,
    speech_rate: float = 1.0,
    pitch_rate: float = 1.0,
    instruction: Optional[str] = None
) -> str:
    """
    Synthesize speech from text using Alibaba Cloud CosyVoice.

    Args:
    Args:
        text: The text to synthesize. 
              Supports SSML tags for pauses, e.g., "Hello <break time='1000ms'/> world".
        voice: The voice ID to use (default: "longxiaochun_v2").
        model: The model version (default: "cosyvoice-v2").
        format: The audio format (default: "mp3").
        output_file: Optional path to save the generated audio file.
        volume: Volume (0-100, default: 50).
        speech_rate: Speech rate (0.5-2.0, default: 1.0).
        pitch_rate: Pitch rate (0.5-2.0, default: 1.0).
        instruction: Instruction text for emotion/style control.
                     Required for CosyVoice V3 models.
                     Format: "你说话的情感是<emotion>。"
                     Supported emotions: neutral, fearful, angry, sad, surprised, happy, disgusted.
                     Example: "你说话的情感是happy。"
                     
                     You can also combine with scenario or role:
                     - Scenario: "你正在进行<scenario>，你说话的情感是<emotion>。"
                       (e.g. "你正在进行新闻播报，你说话的情感是neutral。")
                     - Role: "你现在说话的角色是<role>，你说话的情感是<emotion>。"
                       (e.g. "你现在说话的角色是一个旁白，你说话的情感是neutral。")

    Returns:
        The path to the generated audio file.
    """
    if not dashscope.api_key:
        return "Error: DashScope API Key is not configured."

    # Validate parameters
    if not (0 <= volume <= 100):
        return "Error: volume must be between 0 and 100."
    if not (0.5 <= speech_rate <= 2.0):
        return "Error: speech_rate must be between 0.5 and 2.0."
    if not (0.5 <= pitch_rate <= 2.0):
        return "Error: pitch_rate must be between 0.5 and 2.0."

    # Validate voice
    voice_info = get_voice_by_id(voice)
    if not voice_info:
        # Warn but proceed, maybe it's a custom voice or new one not in our list
        logging.warning(f"Voice {voice} not found in local registry.")
    
    from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat

    # Map string format to AudioFormat enum
    # Default to MP3 22050Hz if not specified or unknown
    format_map = {
        "mp3": AudioFormat.MP3_22050HZ_MONO_256KBPS,
        "wav": AudioFormat.WAV_22050HZ_MONO_16BIT,
        "pcm": AudioFormat.PCM_22050HZ_MONO_16BIT,
    }
    audio_format = format_map.get(format.lower(), AudioFormat.MP3_22050HZ_MONO_256KBPS)
    
    # Create synthesizer
    synthesizer = SpeechSynthesizer(
        model=model, 
        voice=voice, 
        format=audio_format,
        volume=volume,
        speech_rate=speech_rate,
        pitch_rate=pitch_rate,
        instruction=instruction
    )
    
    # Generate audio
    try:
        audio = synthesizer.call(text)
        
        # Check if we got audio data
        if synthesizer.get_last_request_id():
            final_output_path = output_file
            
            # Handle default output directory if output_file is not provided
            if not final_output_path:
                default_dir = os.getenv("COSYVOICE_DEFAULT_OUTPUT_DIR")
                if default_dir:
                    # Expand user path (e.g. ~)
                    default_dir = os.path.abspath(os.path.expanduser(default_dir))
                    os.makedirs(default_dir, exist_ok=True)
                    # Generate a filename based on timestamp
                    import time
                    filename = f"cosyvoice_{int(time.time())}.{format}"
                    final_output_path = os.path.join(default_dir, filename)

            if final_output_path:
                # Use provided or generated path
                filepath = os.path.abspath(os.path.expanduser(final_output_path))
                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'wb') as f:
                    f.write(audio)
            else:
                 # Save to a temporary file
                import tempfile
                # Create a temp file with the correct extension
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as f:
                    f.write(audio)
                    filepath = f.name
            
            return f"Audio generated successfully: {filepath}"
        else:
             return f"Error: No audio data received. Request ID: {synthesizer.get_last_request_id()}"

    except Exception as e:
        return f"Error synthesizing speech: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
