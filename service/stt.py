import speech_recognition as sr
from tempfile import TemporaryFile
from playsound import playsound
from dotenv import load_dotenv
from colorama import init, Fore
import json

load_dotenv()

init()

r = sr.Recognizer()

def record_text(language):
    while True:
        with sr.Microphone() as source:
            print(f"{Fore.CYAN}[+] Start speaking...")
            r.adjust_for_ambient_noise(source, duration= 0.2)
            audio_data = r.listen(source)
            try:
                lang = {}
                with open('language.json') as f: 
                    lang = json.load(f)
                    
                print(f"{Fore.GREEN}[+] You've stopped speaking, let me decode that...", lang["languages"].get(language))
                text = r.recognize_google(audio_data, language=lang["languages"].get(language))
                text = text.lower()
                return text
            except:
                print(f"{Fore.RED}[+] I couldn't understand what you said, boss. Can you repeat that?")
                return None