import discord
import config
from discord import app_commands
import json
import random
import gpt

guild = discord.Object(id=config.guildID)

with open('slurs.json') as f:
    slurs_file = json.load(f)
slurs = slurs_file["slurs"]


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def startup(self):
        await self.wait_until_ready()

    async def on_ready(self):
        # await tree.sync(guild=guild)

        if not self.synced:
            await tree.sync(guild=guild)
            self.synced = True
            print("Synced.")

        print(f'Logged on as {self.user}!')

        if not self.synced:
            await tree.sync(guild=guild)
            self.synced = True
            print("Synced.")

    async def on_message(self, message):
        if message.author == self.user:
            return
        x = random.randint(1, 100)

        if client.user in message.mentions and config.gpt_enabled:  # if the bot is mentioned
            response, _, _ = gpt.send_message(message.content)
            await message.channel.send(response)
        elif x <= 10:
            await message.reply(random.choice(slurs))


client = MyClient()
tree = app_commands.CommandTree(client)


@tree.command(name="gay", description="Command description.", guild=guild)
async def commandName(interaction: discord.Interaction, member: discord.Member = None):
    await interaction.response.send_message("Matthew")


@tree.command(name="les", description="Command description.", guild=guild)
async def commandName(interaction: discord.Interaction, member: discord.Member = None):
    await interaction.response.send_message("Matthew")


client.run(config.token)
