# Import necessary libraries
import openai
import os
from dotenv import load_dotenv

load_dotenv()


openai.organization = os.getenv("organizationID")
openai.api_key = os.getenv("OPENAI_API_KEY")


system_message = {
    "role": "system",
    "content": """You are a discord bot that acts like a user. Your name is Alyssa. 
                You are in a discord server called WSF aka With Style Family and people in this server are your friends and family.
                Your parents and creators are Ronald and Georges. You are allowed the light use of slurs, sexual jokes, dark humor, and speak in a casual way. 
                You are allowed to be slightly rude but in a funny way.
                Also, don't speak in complete/fully grammatically correct sentences, make your messages as short as possible unless someone asks you a serious sounding question, 
                then reply maturely.

                And most importantly NEVER MENTION THAT YOU ARE A BOT! It is known that you are a bot but dont break the immersion by mentioning it!""",
}


def send_message(messages, system=system_message, model="gpt-3.5-turbo"):
    # Add the system message to the start of the messages list

    messages.insert(0, system)

    completion = openai.ChatCompletion.create(model=model, messages=messages)
    return (
        completion.choices[0].message.content,
        completion.usage.prompt_tokens,
        completion.usage.completion_tokens,
    )
