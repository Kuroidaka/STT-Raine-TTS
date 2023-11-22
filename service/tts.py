import os
import tempfile
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from playsound import playsound
from tempfile import NamedTemporaryFile
from gtts import gTTS
from tempfile import TemporaryFile
import os
import tempfile
from colorama import init, Fore
import requests


load_dotenv()
init()


def text_to_speech_OpenAI(text, speed):
    OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPEN_AI_API_KEY)
    
    fd, path = tempfile.mkstemp(suffix=".mp3")
    with os.fdopen(fd, 'w') as tmp:

        speech_file_path = path

        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
            speed=speed
        )
        response.stream_to_file(speech_file_path)
        print("======str(speech_file_path)", str(speech_file_path))
        return str(speech_file_path)

def text_to_speech_file(path):
   playsound(path)
        
def text_to_speech_gg(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=False)
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    tts.save(temp_file.name)
    playsound(temp_file.name)
    
def text_to_speech_ell(text):
    ELEVEN_LAB_API_KEY = os.getenv("ELEVEN_LAB_API_KEY")
    CHUNK_SIZE = 1024
    RAINE_VOICE_ID = os.environ["RAINE_VOICE_ID"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{RAINE_VOICE_ID}"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVEN_LAB_API_KEY
    }

    data = {
    "text": text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    
    # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    # temp_file.write(response.content)
    # temp_file.close()
    # playsound(temp_file.name)
    
    fd, path = tempfile.mkstemp(suffix=".mp3")
    with os.fdopen(fd, 'wb') as tmp:
        response = requests.post(url, json=data, headers=headers)
        tmp.write(response.content)

    print("======str(speech_file_path) ", path)
    return path