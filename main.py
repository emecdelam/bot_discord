from dotenv import load_dotenv
import asyncio
import logging
from os import getenv
from discord import Intents,RawReactionActionEvent
from feature import BotFeature
from commands import *
from logging_system import log__,Colors,Level
from client import MyClient
import tracemalloc
from pathlib import Path


load_dotenv(dotenv_path=Path('.env'))
tracemalloc.start()


logger = logging.getLogger()
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('error.log')
logger.addHandler(file_handler)

intents = Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.reactions = True
client = MyClient(intents = intents)

features: list[BotFeature] = [Ping(client),Summon(client),Search(client),Thread(client), Ask(client), Dodo(client)]

@client.event
async def on_ready():
    await log__(f"Attempting a connection",Level.INFO,Colors.lightblue)
    print(
        """██████╗░░█████╗░░█████╗░████████╗██╗███╗░░██╗░██████╗░░░░░░░░░░░░\n██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║████╗░██║██╔════╝░░░░░░░░░░░░\n██████╦╝██║░░██║██║░░██║░░░██║░░░██║██╔██╗██║██║░░██╗░░░░░░░░░░░░\n██╔══██╗██║░░██║██║░░██║░░░██║░░░██║██║╚████║██║░░╚██╗░░░░░░░░░░░\n██████╦╝╚█████╔╝╚█████╔╝░░░██║░░░██║██║░╚███║╚██████╔╝░░██╗██╗██╗\n╚═════╝░░╚════╝░░╚════╝░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░░░╚═╝╚═╝╚═╝""")
    await client.setup_hook()
    await log__(f"Initializing classes",Level.INFO,Colors.lightblue)
    [await x.on_ready() for x in features]
    await log__(f"Logged in as {client.user}",Level.INFO,Colors.lightgreen)
    await asyncio.gather(await client.setup_hook())


@client.event
async def on_message(message):
    [await x.on_message_event(message) for x in features]

@client.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    [await x.on_raw_reaction_add(payload) for x in features]

@client.event
async def on_raw_reaction_remove(payload: RawReactionActionEvent):
    [await x.on_raw_reaction_remove(payload) for x in features]



file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)

client.run(getenv('DISCORD_BOT_TOKEN'), log_handler=file_handler)
