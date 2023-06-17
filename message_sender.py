# Import necessary libraries
import json
import random
import gpt
import config
import funcs
import logger

# ChatGPT reply function
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

# Random slur reply function
async def send_random_slur(client, user_id, message):
    # Increment the spam count
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
            with open(funcs.get_path("slurs.json")) as f:
                slurs_file = json.load(f)
                slurs = slurs_file["slurs"]
            reply = random.choice(slurs)
            await message.reply(reply)
            
            # Logging the stats
            await logger.slur_reply_log(client, user_id, reply, random_number, base_chance, increment, reply_chance)
                   
        except FileNotFoundError:
            await message.channel.send("Error: Slurs file not found.")
        except PermissionError:
            await message.channel.send("Error: Insufficient permissions to access the slurs file.")
        
        # Reset the spam count
        client.number_of_spammed_messages = 0
    
    # Update the user id of the last message (for the next captured message)
    client.user_id_of_last_message = user_id
