from gtts import gTTS
from datetime import datetime, timedelta

text = 'teste de texto para áudio'

def text_to_speech(text):

    print("text to speech", text)

    date_time_now = datetime.utcnow() - timedelta(hours=3)

    date_time_now = date_time_now.strftime('%Y-%m-%d %H-%M-%S-%f')

    example_text = f'{text}'

    speech = gTTS(text = example_text, lang='pt', slow=False)

    speech.save(f'audios/{date_time_now}.mp3')

    return f'{date_time_now}.mp3'