import speech_recognition as sr
from tempfile import TemporaryFile
from playsound import playsound
from dotenv import load_dotenv
from colorama import init, Fore

load_dotenv()

init()

# Initialize recognizer class
r = sr.Recognizer()

def record_text():
    while True:
    # Reads the audio file
        with sr.Microphone() as source:
            print(f"{Fore.CYAN}[+] Start speaking...")
            r.adjust_for_ambient_noise(source, duration= 0.2)
            audio_data = r.listen(source)
            try:
                print(f"{Fore.GREEN}[+] You've stopped speaking, let me decode that... ")
                text = r.recognize_google(audio_data, language="vi-VI")
                text = text.lower()
                return text
            except:
                print(f"{Fore.RED}[+] I couldn't understand what you said, boss. Can you repeat that?")
