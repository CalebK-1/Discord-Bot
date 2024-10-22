import asyncio
import random

import discord
from discord import *
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get

import settings
import responses
import reaction_role


# Bot Client Constructor
class BotClient(commands.Bot):
    def __init__(self) -> None:
        intents: Intents = Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="?", intents=intents)


logger = settings.logging.getLogger("client")


def main() -> None:

    # Instantiating Bot Client
    client = BotClient()

    # Handling startup
    @client.event
    async def on_ready() -> None:
        guild_names_string = ""
        for num in range(0, len(client.guilds)):
            guild_names_string = guild_names_string + client.guilds[num].name + ", "
        logger.info(f"User: {client.user} (ID: {client.user.id})")
        logger.info(f"Running in servers: {guild_names_string}")

        # Runs other files concurrently
        await responses.run(client)
        await reaction_role.run(client)

    # New member handling
    @client.event
    async def on_member_join(member: discord.Member):
        guild = member.guild
        welcomeChannel = guild.get_channel(1292826297038540972)
        newMemberRole = guild.get_role(1293371825027551314)
        if welcomeChannel is not None:
            to_send = f"Welcome {member.mention} to {guild.name}"
            await give_role(welcomeChannel, newMemberRole, member)
            await welcomeChannel.send(to_send)

    # Ping command
    @client.command(
        aliases=["p", "P"],
        help="Should say pong",
        description="Ping command",
        brief="Ping command",
        enabled=True,
        hidden=True,
    )
    async def ping(ctx):
        """Answers with pong"""
        await ctx.send("pong")

    # 8 Ball command
    @client.command(
        aliases=["8ball", "8 ball", "8Ball", "8 Ball", "8", "8b", "8B"],
        help="Gives an 8 ball response per Chandler's request",
        description="8 Ball command. Sends a message that you might find on an 8 Ball",
        brief="8 ball command",
    )
    async def eightball(ctx):
        """8 Ball command"""
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        await ctx.send(answers[random.randint(0, len(answers) - 1)])

    # Add roles
    @client.command(
        aliases=["gr", "role give", "role set", "set role", "give role", "sr"],
        brief='"give role @{Role Name} @{User Name}"',
        description="Gives Role to User",
    )
    @has_permissions(manage_roles=True)
    async def give_role(ctx, role: discord.Role, user: discord.Member):
        try:
            await user.add_roles(role)
            await ctx.send(f"Successfully given {role.mention} to {user.mention}.")
        except Exception as e:
            await ctx.send("Could not give role to user")
            logger.error(e)

    # Remove roles
    @client.command(
        aliases=["rr", "role remove", "remove role"],
        brief='"remove role @{Role Name} @{User Name}"',
        description="Removes Role from User",
    )
    @has_permissions(manage_roles=True)
    async def remove_role(ctx, role: discord.Role, user: discord.Member):
        try:
            await user.remove_roles(role)
            await ctx.send(f"Successfully removed {role} from {user.mention}.")
        except Exception as e:
            await ctx.send("Could not take role from user")
            logger.error(e)

    # Send message on error
    @client.event
    async def on_command_error(ctx, error):
        await ctx.send(error)
        logger.error(error)

    # Run from token
    client.run(settings.DISCORD_API_SECRET, root_logger=True)


# run
if __name__ == "__main__":
    main()
