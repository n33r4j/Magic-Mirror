# Basic Product Test
# Camera + LAVIS + ChatGPT + TTS

# Camera + LAVIS test
import torch
from lavis.models import load_model_and_preprocess
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device}...")

from openai import OpenAI
from dotenv import load_dotenv
import pyttsx3
import os

load_dotenv()

import numpy as np
import cv2 as cv
import time

personalities = {
"A": "You are a sassy, sarcastic assistant easily annoyed by people asking questions. You also frequently make puns and jokes.",
"B": "You are a genuine, earnest assistant who deeply respects others. You also give complements and make flattering remarks quite often.",
"C": "You are a broski. You talk to everyone like they are your homie. You speak nothing but the truth, the cold hard truth.",
"D": "You are an Australian bogan with a strange fondness of the color red. You seek red items and never fail to bring it up. You also like to describe things using analogies familiar to you.",
"E": "You are an butler from the Victorian era. You are extremely formal in your communication, have utmost respect for authority and quick to lash back with clever comebacks at anyone who does not conform to Victorian values.",
"G": "You are Gordon Ramsey and you're annoyed.",
}

goals = {
"Describe person": "Describe the person standing in front of you.",
"Greet stranger": "Greet the stranger in front of you.",
}

extras = {
"shorten": "Keep responses to upto about 100 words.",
}

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

engine.setProperty('voice', voices[0].id)
print(f"rate: {rate}")
engine.setProperty('rate', rate)
engine.setProperty('volume', volume)

client = OpenAI()

# time.sleep(5)
start_time = time.time()

cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# So that the image is not too dark
ramp_frames = 30
for i in range(ramp_frames):
        temp = cap.read()

ret, frame = cap.read()
    
if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
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
    questions = ["How old is this person?",
        "Describe the outfit of the person",
        "What type of clothing is this person wearing?",
        "What color top are they wearing?",
        "What color bottom are they wearing?",
        "What style of clothing are they wearing?",
        "How is the person feeling?",
        "Describe the person's facial features",
        "What is the person doing?",
        "Where are they currently?",
        "What environment are they currently in?",
        "What accessories they wearing?",
        "What hairstyle do they have?",
        "What kind of shoes are they wearing?",
    ]

    # start_time = time.time()
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    
    answers = []

    for q in questions:
        pq = txt_processors["eval"](q)   
        answers.append(model.predict_answers(samples={"image": image, "text_input": pq}, inference_method="generate"))
    
    # question_1 = txt_processors["eval"](questions[1])
    # question_2 = txt_processors["eval"](questions[5])
    # question = txt_processors["eval"](qs)
    # answer_1 = model.predict_answers(samples={"image": image, "text_input": question_1}, inference_method="generate")
    # answer_2 = model.predict_answers(samples={"image": image, "text_input": question_2}, inference_method="generate")
    # answers = model.predict_answers(samples={"image": image, "text_input": qs}, inference_method="generate")
    # print(f"Execution time: {time.time() - start_time}")
    print("Answers")
    for a in answers:
         print(a)
    # print(answer_1)
    # It's a bit slow ~15 sec per question
    person_description = f"They are about {answers[0]} years old, wearing {answers[1]}, a {answers[3]} top, a {answers[4]} bottom. They are in {answers[5]} clothes and also seem to be wearing {answers[11]}. They have {answers[7]} looking facial features and look {answers[6]}. They are {answers[8]} in a {answers[9]}. Their hair is {answers[12]} and have on {answers[13]}."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": personalities["G"]},
            {"role": "user", "content": goals["Describe person"] + person_description + extras["shorten"]}
        ]
    )

    print(f"Execution time: {time.time() - start_time}")

    response = completion.choices[0].message.content
    print(response)

    engine.say(response)
    engine.runAndWait()

cap.release()
cv.destroyAllWindows()