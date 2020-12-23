# bot.py
import os
import discord
from dotenv import load_dotenv
import requests
import json
import random
from replit import db
from keep_alive import keep_alive




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

special__sad_words = ["crystal", "love", "idfk this shit wont work"]

sad_words = ["suicide", "Kill myself", "depressed", "single and sad", "depression", "broke up with me", "kms", "kys", "unhappy", "virgin", "sad"]

inspiring_words = ["Hang in there.", "Don't give up.", "Keep pushing.", "Stay strong."]

special_inspiring_words=["Never let a bad person change your inner goodness.", 
"Sadness flies away on the wings of time.", "The truth is, unless you let go, unless you forgive yourself, unless you forgive the situation, unless you realize that the situation is over, you cannot move forward."]


if "responsing" not in db.keys():
	db["responding"] = True

def get_quote():
	response = requests.get("https://zenquotes.io/api/random"
	)
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return(quote)


def updateE(inspiring_message):
	if "encouragments" in db.keys():
		encouragments = db['encouragments']
		encouragments.append(inspiring_message)
		db["encouragments"] = encouragments
	else:
		db["encouragments"] = [inspiring_message]

def dE(index):
	encouragments = db["encouragments"]
	if len(encouragments) > index:
		del encouragments[index]
		db["encouragments"] = encouragments

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

	if message.author == client.user:
		return

	msg = message.content
	
	if message.content.startswith('!fuckbrandon'):
		await message.channel.send("Fuckin piece of shit skinny fuck. Brandon is why my lord is single")
	
	if message.content.startswith('!egoboost'):
		quote = get_quote()
		await message.channel.send(quote)

	if db["responding"]:
		options = inspiring_words
		if "encouragments" in db.keys():
			options = options + db["encouragments"]

	if any(word in msg for word in sad_words):
		await message.channel.send(random.choice(options))

	s_options = special_inspiring_words
	if "encouragments" in db.keys():
		s_options = s_options + db["encouragments"]

	if any(word in msg for word in special__sad_words):
		await message.channel.send(random.choice(s_options))

	if msg.startswith("$new"):
		inspiring_message = msg.split("$new ",1)[1]
		updateE(inspiring_message)
		await message.channel.send("New Ego Boost comment added.")

	if msg.startswith("$del"):
		encouragments = []
		if "encouragments" in db.keys():
			index = int(msg.split("$del",1)[1])
			dE(index)
			encouragments = db["encouragments"]
		await message.channel.send(encouragments)

	if msg.startswith("$list"):
		encouragments = []
		if "encouragments" in db.keys():
			encouragments = db["encouragments"]
		await message.channel.send(encouragments)

	if msg.startswith("$responding"):
		value = msg.split("$responding ",1)[1]

		if value.lower() == "true":
			db["responding"] = True
			await message.channel.send("I am on. ")
		else:
			db["responding"] = False
			await message.channel.send("i am off")

keep_alive()
client.run(TOKEN)
