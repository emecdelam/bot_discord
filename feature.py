from discord import Message
class BotFeature:
    def __init__(self, client):
        self.client = client
    async def on_message_event(self, message: Message):
        pass
    async def on_ready(self):
        pass