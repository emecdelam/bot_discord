from typing import Dict
import asyncpg
from discord.ext import tasks
from discord import Interaction,TextChannel,RawReactionActionEvent,Message,Member,Embed,Color,app_commands
from feature import BotFeature
from datetime import time
from datetime import timezone
from datetime import datetime
import pickle
from client import MyClient
from logging_system import log__,Level

class Streak(BotFeature):
    times = [time(hour = 0,minute = 0,tzinfo = timezone.utc)]

    def __init__(self,client: MyClient):
        super().__init__(client)
        self.daily_message.add_exception_type(asyncpg.PostgresConnectionError)
        self.channel = None
        self.messages: Dict[Message.id,Dict[Member.id,bool]] = {}
        self.debts = {}
        self.paid = {}
        @client.tree.command()
        async def start_streaks(interaction: Interaction):
            """Reset task loop for current streak"""
            if await self.is_admin(interaction):
                self.channel = interaction.channel
                await interaction.response.send_message("started streaks",ephemeral = True)
                await self.daily_message.start()
                return
            await interaction.response.send_message("missing persmission",ephemeral = True)

        @client.tree.command()
        async def channel_streaks(interaction: Interaction,channel: TextChannel):
            """Stops the task loop for current streaks"""
            if await self.is_admin(interaction):
                self.channel = channel
                await interaction.response.send_message("new channel done",ephemeral = True)
                return
            await interaction.response.send_message("missing persmission",ephemeral = True)

        @client.tree.command()
        async def end_streaks(interaction: Interaction):
            """Stops the task loop for current streaks"""
            if await self.is_admin(interaction):
                self.daily_message.cancel()
                await interaction.response.send_message("ended streaks",ephemeral = True)
                return
            await interaction.response.send_message("missing persmission",ephemeral = True)

        @client.tree.command()
        async def reset_streaks(interaction: Interaction):
            """Stops the task loop for current streaks"""
            if await self.is_admin(interaction):
                pickle.dump(self.messages,open("db\\streak_backup.p","wb"))
                self.messages = {}
                await interaction.response.send_message("resetted streaks",ephemeral = True)
                return
            await interaction.response.send_message("missing persmission",ephemeral = True)
        @client.tree.command()
        async def streaks(interaction: Interaction, member:Member):
            """Show the user number of streaks"""
            self.messages = pickle.load(open("db\\messages.p","rb"))
            count = 0
            for message in self.messages.keys():
                if member.id not in self.messages[message].keys():
                    continue
                if self.messages[message][member.id]:
                    count+=1
                if not self.messages[message][member.id]:
                    count = 0
            await interaction.response.send_message(f"Your current streak is : \n# <a:flame2:1194658671892893716>   {count}   <a:flame2:1194658671892893716>")
        @client.tree.command()
        async def leaderboard(interaction: Interaction):
            """Show the podium for most number of streaks"""
            self.messages = pickle.load(open("db\\messages.p","rb"))
            score = {}
            for message in self.messages.keys():
                for user in self.messages[message].keys():
                    if self.messages[message][user]:
                        if user in score:
                            score[user] += 1
                        else:
                            score[user] = 1
                    else:
                        score[user] = 0
            score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
            desc = ""
            for user, streak in score.items():
                desc += f"<@{user}> : {streak} <a:flame2:1194658671892893716>\n\n"
            embed: Embed = Embed(
                color = Color.blurple(),
                title = '**Leaderboard**',
                description = desc
            )
            await interaction.response.send_message(embed=embed)

    async def on_ready(self) -> None:
        self.channel = self.client.get_channel(1120432504629895300)
    async def is_admin(self,interaction: Interaction) -> bool:
        member = await interaction.guild.fetch_member(interaction.user.id)
        return member.guild_permissions.moderate_members

    @tasks.loop(time = times)
    async def daily_message(self) -> None:
        if (datetime.now().weekday() > 4):
            return
        message:Message = await self.channel.send(
            "Hello, it's time to ~~have fun~~ work, have you already done everything there was to do today?\nIf you had"
            "n't any exercise, have understood the lecture?\nIf you hadn't any lecture, have you advanced in your group"
            " projects?\nIf you can't advance in your group project you migth consider doing summaries\nIf the "
            "summaries are already done you can do the exercises in advance "
            "or seeing the next chapter, going to a lecture with basic knowledge over the topic makes the lecture more"
            "relevant\nIf you can't advance any further, yo might consider preparing for the exam by redoing some "
            "exercises and reviewing important theory concepts")
        self.messages[message.id] = {}
        for member in self.channel.guild.members:
            if not member.bot:
                self.messages[message.id][member.id] = False
        await message.add_reaction('✅')
        pickle.dump(self.messages,open("db\\messages.p","wb"))


    async def on_raw_reaction_add(self,payload: RawReactionActionEvent) -> None:
        if payload.member.bot:
            return
        self.messages = pickle.load(open("db\\messages.p","rb"))
        if payload.message_id not in self.messages.keys():
            await log__(
                f"no message found (adding) in database :{payload.message_id} for messages : {self.messages.keys()}",
                Level.ERROR)
            return
        if payload.member.id not in self.messages[payload.message_id].keys():
            await log__(f"member not found when adding a reaction to :{payload.message_id} for member {payload.member.name}",Level.WARNING)
        self.messages[payload.message_id][payload.member.id] = True
        pickle.dump(self.messages,open("db\\messages.p","wb"))

    async def on_raw_reaction_remove(self,payload: RawReactionActionEvent) -> None:
        self.messages = pickle.load(open("db\\messages.p","rb"))
        if payload.message_id not in self.messages.keys():
            await log__(
                f"no message found (removing) in database :{payload.message_id} for messages : {self.messages.keys()}",
                Level.ERROR)
            return
        if payload.member is None:
            payload.member = await self.client.fetch_user(payload.user_id)
        if payload.member is None:
            await log__(f"Unable to fetch member for user ID: {payload.user_id}",Level.WARNING)
            return
        if payload.user_id not in self.messages[payload.message_id].keys():
            await log__(f"member not found when removing a reaction to: {payload.message_id} for member {payload.member.name}",
                        Level.WARNING)

        if payload.member.id not in self.messages[payload.message_id].keys():
            await log__(f"member not found when removing a reaction to :{payload.message_id} for member {payload.member.name}",Level.WARNING)
        self.messages[payload.message_id][payload.member.id] = False
        pickle.dump(self.messages,open("db\\messages.p","wb"))

