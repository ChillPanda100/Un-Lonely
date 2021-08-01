import discord
import os
import discord.ext
import asyncio
import requests
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import keep_alive

client = discord.Client()
client = commands.Bot(help_command = None, command_prefix="u!")

@client.event
async def on_ready():
	keep_alive.keep_alive()
	print("Bot is online")
	stat = discord.Game("u!help")
	
	# Displays the bot status as "Playing help"
	await client.change_presence(status=discord.Status.online, activity=stat)

# Function for ignoring CommandNotFound error
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    return

for file in os.listdir('./Cogs'):
	if file.endswith(".py"):

		# Loads all the .py files in the folder "Cogs"
		client.load_extension(f'Cogs.{file[:-3]}') 
		
		print(file[:-3] + " is working")

# Retrieves token
client.run(os.getenv('TOKEN'))
