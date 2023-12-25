from discord import Interaction,Embed,Color,ui, ButtonStyle
import time


async def ping(interaction: Interaction) -> None:
    embed = Embed(
        color = Color.blurple(),
        title = '**Response time**',
        description = 'pinging the server')
    start_time = time.time()
    await interaction.response.send_message(ephemeral = False,embed = embed)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    message = await interaction.original_response()
    await message.edit(embed = Embed(
        color = Color.green(),
        title = "**Response time**",
        description = f"responded in :\n\n{response_time:.4f} ms\n\n{response_time / 1000:.4f} s\n\n{response_time / 60000:.4f} m",
    ),view = ui.View().add_item(ui.Button(label = "\U0001F4A5 Stop",style = ButtonStyle.red))
    )
