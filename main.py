import os
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.get_env("BOT_TOKEN")
print(token)