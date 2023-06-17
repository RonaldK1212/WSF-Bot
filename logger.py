import config


# Running_log
async def running_log(client):
    running_message = f"**# Alyssa started running \nSession logs:**"
    logging_channel = client.get_channel(config.logging_channel_id)
    if logging_channel:
        await logging_channel.send(running_message)


# Slur reply log
async def slur_reply_log(
    client, user_id, reply, random_number, base_chance, increment, reply_chance
):
    user_name = client.users_dict[user_id]
    slur_reply_log = (
        "**Slur reply log:**\n"
        f"Replied with **'{reply}'** to **'{user_name}'**\n"
        f"Random number: {random_number}\n"
        f"Reply chance: {base_chance} + {increment} * {client.number_of_spammed_messages - 1} = {reply_chance}%\n"
        f"Messages sent before replying: {client.number_of_spammed_messages}\n"
        "------------------------------------------"
    )
    logging_channel = client.get_channel(config.logging_channel_id)
    if logging_channel:
        await logging_channel.send(slur_reply_log)
