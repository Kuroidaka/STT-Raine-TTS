import speech_recognition as sr
from gtts import gTTS
from tempfile import TemporaryFile
from playsound import playsound
import os, sys, argparse
import tempfile
import requests
from dotenv import load_dotenv
from colorama import init, Fore
import service.tts as tts
import service.stt as stt
import threading
import concurrent.futures
import json
import utils
import time


load_dotenv()

init()


def cli_argument():
    parser = argparse.ArgumentParser(description="Which language do you use for recording?")
    parser.add_argument("-l", "--language", dest="language", type=str,
                        help="Language for recording", default="en-US",
                        required=True, nargs="+")
    argument = parser.parse_args()
    if not argument.language:
        print(f"{Fore.RED}[-] Please specify the a language for recording."
              " Use --help to see usage.")
        sys.exit()
    return argument

args = cli_argument()
language = "".join(args.language)

def fake_response(path, type):
     with open(path) as f:
        fake_res = json.load(f)
        fake_text_index = utils.get_random_index(fake_res[language])
        print(fake_text_index)
        path = f"./assets/voice/{type}/{language}/output{fake_text_index}.mp3"
        if utils.check_file_path(path):
            tts.text_to_speech_file(path)

while(1):
    text = stt.record_text(language)
    origin_url = os.getenv("ORIGIN_URL", "http://localhost:8000")
    url = f'{origin_url}/api/v1/chatgpt/ask-for-tts'
    

    if text is not None:
        print(f'{Fore.BLACK}You said: {text}')
        audio_file_path = None
        # Define your tasks
        def task1():
            fake_response('./assets/voice/fake/fake_res.json', 'fake')

        def task2():
            global audio_file_path
            headers = {'Content-Type': 'application/json'}
            payload = {
                'data': {
                    'content': text,
                    'guildId': os.environ['GUILD_ID']
                },
                'maxTokenEachScript': 300,
                'curUser': {
                    'globalName': os.environ['USER_GLOBALNAME'],
                    'id': os.environ['USER_ID'],
                },
                'lan': language
            }

            try:
                response = requests.post(url, headers=headers, json=payload)

                print('response.status_code', response.status_code)
                if response.status_code == 200:
                    print(f"{Fore.BLACK}==========>", response.json()['data'])
                    # tempSpeech = tts.text_to_speech_OpenAI(response.json()['data'], 1)
                    tempSpeech = tts.text_to_speech_ell(response.json()['data'])
                    audio_file_path = os.path.join(tempSpeech)            
                else:
                   raise Exception("Non-200 status code")
            except Exception as e:
                print(f"{Fore.BLACK}==========>", "ERROR OCCUR")
                fake_response('./assets/voice/error/error_res.json', 'error')
        stop_event = threading.Event()
               
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future2 = executor.submit(task2)
            
            time.sleep(13)
            if future2.running():
                future1 = executor.submit(task1)
                result2 = future2.result()
                result1 = future1.result()
                if audio_file_path:
                    playsound(audio_file_path)
                    os.remove(audio_file_path)
            else:
                result2 = future2.result()  # Get result of task2 if it's already done
                if audio_file_path:
                    playsound(audio_file_path)
                    os.remove(audio_file_path)
                
        