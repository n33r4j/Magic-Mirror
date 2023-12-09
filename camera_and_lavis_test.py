# Camera + LAVIS test
import torch
from lavis.models import load_model_and_preprocess
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device}...")

import numpy as np
import cv2 as cv
import time

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
    print(f"Execution time: {time.time() - start_time}")
    print("Answers")
    for a in answers:
         print(a)
    # print(answer_1)
    # It's a bit slow ~15 sec per question


cap.release()
cv.destroyAllWindows()