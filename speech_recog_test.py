# Speech recognition test
# from pocketsphinx import LiveSpeech

# for phrase in LiveSpeech():
#     print(phrase)

# import speech_recognition as sr
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# r = sr.Recognizer()
# voice_data=""

# def record_audio():
#     with sr.Microphone(device_index=15) as source:
#         #r.energy_threshold >2000
#         # print("entering")
#         r.adjust_for_ambient_noise(source, duration=0.1)  
#         r.dynamic_energy_threshold = True        
#         audio = r.listen(source)
#         voice_data = ""
#         # print("before")
#         try:
#             voice_data = r.recognize_sphinx(audio)
#             # print("A")
#         except sr.UnknownValueError:
#             pass
#         except sr.RequestError:
#             print("Sorry, I did not get that")
#         return voice_data
    
# words = record_audio()
# print(words)

from vosk import Model, KaldiRecognizer
import pyaudio

# model = Model("models/vosk-model-en-us-0.22-lgraph/vosk-model-en-us-0.22-lgraph")
model = Model("models/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")

recognizer = KaldiRecognizer(model, 16000, '[ "mirror mirror" ]')

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        output = text[14:-3]
        print(output)
