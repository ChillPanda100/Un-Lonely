from main import *
import requests
import json
import random
import discord
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from talk import random_talk

bot_approach = "wussup its ur friend lonely bot here to help u not get lonely. wut do u wanna talk about or hear?\n 1. joke\n 2. video (NOT AVAILABLE RIGHT NOW)\n 3. chat"

chatbot = ChatBot("UnLonely", logic_adapters=["chatterbot.logic.BestMatch"])

starter_conversation = ["wassup!", "hello there!", "yo"]

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")
chatbot.set_trainer(ListTrainer)
chatbot.train(random_talk)

end_words = ["bye", "gtg", "cya", "goodbye"]

def random_joke():
	# Gets the dictionary from the website
	get_joke = requests.get("https://official-joke-api.appspot.com/random_joke")

	JSONData = json.loads(get_joke.text)

	# Variable for the joke that will be seen by the user
	final_joke = ""

	# If the key corresponds to the joke or punchline, it will concatenate the value to the final_joke variable
	for key, value in JSONData.items():
		if key == 'setup':
			# Adds the joke to the variable followed by two newlines
			final_joke += value + "\n" + "\n"
		if key == 'punchline':
			# Adds the punchline after the joke is added
			final_joke += value
	
	return final_joke

class events(commands.Cog):
	def __init__(self, client):
		self.client = client

	@client.event
	async def on_message(message):
		content = message.content
		channel = message.channel
		if client.user.mentioned_in(message):
			await channel.send(bot_approach)	
		
		if content == '1' or content.startswith('joke'):
			await channel.send(random_joke())
		is_chatting = False
		if content.startswith("chat") or content.startswith("u!chat") or content == '3':
			await channel.send(random.choice(starter_conversation))
			while True:
				# Checks if the message was sent by the author and is in the same channel
				def check(msg):
					return msg.author == message.author and msg.channel == channel

				# Waits for a response	
				msg = await client.wait_for('message', check=check)

				# Ends the conversation if the message startswith "end" or "u!end"
				if msg.content.startswith("end") or msg.content.startswith("u!end"):
					await channel.send("thanks for chatting with me, bye now!")
					break

				if msg.content.startswith("3") or msg.content.startswith("chat"):
					await channel.send("Cannot have two chats active at same time. Closing chat.")
					break
				
				if msg.content in end_words:
					await channel.send("alrighty, thanks for talking!")
					break

				# The chatbot processes the input and sends back a message
				response = chatbot.get_response(msg.content)
				await channel.send(response)

		# Prevents '@client.event' from blocking the commands
		await client.process_commands(message)

	@commands.command(aliases=["interact"])
	async def options(self, message):
		await message.channel.send(bot_approach)

	@commands.command()
	async def joke(self, message):
		await message.channel.send(random_joke())

def setup(client):
	client.add_cog(events(client))
