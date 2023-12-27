import json

import dotenv
import requests
from dependencies import BaseTool, os

dotenv.load_dotenv()
bot_token = os.environ['DISCORD_KEY']


def get_dm_channel(user_id):
    url = 'https://discord.com/api/v9/users/@me/channels'
    headers = {
        'Authorization': f'Bot {bot_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'recipient_id': user_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        # Successfully retrieved the DM channel
        return response.json()['id']
    else:
        # Handle errors
        print(f"Error getting DM channel: {response.status_code}")
        print(response.json())
        return None


def send_message(channel_id, message):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    headers = {
        'Authorization': f'Bot {bot_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'content': message
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        # Message sent successfully
        print("Message sent successfully.")
    else:
        # Handle errors
        print(f"Error sending message: {response.status_code}")
        print(response.json())
    return response


class DiscordBot(BaseTool):
    name = "discord_message"
    description = "Useful to send me or someone else a message as plain text or md format via Discord, cannot be used to open discord app. message should NOT be in json format."

    def __init__(self, bot_token: str):
        bot_token = bot_token
        object.__setattr__(self, "bot_token", bot_token)
        super().__init__()

    def _run(self, tool_input: str, **kwargs) -> str:
        """Send a message to a Discord channel."""
        message = tool_input
        channel_id = get_dm_channel('346148004002267156')
        try:
            message = json.loads(message)
            for i in message:
                response = send_message(channel_id, str(message[i]))
        except TypeError:
            response = send_message(channel_id, str(message))

        if response.status_code == 200 or response.status_code == 201:
            return "Message sent successfully"
        else:
            return f"Failed to send message, status code: {response.status_code}"


# Create an instance of the custom search tool
discord_messaging = DiscordBot(bot_token)
