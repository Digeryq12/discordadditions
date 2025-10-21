import os
import discord
from dotenv import load_dotenv
import json
import re

bot_prefix = "!"
embed_color = 431252
embed_error_color = 16711680

load_dotenv()
token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
guild_id = "1385626987003121877"

def read_json(file_name):
    with open(file_name, "r") as file:
        return json.load(file)


def write_json(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, sort_keys=True, indent=4)

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
        guild = await client.fetch_guild(guild_id)

        match = re.match(rf"{re.escape(bot_prefix)}(\w+)", msg)
        if match:
            command = match.group(1)
            if command == "ping":
                latency = round(client.latency * 1000)
                content = f"Pong! {latency}"
                embed = create_embed("Ping", content, embed_color, None, None)
                await message.reply(embed=embed)
            
            if command == "reset_nick":
                await message.author.edit(nick=message.author.global_name)
                embed = create_embed("Reset Nickname", "Successfully reset your nickname.", embed_color, None, None)
                await message.reply(embed=embed)
        
        match = re.match(rf"{re.escape(bot_prefix)}(\w+) (\S+)", msg)
        if match:
            command = match.group(1)
            parameter = match.group(2)
            if command == "pookie":
                member = await guild.fetch_member(parameter)
                try:
                    member = await guild.fetch_member(parameter)
                except:
                    embed = create_embed("Error", "Could not find user.", embed_error_color, None, None)
                else:
                    try:
                        await member.edit(nick=f"{member.global_name} ({message.author.global_name}'s pookie)")
                        embed = create_embed("Pookie", f"{member.global_name} is now your pookie!", embed_color, None, None)
                    except:
                        embed = create_embed("Error", "Failed to change status of user.", embed_error_color, None, None)

                await message.reply(embed=embed)

client.run(token)