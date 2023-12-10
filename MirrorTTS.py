# TTS

import pyttsx3

voice_indexes = {
    "EngUS-male": 0,
    "EngUK-female": 1,
    "EngUS-female": 2,
    "Jap-female": 3,
    "Chinese-female": 4,
}

voice_profiles = {
    "A": "EngUS-female",
    "B": "EngUS-male",
    "Broski": "EngUS-male",
    "Bogan": "EngUS-male",
    "Butler": "EngUK-female",
    "Gordan Rm": "EngUS-male",
    "David At": "EngUS-male",
    "Paris Hilton": "EngUS-female",
    "Uncle Roger": "EngUS-male",
}


class MirrorTTS:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.rate = self.engine.getProperty('rate')
        self.volume = self.engine.getProperty('volume')

    def setVoiceProfile(self, persona):
        # Not the best way to do this, I know :(
        self.engine.setProperty('voice', self.voices[voice_indexes[voice_profiles[persona]]].id)
        # self.engine.setProperty('rate', rate)
        # self.engine.setProperty('volume', volume)