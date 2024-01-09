from os import getenv
from discord import Client,app_commands,Intents
from feature import BotFeature
from commands import Ping,Summon,Search
from logging_system import log__,Colors,Level
from ex_reminder import Add,Done


class MyClient(Client):
    def __init__(self,*,intents: Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild in self.guilds:
            self.tree.copy_global_to(guild = guild)
            await self.tree.sync(guild = guild)


intents = Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.reactions = True
client = MyClient(intents = intents)

features: list[BotFeature] = [Ping(client),Summon(client),Search(client),Add(client),Done(client)]

@client.event
async def on_ready():
    await log__(f"Attempting a connection",Level.INFO,Colors.lightblue)
    print(
        """██████╗░░█████╗░░█████╗░████████╗██╗███╗░░██╗░██████╗░░░░░░░░░░░░\n██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║████╗░██║██╔════╝░░░░░░░░░░░░\n██████╦╝██║░░██║██║░░██║░░░██║░░░██║██╔██╗██║██║░░██╗░░░░░░░░░░░░\n██╔══██╗██║░░██║██║░░██║░░░██║░░░██║██║╚████║██║░░╚██╗░░░░░░░░░░░\n██████╦╝╚█████╔╝╚█████╔╝░░░██║░░░██║██║░╚███║╚██████╔╝░░██╗██╗██╗\n╚═════╝░░╚════╝░░╚════╝░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░░░╚═╝╚═╝╚═╝""")
    await client.setup_hook()
    await log__(f"Initializing classes",Level.INFO,Colors.lightblue)
    [await x.on_ready() for x in features]
    await log__(f"Logged in as {client.user}",Level.INFO,Colors.lightgreen)
@client.event
async def on_message(message):
    [await x.on_message_event(message) for x in features]


# Main loop starts here
client.run(getenv('DISCORD_BOT_TOKEN'))
