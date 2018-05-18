import discord
import json
import requests
import re
import random

TOKEN = 'NDQ1NjUwNDc2NDM2ODE1ODkz.Ddtj7Q.9AmZpLZxE1NnyjUq-R9gXIxntCM'
nick = 'vqgXph15'


def createSession():
    body = {
        'user': 'YNWnSHCuFnDun5iV',
        'key': 'fzcVpXJjZBb3av3dwDAoBSXEY6iX5ulR'
    }
    req = requests.post('https://cleverbot.io/1.0/create', json=body)
    req = json.loads(req.text)
    print("Nick: {}".format(req['nick']))
    return req['nick']


def sendMessage(message):
    body = {
        'user': 'YNWnSHCuFnDun5iV',
        'key': 'fzcVpXJjZBb3av3dwDAoBSXEY6iX5ulR',
        'nick': nick,
        'text': message
    }

    r = requests.post('https://cleverbot.io/1.0/ask', json=body)
    r = json.loads(r.text)
    if r['status'] == 'success':
        return r['response']
    else:
        return r


talking = {}
commands = {}
client = discord.Client()

ee_0xcpu = []

def cmd_talk(message):
    talking[str(message.author)] = True
    print(talking)
    return 'Started talking to Cleverbot. To stop type `cvb stop`'


def cmd_stop(message):
    talking[str(message.author)] = False
    print(talking)
    return 'Stopped talking to Cleverbot. To talk again type `cvb talk`'


def cmd_help(message):
    retMsg = 'All Cleverbot commands start with cvb:\n'
    for command in commands:
        retMsg += '`cvb {}` - {}\n'.format(commands[command]['cmd'], commands[command]['desc']) if commands[command]['shown'] is True else ''
    return retMsg


def cmd_info(message):
    return 'Cleverbot is a chatterbot web application that uses an artificial intelligence algorithm to have conversations with humans.'


def cmd_0xcpu(message):
    return ee_0xcpu[random.randrange(0, len(ee_0xcpu))]


def add_command(name, desc, shown, func):
    commands[name] = {}
    commands[name]['func'] = func
    commands[name]['cmd'] = name
    commands[name]['desc'] = desc
    commands[name]['shown'] = shown


def init():
    add_command('talk', 'start talking with Cleverbot', cmd_talk, True)
    add_command('stop', 'stop talking to Cleverbot', cmd_stop, True)
    add_command('help', 'print this help message', cmd_help, True)
    add_command('info', 'details about Cleverbot', cmd_info, True)
    add_command('0xcpu', 'dunno', cmd_0xcpu, False)
    
    ee_0xcpu.append('i put 0xcpu it give flag')
    ee_0xcpu.append('i put 0xcpu it dont work')
    ee_0xcpu.append('rumor has it that b64 bruteforce is still running')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('cvb'):
        if not str(message.channel).startswith("cleverbot"):
            await client.send_message(message.channel,
                                      "Cleverbot can only be used in a text channel named `cleverbot`.")
        else:
            command = ''
            try:
                command = re.match('cvb (.*[a-zA-Z0-9])', message.content).group(1)
                resp = commands[command]['func'](message)
                if resp != '':
                    await client.send_message(message.channel, resp)
            except:
                await client.send_message(message.channel,
                                          "Command `cvb {}` not found. Try `cvb help` for a list of commands.".format(
                                              command))
    else:
        if str(message.author) in talking.keys() and talking[str(message.author)] == True:
            cleverResponse = sendMessage(message.content)
            await client.send_message(message.channel, "{}, {}".format(message.author.mention, cleverResponse))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # print(client.server.id)
    print('------------')
    # print('Server name: {}'.format(server.name))
    init()
    await client.change_presence(game=discord.Game(name='cvb help'))

client.run(TOKEN)
