# Import necessary libraries
import os
import client

# Run the client with the bot token from the environment variables
client.client.run(os.getenv("BOT_TOKEN"))
