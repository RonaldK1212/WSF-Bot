# Import necessary libraries
import os
import sys
import discord
import config
from discord import app_commands
import json
import random
import gpt

# Get the guild ID from the environment variables
guild = discord.Object(id=os.getenv("GUILD_ID"))

# Define a custom client class
class MyClient(discord.Client):
    def __init__(self):
        # Initialize the client with the default intents
        super().__init__(intents=discord.Intents.default())
        self.synced = False
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
                print("Bot is ready and connected.")
                print(f"Logged on as {self.user}!")
                
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
            await self.send_chatgpt_reply(message)
        
        # Random slur reply
        await self.send_random_slur(user_id, message)

    async def send_chatgpt_reply(self, message):
        # If the message is a reply to the bot's message
        if message.reference and message.reference.resolved.author == self.user:
            assistant_message = {"role": "assistant", "content": message.reference.resolved.content}
            user_message = {"role": "user", "content": message.content}
            response, _, _ = gpt.send_message([assistant_message, user_message], model="gpt-4")
        else:
            user_message = {"role": "user","content": message.content}
            response, _, _ = gpt.send_message([user_message], model="gpt-4")
        await message.channel.send(response)

    async def send_random_slur(self, user_id, message):
        self.number_of_spammed_messages += 1
        # If the user ID of the previous message is different, reset the spam count
        if self.user_id_of_last_message and self.user_id_of_last_message != user_id:
            self.number_of_spammed_messages = 1
        
        # Generate a random number
        random_number = random.randint(1, 100)

        # Randomness variables
        base_chance = 1
        increment = 2
        reply_chance = base_chance + increment * (self.number_of_spammed_messages - 1)

        # If the random number is less than or equal to the current chance, reply with a random slur
        if random_number <= reply_chance:
            try:
                # Open and load the slurs.json file
                with open(os.path.join(sys.path[0], "slurs.json")) as f:
                    slurs_file = json.load(f)
                    slurs = slurs_file["slurs"]
                await message.reply(random.choice(slurs))
                
                # Logging the stats
                print("------------------------------------------")
                print(f"Replied to {user_id}")
                print("Stats:")
                print(f"Random number: {random_number}")
                print(f"Messages sent: {self.user_message[user_id]}")
                print(f"Reply chance: {base_chance} + {increment} * {self.user_message[user_id] - 1} = {reply_chance}%")
                print("------------------------------------------")
                 
            except FileNotFoundError:
                await message.channel.send("Error: Slurs file not found.")
            except PermissionError:
                await message.channel.send("Error: Insufficient permissions to access the slurs file.")
            
            # Reset the spam count
            self.number_of_spammed_messages = 0
        
        #Update the user id of the last message (for the next captured message)
        self.user_id_of_last_message = user_id

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