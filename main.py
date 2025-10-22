import os
import discord
from dotenv import load_dotenv
import json
import re
import asyncio
import datetime
import random
import time

embed_color = 431252
embed_error_color = 16711680

load_dotenv()
token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)
guild_id = "1385626987003121877"
staff_role_id = "1389952977003085844"
latest_help = None
excluded_channels = [
    "1427704338981060739", #LSLink
]
dm_command_cooldown = 5
dm_command_last_used = time.time()

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
    activity = discord.CustomActivity(name=f"{saved_data["command-prefix"]}{cmd} | Open-source", emoji=emoji)
    return activity

@client.event
async def on_message(message):
    if not message.author == client.user and not str(message.channel.id) in excluded_channels:
        msg = message.content.lower()
        guild = await client.fetch_guild(guild_id)
        sender = await guild.fetch_member(message.author.id)
        roles = sender.roles
        staff_role = await guild.fetch_role(staff_role_id)

        match = re.match(rf"{re.escape(saved_data["command-prefix"])}(\S+)", msg)
        if match:
            command = match.group(1)
            if command == "ping":
                latency = round(client.latency * 1000)
                content = f"Pong! {latency}ms"
                embed = create_embed("Ping", content, embed_color, None, None)
                await message.reply(embed=embed)
            
            if command == "help":
                content = """Please specify the help category by using one of the reactions below.
**Categories:**
*general*, *fun*, *staff*"""
                embed = create_embed("Ping", content, embed_color, None, None)
                global latest_help
                help_msg = await message.reply(embed=embed)
                await help_msg.add_reaction("🌍")
                await help_msg.add_reaction("🎉")
                await help_msg.add_reaction("🛡️")
                latest_help = help_msg
            
            if command == "reset-nick":
                try:
                    await message.author.edit(nick=message.author.name)
                except:
                    embed = create_embed("Error", "Failed to reset nickname of user.", embed_error_color, None, None)
                else:
                    embed = create_embed("Reset Nickname", "Successfully reset your nickname.", embed_color, None, None)

                await message.reply(embed=embed)
            
            if command == "git":
                embed = create_embed("Github repository", "Link: https://github.com/Digeryq12/discordadditions", embed_color, None, None)
                await message.reply(embed=embed)
            
            if command == "staff-call":
                emoji = discord.PartialEmoji(name="chickendrip", id="1390038881772240907")
                embed = create_embed("Staff call", f"{message.author.mention} is calling from {message.channel.mention}!", embed_error_color, None, None)
                staff_channel = await guild.fetch_channel("1398559095145103451")
                await staff_channel.send(embed=embed)
                await message.add_reaction(emoji)
            
            if staff_role in roles:
                if command == "qotd":
                    if message.reference:
                        quote_message = await message.channel.fetch_message(message.reference.message_id)
                        qotd_channel = await guild.fetch_channel("1427670684930408649")
                        now = datetime.datetime.now()
                        current_time = now.strftime("%B %d")
                        qotd = create_embed(f"QOTD {current_time}", f"*{quote_message.content}*\n- {quote_message.author.name}", embed_color, None, None)
                        await qotd_channel.send(embed=qotd)
                        embed = create_embed("QOTD", "Successfully selected the quote of today.", embed_color, None, None)
                        await message.reply(embed=embed)
                    else:
                        embed = create_embed("Error", "You need to reply to a message.", embed_error_color, None, None)
                        await message.reply(embed=embed)
        
        match = re.match(rf"{re.escape(saved_data["command-prefix"])}(\S+) (.+)", msg)
        if match:
            command = match.group(1)
            parameter = match.group(2)
            if command == "pookie":
                if parameter != "@everyone":
                    try:
                        member = await guild.fetch_member(get_id_from_mention(parameter))
                    except:
                        embed = create_embed("Error", "Could not find user.", embed_error_color, None, None)
                    else:
                        if member != message.author:
                            try:
                                await member.edit(nick=f"{member.name} ({message.author.name}'s pookie)")
                                embed = create_embed("Pookie", f"{member.name} is now your pookie!", embed_color, None, None)
                            except:
                                embed = create_embed("Error", "Failed to change nickname of user.", embed_error_color, None, None)
                        else:
                            embed = create_embed("Error", "No. :3", embed_error_color, None, None)
                else:
                    embed = create_embed("Error", "Nice try duh.", embed_error_color, None, None)

                await message.reply(embed=embed)
            
            if command == "profile":
                try:
                    member = await guild.fetch_member(get_id_from_mention(parameter))
                except:
                    embed = create_embed("Error", "Could not find user.", embed_error_color, None, None)
                else:
                    join_date = member.joined_at.strftime("%d/%m/%Y, %H:%M")
                    status = member.activities
                    display_name = member.display_name
                    is_pending = member.pending
                    username = member.name
                    member_id = member.id
                    is_bot = member.bot
                    member_roles = member.roles
                    creation_date = member.created_at.strftime("%d/%m/%Y, %H:%M")
                    avatar = member.display_avatar
                    banner = member.display_banner
                    roles_string = ""
                    for rl in member_roles:
                        if rl.name != "@everyone":
                            roles_string += f"{rl.mention} "

                    embed_content = f"""**@{username}**
**Id:** {member_id}
**Status:** {status}
**Creation date:** {creation_date}
**Server join date:** {join_date}
**Roles:** {roles_string}
**Is bot:** {is_bot}
**Is pending (application):** {is_pending}"""
                    
                    embed = create_embed(f"{display_name}'s Profile", embed_content, embed_color, avatar, banner)

                await message.reply(embed=embed)
            
            if command == "eat":
                try:
                    member = await guild.fetch_member(get_id_from_mention(parameter))
                except:
                    embed = create_embed("Error", "Could not find user.", embed_error_color, None, None)
                else:
                    yumm_color = embed_color

                    if member.id == message.author.id:
                        yummessage = "You ate... yourself?"
                    elif member.bot:
                        if member.id == client.user.id:
                            yummessage = "HEY! I'm not yummy! Don't eat me!"
                            yumm_color = embed_error_color
                        else:
                            yummessage = "You ate... a clanker?"
                    else:
                        yum_list = ["Yum!", "Yummy!", "Delicious!", "Tasty!", "Mmmmm!"]
                        rand = random.randint(0, len(yum_list) - 1)
                        yummessage = f"You ate: {member.name}. {yum_list[rand]}"
                    
                    embed = create_embed("Eat", yummessage, yumm_color, None, None)
                    await message.reply(embed=embed)
            
            if command == "8ball":
                responses = [
                    # Positive
                    "It is certain",
                    "It is decidedly so",
                    "Without a doubt",
                    "Yes – definitely",
                    "You may rely on it",
                    "As I see it, yes",
                    "Most likely",
                    "Outlook good",
                    "Yes",
                    "Signs point to yes",

                    # Neutral
                    "Reply hazy, try again",
                    "Ask again later",
                    "Better not tell you now",
                    "Cannot predict now",
                    "Concentrate and ask again",

                    # Negative
                    "Don't count on it",
                    "My reply is no",
                    "My sources say no",
                    "Outlook not so good",
                    "Very doubtful"
                ]

                rand = random.randint(0, len(responses) - 1)
                embed = create_embed("Magic 8 Ball", responses[rand], embed_color, None, None)
                await message.reply(embed=embed)
            
            if command == "rate":
                rating = random.randint(1, 10)
                embed = create_embed("Rate", f"Giving a {rating}/10 to '{parameter}'", embed_color, None, None)
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

                if command == "purge":
                    try:
                        int(parameter)
                    except:
                        embed = create_embed("Error", "Invalid parameter.", embed_error_color, None, None)
                    else:
                        if int(parameter) <= 100:
                            await message.channel.purge(limit=int(parameter), bulk=True)
                            embed = embed = create_embed("Purge", f"Successfully purged {parameter} messages.", embed_color, None, None)
                        else:
                            embed = create_embed("Error", "You cannot purge more than 100 messages.", embed_error_color, None, None)
                    
                    await message.channel.send(embed=embed)
        
        match = re.match(rf"{re.escape(saved_data["command-prefix"])}(\S+) (\S+) (.+)", msg)
        if match:
            command = match.group(1)
            parameter1 = match.group(2)
            parameter2 = match.group(3)

            if command == "dm":
                global dm_command_last_used
                now = time.time()
                if now - dm_command_last_used < dm_command_cooldown:
                    embed = create_embed("Error", "Slow down with that command.", embed_error_color, None, None)
                    await message.reply(embed=embed)
                else:
                    dm_command_last_used = now
                    try:
                        member = await guild.fetch_member(get_id_from_mention(parameter1))
                    except:
                        embed = create_embed("Error", "Could not find user.", embed_error_color, None, None)
                        await message.reply(embed=embed)
                    else:
                        emoji = discord.PartialEmoji(name="chickendrip", id="1390038881772240907")
                        dm_channel = await member.create_dm()
                        embed = create_embed(f"{message.author.name} (from '{guild.name}')", parameter2, embed_color, None, None)
                        await dm_channel.send(embed=embed)
                        await message.add_reaction(emoji)
                    

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message == latest_help and reaction.me:
        trigger_message = await reaction.message.channel.fetch_message(reaction.message.reference.message_id)
        if user.id == trigger_message.author.id:

            general_help_message = f"""- **ping** *{saved_data["command-prefix"]}ping*
Returns the rtt.
- **reset-nick** *{saved_data["command-prefix"]}reset-nick*
Resets your nickname (to your username).
- **git** *{saved_data["command-prefix"]}git*
Returns the github repo link.
- **staff-call** *{saved_data["command-prefix"]}staff-call*
'Call' the staff members.
- **profile** *{saved_data["command-prefix"]}profile [@user]*
View the profile of the specified user.
- **dm** *{saved_data["command-prefix"]}dm [@user] [prompt]*
Direct message the specified user with the given prompt."""

            fun_help_message = f"""- **pookie** *{saved_data["command-prefix"]}pookie [@user]*
Make someone your pookie.
- **eat** *{saved_data["command-prefix"]}eat [@user]*
No context.
- **8ball** *{saved_data["command-prefix"]}8ball [prompt]*
Let the magic 8 ball respond to your prompt.
- **rate** *{saved_data["command-prefix"]}rate [prompt]*
Rates the prompt.
- **barn** (STAFF) *{saved_data["command-prefix"]}barn [@user]*
Barns the specified user."""

            staff_help_message = f"""- **qotd** *{saved_data["command-prefix"]}qotd* (Reply to a message)
Select the quote of the day.
- **change-prefix** *{saved_data["command-prefix"]}change-prefix [prefix]*
Change the command prefix.
- **purge** *{saved_data["command-prefix"]}purge [amount]*
Delete the specififed amount of messages in the channel."""

            if reaction.emoji == "🌍":
                embed = create_embed("General", general_help_message, embed_color, None, None)
            elif reaction.emoji == "🎉":
                embed = create_embed("Fun", fun_help_message, embed_color, None, None)
            elif reaction.emoji == "🛡️":
                embed = create_embed("Staff", staff_help_message, embed_color, None, None)

            await reaction.message.clear_reactions()
            await reaction.message.edit(embed=embed)

@client.event
async def on_ready():
    guild = await client.fetch_guild(guild_id)
    await guild.chunk()

    cmds = ["ping", "reset-nick", "pookie", "barn", "change-prefix", "git", "dm", "profile", "eat",
            "staff-call", "purge", "8ball", "qotd", "rate", "help"]
    cmds.sort()
    while True:
        for cmd in cmds:
            await client.change_presence(activity=get_activity(cmd))
            await asyncio.sleep(5)

client.run(token)