from main import *
import discord
from discord.ext import commands
import Embed

class events(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def credits(self, ctx):
		embedVar = Embed.embed("Credits", "UnLonely Bot was created by ``soapyou#7743`` and ``ChillPanda#5842``. Thank you ``Sarah_TheDiscordKoala#8679`` for coming up with the original idea.")
		await ctx.send(embed=embedVar)

	@commands.command()
	async def help(self, ctx, *args):
		embedVar = Embed.embed("Help Section", "``u!help``: This message.\n``u!options``: Interact with the bot! (You can also ping instead of using this)\n``u!joke``: Hear a joke!\n``u!end``: Use this while chatting to end chatting (or just say ``end``!)\n ``u!github``: Link to GitHub repository\n``u!credits``: Displays the credits and people involved.")
		await ctx.send(embed=embedVar)
	
	@commands.command()
	async def github(self, ctx):
		embedVar = Embed.embed("GitHub Repository", "https://github.com/ChillPanda100/Un-Lonely")
		await ctx.send(embed=embedVar)

def setup(client):
	client.add_cog(events(client))
