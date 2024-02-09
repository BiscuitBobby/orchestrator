import builtins
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Qdrant
from dependencies import BaseTool, os
from pathlib import Path
import requests
import dotenv
import json

dotenv.load_dotenv()
bot_token = os.environ['DISCORD_KEY']

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

loader = JSONLoader(
    file_path='./contacts.json',
    jq_schema='.contacts[]',
    text_content=False)

data = loader.load()
qdrant = Qdrant.from_documents(
    data,
    embeddings,
    location=":memory:",  # Local mode with in-memory storage only
    collection_name="my_documents",
)

def get_contact(query):
    found_docs = qdrant.similarity_search(query)
    output = json.loads(found_docs[0].page_content)
    print(output)
    return str(output["id"])

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

# -------------------------------------------------------------------------------------------------------------------

class DiscordBot(BaseTool):
    name = "discord_message"
    description = "Useful to send me or someone else a message via Discord, cannot be used to open discord app"

    def __init__(self, bot_token: str):
        bot_token = bot_token
        object.__setattr__(self, "bot_token", bot_token)
        super().__init__()

    def _run(self, tool_input: str, **kwargs) -> str:
        """Send a message to a Discord channel."""
        message = tool_input
        channel_id = get_dm_channel(get_contact(builtins.global_prompt))# (input("\nenter user id: "))

        input(f"recipient: {get_contact(builtins.global_prompt)}\n{tool_input}")
        
        if tool_input[0]=='{' and tool_input[-1] =='}':
            message = json.loads(message)
            if 'message' in message:
                response = send_message(channel_id, message["message"])
            else:
                for i in message:
                    response = send_message(channel_id, message[i])
        else:
            response = send_message(channel_id, message)

        if response.status_code == 200 or response.status_code == 201:
            return "Message sent successfully"
        else:
            return f"Failed to send message, status code: {response.status_code}"


# Create an instance of the custom search tool
discord_messaging = DiscordBot(bot_token)