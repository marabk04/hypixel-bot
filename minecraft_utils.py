import requests

def getInfo(call):
    response = requests.get(call)
    return response.content


def UsernameToID(username):
    mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    uuid = getInfo(mojang_url)
    return uuid['id']

def format_username(username):
    mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    formatted_username = getInfo(mojang_url)
    return formatted_username['name']
