import os
from openai import OpenAI
from dotenv import load_dotenv
from playsound import playsound
from gtts import gTTS
from colorama import init, Fore
import json
import service.tts as tts

load_dotenv()
init()

API_KEY = os.getenv("OPENAI_API_KEY")

def text_to_speech_OpenAI(text, speed, save_path, name):
    client = OpenAI(api_key=API_KEY)

    # specify your path in speech_file_path
    speech_file_path = os.path.join(save_path, f"{name}.mp3")

    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
        speed=speed
    )

    response.stream_to_file(speech_file_path)
    playsound(speech_file_path)
    
# tts.text_to_speech_file("assets/voice/fake/en/output0.mp3")


lang = {}
with open('./assets/voice/error/error_res.json') as f: 
    lang = json.load(f)

for i in range(len(lang['vi'])):
    text_to_speech_OpenAI(lang['vi'][i], 1.1, './assets/voice/error/vi', f"output{i}")

