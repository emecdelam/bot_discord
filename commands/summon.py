from discord import Interaction, User, app_commands
from random import choice
from typing import List
from feature import BotFeature
class Summon(BotFeature):
    def __init__(self, client):
        super().__init__(client)

        @client.tree.command()
        @app_commands.describe(
            user = "the user to summon"
        )
        async def summon(interaction: Interaction,user: User):
            """Summons a person"""
            await summon__(interaction,user)

async def summon__(interaction: Interaction, user: User) -> None:
    with open("constants/summoning_gifs.txt","r") as file:
        data: List[str] = file.read().splitlines()
    await interaction.response.send_message(choice(data))
    await interaction.followup.send(f"<@{user.id}>")
