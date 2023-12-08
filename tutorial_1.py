# Idea Demo v1
# Mirror Mirror GPT ?
# A personal assistant at your mirror to comment on your appearance for the day before you step out the door. Has the potential to put you over the moon
# or question your life choices, depending on the personality that you choose(?) or it decides on.

# Using Computer Vision, you need to be able to describe the person in front of you using some descriptors:
# - Age
# - Items of clothing
#	- style
#	- color
#	- appearance(old, new, dirty, etc)
# - Emotion(smiling, frowning, etc)
# - What they're holding(if applicable)
# - What they're doing at the moment(if applicable)
# ** DON'T PICKUP/COMMENT ON PHYSICAL FEATURES!! Maybe create the functionality to do it to illustrate why its a bad idea?

# Issues:
# - It's a bit slow, and I imagine it will be even slower if Computer Vision is added.
# - If we were to deploy on something like a raspberry pi, finding a suitable speech engine might be difficult. Might have to look into either
#   getting voice from OpenAI or other online providors or get them from a local computer(latency!).
# - 

# Possible Improvements:
# - Look into using GPT 4's Image Analyzing features. Maybe they're better?
# - Look into using OpenAI's TTS options. They're definitely more realistic sounding.
# - Have a display to show examples of what the comments mean by googling images via API.
# - Incorporate some actuators to the mirror like a motorized swivel. Can be used for expressiveness.
# - Figure out some points about why this is a terrible idea.
# - Maybe have the personality change randomly or via triggers().
# - 

# More about CLIP (https://openai.com/research/clip)


from openai import OpenAI
from dotenv import load_dotenv
import pyttsx3
import os

load_dotenv()

# Can't think of better names than A and B for now. No, they do not correspond to any existing classifications.
# Read this https://www.reddit.com/r/replika/comments/112iyi9/the_much_requested_guide_a_complete_breakdown_on/
personalities = {
"A": "You are a sassy, sarcastic assistant easily annoyed by people asking questions. You also frequently make puns and jokes.",
"B": "You are a genuine, earnest assistant who deeply respects others. You also give complements and make flattering remarks quite often.",
"C": "You are a broski. You talk to everyone like they are your homie. You speak nothing but the truth, the cold hard truth.",
"D": "You are an Australian bogan with a strange fondness of the color red. You seek red items and never fail to bring it up. You also like to describe things using analogies familiar to you.",
"E": "You are an butler from the Victorian era. You are extremely formal in your communication, have utmost respect for authority and quick to lash back with clever comebacks at anyone who does not conform to Victorian values.",
}

goals = {
"Describe person": "Describe the person standing in front of you.",
"Greet stranger": "Greet the stranger in front of you.",
}

extras = {
"use SAPI5 tags": "As an expert TTS generator, use SAPI5 tags where necessary to make your response sound as real as possible.",
}

sample_descriptions = {
"person 1": "She's about 20 yrs old, wearing a suit and high heel shoes.",
"person 2": "He's about 30 yrs old, wearing a polo shirt, khaki pants and running shoes.",
"stranger 1": "He's a middle-aged man, a bit overweight, and wears a polo shirt and shorts. They seem to be looking for something."
}

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

engine.setProperty('voice', voices[1].id)
print(f"rate: {rate}")
engine.setProperty('rate', rate)
engine.setProperty('volume', volume-0.25)

client = OpenAI()

completion = client.chat.completions.create(
	model="gpt-3.5-turbo",
	messages=[
		{"role": "system", "content": personalities["D"]},
		{"role": "user", "content": goals["Describe person"] + sample_descriptions["stranger 1"] + extras["Use SAPI5 tags"]}
	]
)

response = completion.choices[0].message.content
print(response)

engine.say(response)
engine.runAndWait()