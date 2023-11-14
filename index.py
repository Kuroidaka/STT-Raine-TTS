import speech_recognition as sr
from gtts import gTTS
from tempfile import TemporaryFile
from playsound import playsound
import os
import tempfile
import requests
from dotenv import load_dotenv
from colorama import init, Fore
import tts
import stt

load_dotenv()

init()

while(1):
    text = stt.record_text()
    origin_url = os.getenv("ORIGIN_URL", "http://localhost:8000")
    url = f'{origin_url}/api/v1/chatgpt/ask-for-tts'
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        'data': {
            'content': text,
            'guildId': os.environ['GUILD_ID']
        },
        'maxTokenEachScript': 1000,
        'curUser': {
            'globalName': os.environ['USER_GLOBALNAME'],
            'id': os.environ['USER_ID'],
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"{Fore.BLACK}==========>", response.json()['data'])
        tts.text_to_speech_OpenAI(response.json()['data'])
    else:
        print("Oops, no pizza. Let's try again!")