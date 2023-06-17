# Import necessary libraries
import os
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
        self.user_message = {}

    async def startup(self):
        # Wait until the client is ready
        await self.wait_until_ready()

    async def on_ready(self):
        # Sync the command tree with the guild when the client is ready
        if not self.synced:
            await tree.sync(guild=guild)
            self.synced = True
            print("Synced.")

        print(f"Logged on as {self.user}!")
    
    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return

        # Get the user ID of the current message
        user_id = message.author.id
        
        # ChatGPT reply
        if client.user in message.mentions and config.gpt_enabled:
            # If the message is a reply to the bot's message
            if message.reference and message.reference.resolved.author == self.user:
                assistant_message = {"role": "assistant", "content": message.reference.resolved.content}
                user_message = {"role": "user", "content": message.content}
                response, _, _ = gpt.send_message([assistant_message, user_message], model="gpt-4")
            else:
                user_message = {"role": "user","content": message.content}
                response, _, _ = gpt.send_message([user_message], model="gpt-4")
            await message.channel.send(response)
        
        
        # Random slur reply
        # Check if the user ID exists in the dictionary, if not, initialize the count to 0
        if user_id not in self.user_message:
            self.user_message[user_id] = 0

        # If the user ID of the previous message is different, reset the consecutive message count
        previous_user_id = message.channel.last_message.author.id if message.channel.last_message else None
        if previous_user_id == user_id:
            # Increment the consecutive message count for the current user
            self.user_message[user_id] += 1
        
        # Generate a random number
        random_number = random.randint(1, 100)

        # Randomness variables
        base_chance = 1
        increment = 3
        reply_chance = base_chance + increment * (self.user_message[user_id] - 1)

        # If the random number is less than or equal to the current chance, reply with a random slur
        if random_number <= reply_chance:
            # Open and load the slurs.json file
            with open("WSF-Bot\\slurs.json") as f:
                slurs_file = json.load(f)
            slurs = slurs_file["slurs"]
            await message.reply(random.choice(slurs))
            
            # Close the slurs.json file
            f.close()
            
            # Reset the messages count for the user
            self.user_message[user_id] = 0
            
        
        # Reset the dictionary if 2 different people are talking
        if len(self.user_message) > 1:
            self.user_message = {}

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
    # Open and load the translator.json file
    with open("WSF-Bot\\translator.json") as f:
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
    
    # Send the response message
    await interaction.response.send_message(response)
    # Close the translator.json file
    f.close()

# Run the client with the bot token from the environment variables
client.run(os.getenv("BOT_TOKEN"))
