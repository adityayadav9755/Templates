# majdooron ko bulawa
import speech_recognition as sr
import pyttsx3


class Listen:
    recog = sr.Recognizer()

    def hear(self):
        """
        When called turns on mic and returns the audio heard in string form.
        """
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recog.listen(source, phrase_time_limit=5)
        try:
            audio = self.recog.recognize_google(audio).lower()
        except ValueError:
            Speech.speak(Speech(), "I beg your pardon please!")

        return audio


class Speech:
    engine = pyttsx3.init()

    def __init__(self, rate=170, volume=0.8, voiceid=0):
        self.rate = rate
        self.volume = volume
        self.voiceid = voiceid

    def speak(self, speech):
        """
        Takes string as argument and makes computer speak that in audio form.
        """
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        self.engine.setProperty('voice', voices[self.voiceid].id)
        self.engine.say(speech)
        self.engine.runAndWait()
