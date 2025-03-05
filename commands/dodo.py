from discord import Interaction
from random import choice
from typing import List
from feature import BotFeature


class Dodo(BotFeature):
    def __init__(self, client):
        super().__init__(client)
        @client.tree.command()
        async def dodo(interaction: Interaction):
            """Responds with a sleep gif"""
            await dodo__(interaction)

async def dodo__(interaction: Interaction) -> None:
    with open("constants/sleep_gifs.txt","r") as file:
        data: List[str] = file.read().splitlines()
    await interaction.response.send_message(choice(data))