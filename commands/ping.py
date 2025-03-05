from discord import Interaction,Embed,Color,ButtonStyle,InteractionMessage
from discord.ui import Button,View
from feature import BotFeature
import time

class Ping(BotFeature):
    def __init__(self, client):
        super().__init__(client)
        @client.tree.command()
        async def ping(interaction: Interaction):
            """Gives you the response time"""
            await ping__(interaction)
async def ping__(interaction: Interaction) -> None:
    embed: Embed = Embed(
        color = Color.blurple(),
        title = '**Response time**',
        description = 'pinging the server'
    )
    start_time: float = time.time()
    await interaction.response.send_message(embed = embed)
    message: InteractionMessage = await interaction.original_response()
    end_time: float = time.time()
    response_time: float = (end_time - start_time) * 1000

    await message.edit(
        embed=Embed(
            color=Color.green(),
            title="**Response time**",
            description=f"Responded in:\n\n{response_time:.4f} ms\n\n{response_time / 1000:.4f} s\n\n{response_time / 60000:.4f} m",
        )
    )
