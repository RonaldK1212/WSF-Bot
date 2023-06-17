# Import necessary libraries
import os
import sys
import discord
import config
from discord import app_commands
import json
import message_sender

# Get the guild ID from the environment variables
guild = discord.Object(id=os.getenv("GUILD_ID"))

def initialize_user_dict():
    try:
        with open(os.path.join(sys.path[0], "users.json")) as f:
            users_file = json.load(f)
            users = users_file["users"]
        users_dict = {}
        for user in users:
            users_dict[int(user["member_id"])] = user["member_name"]
        return users_dict
        
    except FileNotFoundError:
        print("Error: Users file not found.")
    except PermissionError:
        print("Error: Insufficient permissions to access the slurs file.")
        
# Define a custom client class
class MyClient(discord.Client):
    def __init__(self):
        # Initialize the client with the default intents
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.users_dict = initialize_user_dict()    
        self.user_id_of_last_message = None
        self.number_of_spammed_messages = 0

    async def startup(self):
        # Wait until the client is ready
        await self.wait_until_ready()

    async def on_ready(self):
        try:
            # Sync the command tree with the guild when the client is ready
            if not self.synced:
                await tree.sync(guild=guild)
                self.synced = True
                print("Synced.")
                print('Logged in as', self.user.name)
                print('Client ID:', self.user.id)
                print(f"Bot is now logging to channel {config.logging_channel_id}")
                print('-----------------------------------')

                running_message = f"**# Alyssa started running \nSession logs:**"
                # Access the global logging channel ID
                logging_channel = self.get_channel(config.logging_channel_id)
                if logging_channel:
                    await logging_channel.send(running_message)
                
        except discord.ConnectionError:
            print("Failed to connect to Discord.")
        except Exception as e:
            print(f"An error occurred during connection: {str(e)}")
    
    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return

        # Get the user ID of the current message
        user_id = message.author.id
        
        # ChatGPT reply
        if client.user in message.mentions and config.gpt_enabled:
            await message_sender.send_chatgpt_reply(self, message)
        
        # Random slur reply
        await message_sender.send_random_slur(self, user_id, message)

# Create an instance of the custom client
client = MyClient()

# Create a command tree for the client
tree = app_commands.CommandTree(client)

# Gay command
@tree.command(name="gay", description="Command description.", guild=guild)
async def commandName(interaction: discord.Interaction, member: discord.Member = None):
    # Send a message when the command is used
    await interaction.response.send_message("Matthew")

# Translator command
@tree.command(name="translator", description="Command description.", guild=guild)
async def commandName(interaction: discord.Interaction, word: str, description: str = "yes"):
    try:
        # Open and load the translator.json file
        with open(os.path.join(sys.path[0], "translator.json")) as f:
            translator_data = json.load(f)
        
        # Search for the selected word in the translator data
        translation = None
        for entry in translator_data["translator"]:
            if entry["arabic"] == word:
                translation = f'**Arabic:** *{entry["arabic"]}*\n**English:** *{entry["english"]}*'
                break
        
        # Prepare the response message
        response = translation
        if description == "yes":
            for entry in translator_data["translator"]:
                if entry["arabic"] == word:
                    response += "\n\n" + entry["description"]
                    break
        # Check if the response is empty
        if response:
            # Send the response message
            await interaction.response.send_message(response)
        else:
            await interaction.response.send_message("No translation found.")
    
    except FileNotFoundError:
        await interaction.response.send_message("Error: Translator file not found.")
    except PermissionError:
        await interaction.response.send_message("Error: Insufficient permissions to access the translator file.")
    except KeyError:
        await interaction.response.send_message("Error: Word not found in the translator data.")

# Run the client with the bot token from the environment variables
client.run(os.getenv("BOT_TOKEN"))