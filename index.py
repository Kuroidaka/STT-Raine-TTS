import speech_recognition as sr
from gtts import gTTS
from tempfile import TemporaryFile
from playsound import playsound
import os
import tempfile

# Initialize recognizer class
r = sr.Recognizer()

def record_text():
    while True:
    # Reads the audio file
        with sr.Microphone(device_index = 3) as source:
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
    speak_text(text, 'en-uk')