# Import necessary libraries
import os
import discord
import config
from discord import app_commands
import json
import random
import gpt

# Get the guild ID from the environment variables
guild = discord.Object(id=os.getenv('GUILD_ID'))

# Open and load the slurs.json file
with open('slurs.json') as f:
    slurs_file = json.load(f)
slurs = slurs_file["slurs"]

# Define a custom client class


class MyClient(discord.Client):
    def __init__(self):
        # Initialize the client with the default intents
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def startup(self):
        # Wait until the client is ready
        await self.wait_until_ready()

    async def on_ready(self):
        # Sync the command tree with the guild when the client is ready
        if not self.synced:
            await tree.sync(guild=guild)
            self.synced = True
            print("Synced.")

        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return

        # Generate a random number
        x = random.randint(1, 100)

        # If the bot is mentioned and GPT is enabled
        if client.user in message.mentions and config.gpt_enabled:
            # If the message is a reply to the bot's message
            if message.reference and message.reference.resolved.author == self.user:
                assistant_message = {"role": "assistant",
                                     "content": message.reference.resolved.content}
                user_message = {"role": "user", "content": message.content}
                response, _, _ = gpt.send_message(
                    [assistant_message, user_message], model="gpt-4")
            else:
                user_message = {"role": "user", "content": message.content}
                response, _, _ = gpt.send_message(
                    [user_message], model="gpt-4")
            await message.channel.send(response)
        # If the random number is less than or equal to 3, reply with a random slur
        elif x <= 3:
            await message.reply(random.choice(slurs))


# Create an instance of the custom client
client = MyClient()

# Create a command tree for the client
tree = app_commands.CommandTree(client)

# Define a command for the command tree
@tree.command(name="gay", description="Command description.", guild=guild)
async def commandName(interaction: discord.Interaction, member: discord.Member = None):
    # Send a message when the command is used
    await interaction.response.send_message("Matthew")

@tree.command(name="Translator", description="Command description.", guild=guild)
async def commandName(interaction: discord.Interaction, member: discord.Member = None):
    # Send a message when the command is used
    await interaction.response.send_message("Work in progress!!!")

# Run the client with the bot token from the environment variables
client.run(os.getenv('BOT_TOKEN'))
