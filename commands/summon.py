from discord import Interaction, User
from random import choice
from typing import List


async def summon(interaction: Interaction, user: User) -> None:
    with open("constants/summoning_gifs.txt","r") as file:
        data: List[str] = file.readlines()
    await interaction.response.send_message(choice(data))
    await interaction.followup.send(f"<@{user.id}>")
