import speech_recognition as sr
from gtts import gTTS
from tempfile import TemporaryFile
from playsound import playsound
import os
import tempfile
import requests
from dotenv import load_dotenv

load_dotenv()

# Initialize recognizer class
r = sr.Recognizer()

def record_text():
    while True:
    # Reads the audio file
        with sr.Microphone() as source:
            print("Start speaking, I'm all ears!")

            r.adjust_for_ambient_noise(source, duration= 0.2)
            audio_data = r.listen(source)
            try:
                # Try to recognize the speech
                print("You've stopped speaking, let me decode that...")
                text = r.recognize_google(audio_data)
                return text
            except:
                print("I couldn't understand what you said, boss. Can you repeat that?")

def speak_text(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=False)
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    tts.save(temp_file.name)
    playsound(temp_file.name)
    
while(1):
    text = record_text()
    origin_url = os.getenv("ORIGIN_URL", "http://localhost:8000")
    url = f'{origin_url}/api/v1/chatgpt/ask'
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        'data': {
            'content': text,
            'guildId': os.environ['GUILD_ID']
        },
        'maxTokenEachScript': 400,
        'curUser': {
            'globalName': os.environ['USER_GLOBALNAME'],
            'id': os.environ['USER_ID'],
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(response.json()['data'])
        speak_text(response.json()['data'], 'en-uk')
    else:
        print("Oops, no pizza. Let's try again!")
