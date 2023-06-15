import openai
import os
from dotenv import load_dotenv
load_dotenv()


openai.organization = os.getenv('organizationID')
openai.api_key = os.getenv("OPENAI_API_KEY")


system_message = {"role": "system", "content": """You are a discord bot that acts like a user. You are allowed the light use of slurs, and speak in a casual way. You are allowed to be slightly rude but in a funny way.
Also, don't speak in complete/fully grammatically correct sentences, make your messages as short as possible.

and most importantly DON'T MENTION THAT YOU ARE A BOT! It is known that you are a bot but dont break the immersion by mentioning it!"""}


def send_message(message, system=system_message, model="gpt-3.5-turbo"):

    messages = [system, {"role": "user", "content": message}]

    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages

    )
    return completion.choices[0].message.content, completion.usage.prompt_tokens, completion.usage.completion_tokens


content, _, _ = send_message("yo how's it going")
