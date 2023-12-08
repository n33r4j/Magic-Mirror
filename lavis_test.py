# https://github.com/salesforce/LAVIS
# For the installation to succeed, you need pip version greater than 20
# Activity detection: https://github.com/guillaume-chevalier/HAR-stacked-residual-bidir-LSTMs

import torch
from lavis.models import load_model_and_preprocess
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ====== IMAGES =======
# raw_image = Image.open("sample_images/merlion.png").convert("RGB")
# raw_image = Image.open("sample_images/man_in_suit.jpg").convert("RGB")
# raw_image = Image.open("sample_images/woman_in_dress.jpg").convert("RGB")
# raw_image = Image.open("sample_images/uni_student_1.jpg").convert("RGB")
raw_image = Image.open("sample_images/man_in_shorts_1.jpg").convert("RGB")

# ===== IMAGE CAPTIONING =========

# loads BLIP caption base model, with finetuned checkpoints on MSCOCO captioning dataset.
# this also loads the associated image processors
# model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
# # preprocess the image
# # vis_processors stores image transforms for "train" and "eval" (validation / testing / inference)
# image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
# # generate caption
# caption = model.generate({"image": image})
# print(caption)


# ========= VISUAL QUESTION ANSWERING =================

# Question: How long of a caption can it generate ?

model, vis_processors, txt_processors = load_model_and_preprocess(name="blip_vqa", model_type="vqav2", is_eval=True, device=device)
# ask a random question.
questions = ["How old is this person?",
	"Describe the outfit of the person",
	"What type of clothing is this person wearing?",
	"How is the person feeling?",
]

q_index = 1

image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
question = txt_processors["eval"](questions[q_index])
answers = model.predict_answers(samples={"image": image, "text_input": questions[q_index]}, inference_method="generate")
print(answers)
# It's a bit slow ~15 sec per question