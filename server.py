import discord
import asyncio

TOKEN = 'NDQ1NjUwNDc2NDM2ODE1ODkz.Ddtj7Q.9AmZpLZxE1NnyjUq-R9gXIxntCM'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("Hello"):
    	yield from client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
