import random
import gpt
import config
import os
import sys
import json

async def send_chatgpt_reply(client, message):
    # If the message is a reply to the bot's message
    if message.reference and message.reference.resolved.author == client.user:
        assistant_message = {"role": "assistant", "content": message.reference.resolved.content}
        user_message = {"role": "user", "content": message.content}
        response, _, _ = gpt.send_message([assistant_message, user_message], model="gpt-4")
    else:
        user_message = {"role": "user","content": message.content}
        response, _, _ = gpt.send_message([user_message], model="gpt-4")
    await message.channel.send(response)

async def send_random_slur(client, user_id, message):
    client.number_of_spammed_messages += 1
    # If the user ID of the previous message is different, reset the spam count
    if client.user_id_of_last_message and client.user_id_of_last_message != user_id:
        client.number_of_spammed_messages = 1
    
    # Generate a random number
    random_number = random.randint(1, 100)

    # Randomness variables
    base_chance = 1
    increment = 2
    reply_chance = base_chance + increment * (client.number_of_spammed_messages - 1)

    # If the random number is less than or equal to the current chance, reply with a random slur
    if random_number <= reply_chance:
        try:
            # Open and load the slurs.json file
            with open(os.path.join(sys.path[0], "slurs.json")) as f:
                slurs_file = json.load(f)
                slurs = slurs_file["slurs"]
            reply = random.choice(slurs)
            await message.reply(reply)
            
            # Logging the stats
            user_name = client.users_dict[user_id]
            slur_reply_log = (
                "**Slur reply log:**\n"
                f"Replied with '{reply}' to '{user_name}'\n"
                f"Random number: {random_number}\n"
                f"Reply chance: {base_chance} + {increment} * {client.number_of_spammed_messages - 1} = {reply_chance}%\n"
                f"Number of spam messages sent before replying: {client.number_of_spammed_messages}\n"
                "------------------------------------------"
            )
            # Access the global logging channel ID
            logging_channel = client.get_channel(config.logging_channel_id)
            if logging_channel:
                await logging_channel.send(slur_reply_log)
                
        except FileNotFoundError:
            await message.channel.send("Error: Slurs file not found.")
        except PermissionError:
            await message.channel.send("Error: Insufficient permissions to access the slurs file.")
        
        # Reset the spam count
        client.number_of_spammed_messages = 0
    
    # Update the user id of the last message (for the next captured message)
    client.user_id_of_last_message = user_id