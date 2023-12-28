from os import getenv
from typing import Optional

from discord import Client,app_commands,Intents,Interaction,User

from commands import ping__,summon__, search__
from logging_system import Colors,Level,log__


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


@client.event
async def on_ready():
    await log__(f"Attempting a connection",Level.INFO,Colors.lightblue)
    print(
        """██████╗░░█████╗░░█████╗░████████╗██╗███╗░░██╗░██████╗░░░░░░░░░░░░\n██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║████╗░██║██╔════╝░░░░░░░░░░░░\n██████╦╝██║░░██║██║░░██║░░░██║░░░██║██╔██╗██║██║░░██╗░░░░░░░░░░░░\n██╔══██╗██║░░██║██║░░██║░░░██║░░░██║██║╚████║██║░░╚██╗░░░░░░░░░░░\n██████╦╝╚█████╔╝╚█████╔╝░░░██║░░░██║██║░╚███║╚██████╔╝░░██╗██╗██╗\n╚═════╝░░╚════╝░░╚════╝░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░░░╚═╝╚═╝╚═╝""")
    await client.setup_hook()
    await log__(f"Logged in as {client.user}",Level.INFO,Colors.lightgreen)


@client.tree.command()
async def ping(interaction: Interaction):
    """Gives you the response time"""
    await ping__(interaction)


@client.tree.command()
@app_commands.describe(
    user = "the user to summon"
)
async def summon(interaction: Interaction,user: User):
    """Summons a person"""
    await summon__(interaction,user)
@client.tree.command()
@app_commands.describe(
    content = "the query to search",
    num_results='the number of different results'
)
async def search(interaction: Interaction,content:str,num_results:Optional[int]=3):
    """Returns you the searches for a result"""
    await search__(interaction,content,num_results-1)

# Main loop starts here
client.run(getenv('DISCORD_BOT_TOKEN'))
