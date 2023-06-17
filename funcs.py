# Import necessary libraries
import json
import os
import sys


# Get file path function
def get_path(filename):
    return os.path.join(sys.path[0], filename)


# Get all the users names using their ID
def initialize_user_dict():
    try:
        with open(get_path("users.json")) as f:
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
