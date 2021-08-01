import discord

# Hex code for lime
colorEmbed = 0x00ff00

def embed(header, desc):

	# The arguments needed for the embed
	embedVar = discord.Embed(title = header, description = desc, color = colorEmbed) 
	
	return embedVar
