from discord import Interaction,Embed,Color,ButtonStyle,InteractionMessage
from discord.ui import Button,View
import time


async def ping(interaction: Interaction) -> None:
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

    view: View = View(timeout = 120).add_item(
        Button(label = "Delete",style = ButtonStyle.red,emoji = '\U0001F4A5',custom_id = "delete_button"))
    view.callback = lambda interaction, button: interaction.message.delete() if button.custom_id == "delete_button" else None

    await message.edit(embed = Embed(
        color = Color.green(),
        title = "**Response time**",
        description = f"responded in:\n\n{response_time:.4f} ms\n\n{response_time / 1000:.4f} s\n\n{response_time / 60000:.4f} m",
    ),view = view)
