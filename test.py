import requests

def get_player_description(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        player_data = response.json()
        return player_data["description"]
    else:
        return None

user_id = 156719681 # Replace with the desired user ID
description = get_player_description(user_id)

print(f"Player description: \n{description}")

