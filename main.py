import os
from typing import Optional
from dotenv import load_dotenv

import discord
from discord import *
from discord.ext import commands
from discord.utils import get

from responses import get_response

# Load the token
load_dotenv()
TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
# print(TOKEN)


# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client: Client = Client(intents=intents)


# Message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("No parameters fed")
        return

    # If user starts a message with "?" get a response and send it.
    if (
        user_message[0] == "?"
    ):  # True if the first character of the message is a question mark
        user_message = user_message[1:]
        try:
            response: str = get_response(user_message)

            print(response)
            await message.channel.send(response)

        except Exception as e:
            print(e)


# Add roles
async def give_role(ctx, role: discord.Role, user: discord.Member):
    try:
        await user.add_roles(role)
        await ctx.send(f"Successfully given {role.mention} to {user.mention}.")
    except Exception as e:
        print(e)


# Remove roles
async def remove_role(ctx, role: discord.Role, user: discord.Member):
    try:
        await user.remove_roles(role)
        await ctx.send(f"Successfully removed {role} from {user.mention}.")
    except Exception as e:
        print(e)


# Handling startup
@client.event
async def on_ready() -> None:
    print("{client.user} is now running!")


# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    message_content: str = message.content
    channel: str = str(message.channel)
    print(f"[{channel}] {username}: {message_content}")

    await send_message(message, message_content)


# New member handling
@client.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    welcomeChannel = guild.get_channel(1292826297038540972)
    newMemberRole = guild.get_role(1293371825027551314)
    if welcomeChannel is not None:
        to_send = f"Welcome {member.mention} to {guild.name}"
        await welcomeChannel.send(to_send)
        await give_role(welcomeChannel, newMemberRole, member)


# Main entry point
def main() -> None:
    client.run(token=TOKEN)


# run
if __name__ == "__main__":
    main()
