from feature import BotFeature
from discord import Interaction, app_commands
from discord.ui import UserSelect, View
from re import compile
from .assignment import Assignment
class Add(BotFeature):
    def __init__(self, client):
        super().__init__(client)

        @client.tree.command()
        @app_commands.describe(
            exercise_name = 'the exercise name formatted like this : {course code} [{number}] ex : lepl1106 [2]',
            due_date = 'the due date, like this : "2024-01-08 14:30"'
        )
        async def add(interaction: Interaction, exercise_name:str, due_date:str):
            """Add an exercise as to be done formatted like this : {course code} [{number}] ex : lepl1106 [2]"""
            if await is_valid_date_time_format(due_date):
                await add__(interaction,exercise_name,due_date)
            else:
                await interaction.response.send_message('invalid time format it should be like this: `2024-01-08 14:30`',ephemeral=True)
async def add__(interaction:Interaction,exercise_name,due_date):
    user_select = UserSelect(
        placeholder = "Select user(s)",
        max_values = 25
    )
    async def callback(interaction:Interaction):
        users = user_select.values
        assignment = Assignment(exercise_name,due_date,users)
        await assignment.save()
        await interaction.response.send_message("Assignment added",ephemeral = True)
    user_select.callback = callback
    view:View = View()
    view.add_item(user_select)
    sent = await interaction.response.send_message("Choose who to add to the assignment",view = view)
async def is_valid_date_time_format(input_string):
    pattern = compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')
    return bool(pattern.match(input_string))
