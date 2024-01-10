from discord import Client,Intents,app_commands


class MyClient(Client):
    def __init__(self,*,intents: Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild in self.guilds:
            self.tree.copy_global_to(guild = guild)
            await self.tree.sync(guild = guild)