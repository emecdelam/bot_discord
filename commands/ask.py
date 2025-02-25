from os import getenv
from openai import OpenAI
from discord import Interaction, app_commands
from feature import BotFeature
from datetime import datetime
from logging_system import log__, Level
class Ask(BotFeature):
    def __init__(self, client):
        super().__init__(client)
        API = getenv('DEEPSEEK_API_KEY ')
        self.client = OpenAI(api_key=API, base_url="https://api.deepseek.com")
        @client.tree.command()
        @app_commands.describe(
            question='the content'
        )
        async def ask(interaction: Interaction, question:str):
            """Gives you the response time"""
            await ask__(interaction, question, self.client)
async def ask__(interaction: Interaction, question: str, client) -> None:
    await interaction.response.send_message(f"Processing since <t:{int(datetime.utcnow().timestamp())}:R>")
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
            await interaction.channel.send(chunk)
    except Exception as e:
        await interactionc.channel.send("An error occurred while contacting the DeepSeek API.")
        log__(f"Deepseek error", Level.INFO)