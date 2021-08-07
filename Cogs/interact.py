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

chatbot = ChatBot("UnLonely", logic_adapters=[
	"chatterbot.logic.BestMatch",
	"chatterbot.logic.MathematicalEvaluation",
	])

starter_conversation = ["wassup!", "hello there!", "yo"]

end_words = ["bye", "gtg", "cya", "goodbye", "u!end", "end"]

chatbot.set_trainer(ChatterBotCorpusTrainer)

chatbot.train("chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")

chatbot.set_trainer(ListTrainer)

chatbot.train(random_talk)

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
			await message.reply(bot_approach, mention_author=False)	
		
		if content == '1' or content.startswith('joke'):
			await channel.send(random_joke())

		if content.startswith("chat") or content.startswith("u!chat") or content.startswith("3"):
			await message.reply(random.choice(starter_conversation), mention_author=False)
			while True:
				still_talking = True

				# Checks if the message was sent by the author and is in the same channel
				def check(msg):
					return msg.author == message.author and msg.channel == channel

				# Waits for a response	
				msg = await client.wait_for('message', check=check)

				msg_content = msg.content.lower()

				# Ends the conversation if any of the words in end_words appears in the message
				for word in end_words:
					if word in msg_content:
						await msg.reply("alrighty, thanks for talking!", mention_author=False)
						still_talking = False
						break
				
				if not still_talking:
					break

				if msg_content.startswith("u!chat") or msg_content.startswith("chat") or msg_content.startswith("3"):
					await msg.reply("Cannot have two chats active at same time. Closing chat.", mention_author=False)
					break

				# The chatbot processes the input and sends back a message
				response = chatbot.get_response(msg.content)
				await msg.reply(response, mention_author=False)

				print(f'User: {msg.content}')
				print(f'Un-Lonely: {response}')
				print(str(msg.author) + "\n")

		# Prevents '@client.event' from blocking the commands being used
		await client.process_commands(message)

	@commands.command(aliases=["interact"])
	async def options(self, message):
		await message.reply(bot_approach, mention_author=False)

	@commands.command()
	async def joke(self, message):
		await message.channel.send(random_joke())

def setup(client):
	client.add_cog(events(client))
