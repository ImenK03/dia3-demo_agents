import os
from dotenv import load_dotenv
from groq import Groq


class SpeechToText:

    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])

    def transcribe(self, audio_file):
        result = self.groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_file.getvalue()),
            model="whisper-large-v3-turbo",
            language="fr",
        )
        return result.text