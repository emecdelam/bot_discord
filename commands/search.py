from typing import Optional,Dict,List,Union
from googlesearch import search as gsearch
from discord import Interaction,Embed,Color,ButtonStyle,ui,Message, app_commands
from discord.ui import Button,View
from feature import BotFeature
class Search(BotFeature):
    def __init__(self, client):
        super().__init__(client)
        @client.tree.command()
        @app_commands.describe(
            content = "the query to search",
            num_results = 'the number of different results'
        )
        async def search(interaction: Interaction,content: str,num_results: Optional[int] = 3):
            """Returns you the searches for a result, can't be less than 1"""
            await search__(interaction,content,num_results - 1)

class Buttons(View):
    def __init__(self,content: List[Dict[str,str]],original: Message,embed: Embed,*,timeout: int = None):
        super().__init__(timeout = timeout)
        self.content = content
        self.pointer = 0
        self.embed = embed
        self.original = original

    async def pointer_check(self,direction: int) -> None:
        if self.pointer + direction == 0:
            self.previous_button.disabled = True
            self.next_button.disabled = False
        elif self.pointer + direction == len(self.content) - 1:
            self.next_button.disabled = True
            self.previous_button.disabled = False
        else:
            self.previous_button.disabled = False
            self.next_button.disabled = False
        self.pointer += direction

    @ui.button(label = "Previous",style = ButtonStyle.blurple,emoji = '\u2B05',custom_id = 'prev')
    async def previous_button(self,interaction: Interaction,button: Button) -> None:
        await self.pointer_check(-1)
        self.embed = Embed(color = Color.blurple(),title = self.content[self.pointer]["title"],
                           description = self.content[self.pointer]["desc"])
        self.embed.add_field(name = "Link",value = self.content[self.pointer]["url"])
        await self.original.edit(embed = self.embed,view = self)
        await interaction.response.edit_message(view = self)

    @ui.button(label = "Next",style = ButtonStyle.blurple,emoji = '\u27A1',custom_id = 'next')
    async def next_button(self,interaction: Interaction,button: Button) -> None:
        await self.pointer_check(1)
        self.embed = Embed(color = Color.blurple(),title = self.content[self.pointer]["title"],
                           description = self.content[self.pointer]["desc"])
        self.embed.add_field(name = "Link",value = self.content[self.pointer]["url"])
        await self.original.edit(embed = self.embed,view = self)
        await interaction.response.edit_message(view = self)


async def search__(interaction: Interaction,query: str,num_results: Optional[int] = 5) -> None:
    embed: Embed = Embed(
        color = Color.blurple(),
        title = '**Searching**',
        description = '...'
    )
    await interaction.response.send_message(embed = embed)
    results: List[Dict[str,str]] | str = google_search(query,num_results = num_results)
    sent = await interaction.original_response()
    if type(results) == str:
        await sent.edit(content = f"It didn't go as planned, the error is :\n{results}")
        return

    buttons: Buttons = Buttons(list(results),sent,embed)
    buttons.previous_button.disabled = True
    if len(results) < 2:
        buttons.next_button.disabled =True
    await sent.edit(
        embed = Embed(color = Color.blurple(),title = results[0]["title"],description = results[0]["desc"]).add_field(
            name = "Link",value = results[0]["url"]),view = buttons)


def google_search(query: str,num_results: int) -> Union[str,List[Dict[str,str]]]:
    if num_results < 1:
        num_results = 1
    try:
        results = gsearch(query,num_results = num_results,advanced = True)
        returned: List[Dict[str,str]] = []
        for i,result in enumerate(results):
            returned.append({"title":result.title,"desc":result.description,"url":result.url})
        return returned
    except Exception as e:
        return f"An error occurred: {e}"
