from flask import Flask
from flask import request
import speech_recognition as sr
from pydub import AudioSegment
import subprocess
import os
from zoom import abre_zoom
from text_to_speech import text_to_speech
import time

#DOWNLOAD TO /bin the following files:
#ffmpeg.exe
#ffplay.exe
#ffprobe.exe

def delete_files(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully")
    except FileNotFoundError:
        print(f"File '{file_path}' not found")
    except Exception as e:
        print(f"Error deleting file '{file_path}': {e}")

def ogg_to_wav(input_file):
    # Set the output file path
    command = f'"bin/ffmpeg.exe" -i "audios/{input_file}.ogg" -acodec pcm_s16le -ar 44100 "audios/{input_file}.wav"'
    subprocess.run(command, shell=True, check=True)
    delete_files(f"audios/{input_file}.ogg")
    return f"audios/{input_file}.wav"

def speech_to_text(file_name):
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    
    with sr.AudioFile(file_name) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language='pt-BR')

    delete_files(file_name)

    return text


app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST', 'DELETE'])
def transcript():
    # if request.method == 'GET':
    #     print("GET")
    #     return "GET"
    if request.method == 'POST':
        print("POST")
        json_body = request.get_json()
        ogg_file_name = json_body['file_name']
        file_name = ogg_to_wav(ogg_file_name)
        return speech_to_text(file_name)
    # if request.method == 'DELETE':
    #     print("DELETE")
    #     return "DELETE"
    # else:
    #     print("error")
    #     return "ERROR"

@app.route('/zoom', methods = ['GET'])
async def zoom():
    return await abre_zoom()

@app.route('/tts', methods = ['POST'])
def tts():
    json_body = request.get_json()
    text_to_convert = json_body['text']
    print(text_to_convert)
    resp = text_to_speech(text_to_convert)
    return resp

@app.route('/deltts', methods = ['POST'])
def deltts():
    json_body = request.get_json()
    path_to_delete = json_body['path']
    print(path_to_delete)
    delete_files(f'audios/{path_to_delete}')
    return 'deletado'


app.run()