import os
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


load_dotenv()
init()


API_KEY = os.getenv("OPENAI_API_KEY")


def text_to_speech_OpenAI(text, speed):
    client = OpenAI(api_key=API_KEY)

    with NamedTemporaryFile(delete=True, suffix=".mp3") as temp_mp3:
        speech_file_path = temp_mp3.name

        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
            speed=speed
        )

        response.stream_to_file(speech_file_path)
        playsound(str(speech_file_path))
        
        
def text_to_speech_gg(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=False)
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    tts.save(temp_file.name)
    playsound(temp_file.name)