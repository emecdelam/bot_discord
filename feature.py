from discord import Message, RawReactionActionEvent
from client import MyClient
class BotFeature:
    def __init__(self, client:MyClient):
        self.client = client
    async def on_ready(self):
        pass
    async def on_message_event(self, message: Message):
        pass
    async def on_raw_reaction_add(self,payload: RawReactionActionEvent):
        pass

    async def on_raw_reaction_remove(self,payload: RawReactionActionEvent):
        pass