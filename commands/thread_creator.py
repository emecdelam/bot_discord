from discord import Interaction,app_commands,TextChannel
from discord.app_commands import Choice
from typing import Optional
from feature import BotFeature
class Thread(BotFeature):
    def __init__(self, client):
        super().__init__(client)

        @client.tree.command()
        @app_commands.describe(
            channel='the channel to create the thread',
            name='the name of the course',
            year='the year of the exam',
            number='the auestion number'
        )
        @app_commands.choices(month=[
            Choice(name = "jan",value = "jan"),
            Choice(name = "feb",value = "feb"),
            Choice(name = "mar",value = "mar"),
            Choice(name = "apr",value = "apr"),
            Choice(name = "may",value = "may"),
            Choice(name = "jun",value = "jun"),
            Choice(name = "jul",value = "jul"),
            Choice(name = "aug",value = "aug"),
            Choice(name = "sep",value = "sep"),
            Choice(name = "oct",value = "oct"),
            Choice(name = "nov",value = "nov"),
            Choice(name = "dec",value = "dec")
        ])
        async def thread(interaction: Interaction,channel: TextChannel,name:str,month:Optional[Choice[str]]=None,year:Optional[str]=None,number:Optional[int]=None):
            """Creates a thread"""
            if month is not None:
                month = month.name
            await thread__(interaction,channel,name,month,year,number)

async def thread__(interaction: Interaction,channel: TextChannel,name:str,month:Optional[str]=None,year:Optional[str]=None,number:Optional[int]=None):
    res = name
    if month is not None:
        res += ' - '+month
    if year is not None:
        res +=" " + year
    if number is not None:
        res = f"[{number}] - "+res
    await channel.create_thread(name = res)
    await interaction.response.send_message("thread created",ephemeral = True)
    await channel.send("New thread created : "+res)