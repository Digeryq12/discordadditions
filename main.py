import os
import discord
from dotenv import load_dotenv
import json
import re
import asyncio

embed_color = 431252
embed_error_color = 16711680

load_dotenv()
token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
guild_id = "1385626987003121877"
staff_role_id = "1389952977003085844"

def read_json(file_name):
    with open(file_name, "r") as file:
        return json.load(file)


def write_json(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, sort_keys=True, indent=4)

saved_data = read_json("data.json")

def create_embed(title, content, color, image_url, banner):
    embed = discord.Embed(title=title, description=content, color=color)
    if image_url:
        embed.set_thumbnail(url=image_url)
    if banner:
        embed.set_image(url=banner)
        
    embed.set_footer(text="DCAdditions by @digeryy")
    return embed

def get_id_from_mention(mention):
    match = re.match(r"<@(\S+)>", mention)
    if not match:
        match = re.match(r"(\S+)", mention)

    if match:
        return match.group(1)
    
def get_activity(cmd):
    emoji = discord.PartialEmoji(id="1430257378770685953", name="pukerainbow_gil_static")
    activity = discord.CustomActivity(name=f"{saved_data["command-prefix"]}{cmd} | Making Discord cooler!", emoji=emoji)
    return activity

@client.event
async def on_message(message):
    if not message.author == client.user:
        msg = message.content.lower()
        guild = await client.fetch_guild(guild_id)
        roles = message.author.roles
        staff_role = await guild.fetch_role(staff_role_id)

        match = re.match(rf"{re.escape(saved_data["command-prefix"])}(\S+)", msg)
        if match:
            command = match.group(1)
            if command == "ping":
                latency = round(client.latency * 1000)
                content = f"Pong! {latency}ms"
                embed = create_embed("Ping", content, embed_color, None, None)
                await message.reply(embed=embed)
            
            if command == "reset-nick":
                try:
                    await message.author.edit(nick=message.author.global_name)
                except:
                    embed = create_embed("Error", "Failed to reset nickname of user.", embed_error_color, None, None)
                else:
                    embed = create_embed("Reset Nickname", "Successfully reset your nickname.", embed_color, None, None)

                await message.reply(embed=embed)
        
        match = re.match(rf"{re.escape(saved_data["command-prefix"])}(\S+) (\S+)", msg)
        if match:
            command = match.group(1)
            parameter = match.group(2)
            if command == "pookie":
                try:
                    member = await guild.fetch_member(get_id_from_mention(parameter))
                except:
                    embed = create_embed("Error", "Could not find user.", embed_error_color, None, None)
                else:
                    if member != message.author:
                        try:
                            await member.edit(nick=f"{member.global_name} ({message.author.global_name}'s pookie)")
                            embed = create_embed("Pookie", f"{member.global_name} is now your pookie!", embed_color, None, None)
                        except:
                            embed = create_embed("Error", "Failed to change nickname of user.", embed_error_color, None, None)
                    else:
                        embed = create_embed("Error", "No. :3", embed_error_color, None, None)

                await message.reply(embed=embed)
            
            if staff_role in roles:
                if command == "barn":
                    try:
                        member = await guild.fetch_member(get_id_from_mention(parameter))
                    except:
                        embed = create_embed("Error", "Could not find user.", embed_error_color, None, None)
                    else:
                        if member != message.author:
                            embed = create_embed("Barn", f"{member.mention} got barned!", embed_error_color, "https://c.tenor.com/OaFgXC-QB00AAAAC/tenor.gif", None)
                        else:
                            embed = create_embed("Barn", "You barned yourself, silly.", embed_error_color, "https://c.tenor.com/OaFgXC-QB00AAAAC/tenor.gif", None)

                    await message.reply(embed=embed)
                
                if command == "change-prefix":
                    if saved_data["command-prefix"] != parameter:
                        saved_data["command-prefix"] = parameter
                        write_json("data.json", saved_data)
                        embed = create_embed("Change command prefix", f"Changed command prefix to '{parameter}'.", embed_color, None, None)
                        await client.change_presence(activity=get_activity("ping"))
                    else:
                        embed = create_embed("Error", "That's the current prefix buddy.", embed_error_color, None, None)

                    await message.reply(embed=embed)

@client.event
async def on_ready():
    cmds = ["ping", "reset-nick", "pookie", "barn"]
    while True:
        for cmd in cmds:
            await client.change_presence(activity=get_activity(cmd))
            await asyncio.sleep(5)

client.run(token)