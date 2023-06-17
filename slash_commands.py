# Import necessary libraries
import json

import discord
import funcs
from discord import app_commands


# Gay Command
def gay(interaction: discord.Interaction):
    # Send a message when the command is used
    return interaction.response.send_message(
        f"Hey {interaction.user.mention} Matthew is gay :matthew:"
    )


# Translator command
def translator(interaction: discord.Interaction, word: str, description: str = "yes"):
    try:
        # Open and load the translator.json file
        with open(funcs.get_path("translator.json")) as f:
            translator_data = json.load(f)

        # Search for the selected word in the translator data
        translation = None
        for entry in translator_data["translator"]:
            if entry["arabic"] == word:
                translation = f'**Arabic:** *{entry["arabic"]}*\n**English:** *{entry["english"]}*'
                break

        # Prepare the response message
        response = translation
        # Check the description parameter
        if description == "yes":
            for entry in translator_data["translator"]:
                if entry["arabic"] == word:
                    response += "\n\n" + entry["description"]
                    break
        # Check if the response is empty
        if response:
            # Send the response message
            return interaction.response.send_message(response)
        else:
            return interaction.response.send_message("No translation found.")

    except FileNotFoundError:
        return interaction.response.send_message("Error: Translator file not found.")
    except PermissionError:
        return interaction.response.send_message(
            "Error: Insufficient permissions to access the translator file."
        )
    except KeyError:
        return interaction.response.send_message(
            "Error: Word not found in the translator data."
        )


def load_translator_data():
    # Load the JSON data from the file
    with open(funcs.get_path("translator.json")) as f:
        translator_data = json.load(f)

    # Extract the values of the "arabic" strings
    word_choices = [item["arabic"] for item in translator_data["translator"]]
    word_data = []
    for choice in word_choices:
        word_data.append(
            app_commands.Choice(name=choice, value=str(word_choices.index(choice)))
        )

    description_choices = ["yes", "no"]
    description_data = []
    for choice in description_choices:
        description_data.append(
            app_commands.Choice(
                name=choice, value=str(description_choices.index(choice))
            )
        )

    return (word_data, description_data)
