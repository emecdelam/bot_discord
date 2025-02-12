from os import getenv
from openai import OpenAI
from discord import Interaction, app_commands
from feature import BotFeature

class Ask(BotFeature):
    def __init__(self, client):
        super().__init__(client)
        self.client = OpenAI(api_key=getenv('DEEPSEEK_API_KEY '), base_url="https://api.deepseek.com")
        @client.tree.command()
        @app_commands.describe(
            question='the content'
        )
        async def ask(interaction: Interaction, question:str):
            """Gives you the response time"""
            await ask__(interaction, question, self.client)
async def ask__(interaction: Interaction, question: str, client) -> None:
    try:
        # Query the DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question},
            ],
            stream=False
        )
        answer = response.choices[0].message.content
        answer = answer.replace(r"\[", "$$").replace(r"\]", "$$").replace(r"\( ","$").replace(r" \)" ,"$")
        answer = answer.replace(r"\(","$").replace(r"\)" ,"$")
        for chunk in [answer[i:i+2000] for i in range(0, len(answer), 2000)]:
            await interaction.send(chunk)
    except Exception as e:
        await interaction.send("An error occurred while contacting the DeepSeek API.")
        print(f"Error: {e}")