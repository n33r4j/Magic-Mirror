# Basic Product + Speech Test
# Camera + LAVIS + ChatGPT + TTS + Speech Recog

# TODO
# - Render Captions larger to the screen.
# - Talk every minute along with keyword detection
# - Animations while waiting

import torch
from lavis.models import load_model_and_preprocess
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device}...")

from openai import OpenAI
from dotenv import load_dotenv
import pyttsx3
import os

from vosk import Model, KaldiRecognizer
import pyaudio
import Prompts as pmp
import random

import Prompts as pmp
from MirrorTTS import MirrorTTS as mTTS

load_dotenv()

import numpy as np
import cv2 as cv
import time

#========[ INPUTS ]==========================================
PERSONA_INDEX = 5 # <--- Change this value
PERSONAS = [
    "A",
    "B",
    "Broski",
    "Bogan",
    "Butler",
    "Gordon R",
    "David At",
    "Paris Hilton",
    "Uncle Roger"
]

#============================================================

tts_engine = mTTS()
tts_engine.setVoiceProfile(PERSONAS[PERSONA_INDEX])

client = OpenAI()

speech_R_model = Model("models/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")

recognizer = KaldiRecognizer(speech_R_model, 16000, '[ "mirror mirror" ]')
magic_words = "mirror mirror"

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# time.sleep(5)
start_time = time.perf_counter()

cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# So that the image is not too dark
ramp_frames = 30
for i in range(ramp_frames):
        temp = cap.read()

while True:
    speech_data = stream.read(4096, exception_on_overflow = False)
    
    if recognizer.AcceptWaveform(speech_data):
        text = recognizer.Result()
        output = text[14:-3]

        if output == magic_words:
            print(output, "ok, give me a moment...")
            tts_engine.engine.say("ok, give me a moment...")
            tts_engine.engine.runAndWait()

            ret, frame = cap.read()
        
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                tts_engine.engine.say("Ahhh, something went wrong. Imma head out...")
                tts_engine.engine.runAndWait()
                break

            else:    
                # cv.imshow('frame', frame)
                
                rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                raw_image = Image.fromarray(rgb_image)

                raw_image.show()

                # while True:
                #     if cv.waitKey(1) == ord('q'):
                #         break

                model, vis_processors, txt_processors = load_model_and_preprocess(name="blip_vqa", model_type="vqav2", is_eval=True, device=device)
                # ask a random question.

                # start_time = time.perf_counter()
                image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
                
                answers = []

                for q in pmp.questions:
                    pq = txt_processors["eval"](q)   
                    answers.append(model.predict_answers(samples={"image": image, "text_input": pq}, inference_method="generate")[0])
                
                # print(f"Execution time: {time.perf_counter() - start_time}")
                print("Answers")
                for a in answers:
                    print(a)
                
                person_description = f"They are about {answers[0]} years old, wearing {answers[1]}, a {answers[3]} top, a {answers[4]} bottom. They are in {answers[5]} clothes and also seem to be wearing {answers[11]}. They have {answers[7]} looking facial features and look {answers[6]}. They are {answers[8]} in a {answers[9]} and their hair is {answers[12]}."

                print("="*15, "DEBUG INFO", "="*15)
                print("="*8, "PROMPT", "="*8)
                print(pmp.goals["Describe person"] + person_description + pmp.extras["shorten"])
                print("="*40)

                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": pmp.personalities[PERSONAS[PERSONA_INDEX]]},
                        {"role": "user", "content": pmp.goals["Describe person"] + person_description + pmp.extras["shorten"]}
                    ]
                )

                print(f"Execution time: {time.perf_counter() - start_time}")

                response = completion.choices[0].message.content
                print("="*40)
                print(f"PERSONA: {PERSONAS[PERSONA_INDEX]}")
                print(response)
                print("="*40)

                tts_engine.engine.say(response)
                tts_engine.engine.runAndWait()

        else:
            wrong_answer = pmp.wrong_keyword_responses[random.randint(0, len(pmp.wrong_keyword_responses)-1)]
            print(wrong_answer)
            tts_engine.engine.say(pmp.wrong_keyword_responses[random.randint(0, len(pmp.wrong_keyword_responses)-1)])
            tts_engine.engine.runAndWait()
    

cap.release()
cv.destroyAllWindows()
