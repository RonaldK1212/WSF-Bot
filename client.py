# Import necessary libraries
import config
import discord
import funcs
import logger
import message_sender
import slash_commands
from discord import app_commands

# Get the guild ID from the environment variables
guild = discord.Object(id=config.guild_id)


# Define a custom client class
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.users_dict = funcs.initialize_user_dict()
        self.user_id_of_last_message = None
        self.number_of_spammed_messages = 0

    async def startup(self):
        await self.wait_until_ready()

    async def on_ready(self):
        try:
            if not client.synced:
                await tree.sync(guild=guild)
                client.synced = True
                print("Synced.")
                print("Logged in as", client.user.name)
                print("Client ID:", client.user.id)
                print(f"Bot is now logging to channel {config.logging_channel_id}")
                print("-----------------------------------")
                await logger.running_log(client)

        except discord.ConnectionError:
            print("Failed to connect to Discord.")
        except Exception as e:
            print(f"An error occurred during connection: {str(e)}")

    async def on_message(self, message):
        # Get the user ID of the current message
        user_id = message.author.id

        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return

        # ChatGPT reply
        if client.user in message.mentions and config.gpt_reply_toggled:
            await message_sender.send_chatgpt_reply(self, message)

        # Random slur reply
        if config.slur_reply_toggled:
            await message_sender.send_random_slur(self, user_id, message)


# Create an instance of the custom client
client = MyClient()

# Create a command tree for the client
tree = app_commands.CommandTree(client)


# Gay command
@tree.command(name="gay", description="Find out who is gay", guild=guild)
async def gay(interaction: discord.Interaction):
    await slash_commands.gay(interaction)


# Translator command
@tree.command(
    name="translator", description="Translate from Arabic to English", guild=guild
)
@app_commands.choices(word=slash_commands.load_translator_data()[0])  # words data
@app_commands.choices(
    description=slash_commands.load_translator_data()[1]
)  # description data
# @app_commands.autocomplete(word = slash_commands.word_autocompletion)
async def translator(
    interaction: discord.Interaction,
    word: app_commands.Choice[str],
    description: app_commands.Choice[str],
):
    await slash_commands.translator(interaction, word.name, description.name)
