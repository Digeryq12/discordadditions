import os
import discord
from dotenv import load_dotenv

bot_prefix = "!"
embed_color = 431252

load_dotenv()
token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def create_embed(title, content, color, image_url, banner):
    embed = discord.Embed(title=title, description=content, color=color)
    if image_url:
        embed.set_thumbnail(url=image_url)
    if banner:
        embed.set_image(url=banner)
        
    embed.set_footer(text="DCAdditions by @digeryy")
    return embed

@client.event
async def on_message(message):
    if not message.author == client.user:
        msg = message.content.lower()
        if msg == f"{bot_prefix}ping":
            latency = round(client.latency * 1000)
            content = f"Pong! {latency}"
            embed = create_embed("Ping", content, embed_color, None, None)
            await message.channel.send(embed=embed)

client.run(token)