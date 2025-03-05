from discord import Interaction
from random import choice
from typing import List
from feature import BotFeature
from logging_system import log__, Level

class Dodo(BotFeature):
    def __init__(self, client):
        super().__init__(client)
        @client.tree.command()
        async def dodo(interaction: Interaction):
            """Responds with a sleep gif"""
            await log__(f"Dodo called by : {interaction.user.name}", Level.INFO)
            await dodo__(interaction)

async def dodo__(interaction: Interaction) -> None:
    with open("constants/sleep_gifs.txt","r") as file:
        data: List[str] = file.read().splitlines()
    await interaction.response.send_message(choice(data))