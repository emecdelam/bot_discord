from feature import BotFeature
from discord import Interaction, app_commands
from logging_system import log__,Level
import json
class Done(BotFeature):
    def __init__(self, client):
        super().__init__(client)

        @client.tree.command()
        @app_commands.describe(
            exercise_name = 'the exercise name formatted like this : {course code} [{number}] ex : lepl1106 [2]',
        )
        async def done(interaction: Interaction, exercise_name:str):
            """Sets an exercise to done formatted like this : {course code} [{number}] ex : lepl1106 [2]"""
            await done__(interaction,exercise_name)
async def done__(interaction:Interaction,exercise_name:str):
    try:
        with open("ex_reminder\\ongoing_assignments.json","r") as file:
            data = json.load(file)
        if exercise_name.lower() not in map(str.lower, data.keys()):
            await interaction.response.send_message(f"Assignment not found, available assignments are \n{list(data.keys())}")
            return
        if str(interaction.user.id) not in data[exercise_name]["users"].keys():
            await interaction.response.send_message(f"You were not assigned to this exercise, you can assign yourself by editing the assignment")
            return
        data[exercise_name]["users"][str(interaction.user.id)] = "True"
        with open("ex_reminder\\ongoing_assignments.json","w") as file:
            json.dump(data,file,indent = 4)
        await interaction.response.send_message("Dopamine shot? maybe you should do another exercise ¯\_(ツ)_/¯")
        return
    except Exception as e:
        await log__(f"Couln't read data\n{e}",Level.ERROR)
