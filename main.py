import discord
from discord import *
from discord.ext import commands
from discord.utils import get

import settings
from responses import get_response


logger = settings.logging.getLogger("client")


def main() -> None:
    # Bot Setup
    intents: Intents = Intents.default()
    intents.message_content = True
    intents.members = True

    # client: Client = Client(intents=intents)
    client = commands.Bot(command_prefix="?", intents=intents)

    # Handling startup
    @client.event
    async def on_ready() -> None:
        logger.info(f"User: {client.user} (ID: {client.user.id})")
        # print("{client.user} is now running!")

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

    @client.command(
        aliases=["p"],
        help="Should say pong",
        description="Ping command",
        brief="Ping command",
        enable=True,
        hidden=True,
    )
    async def ping(ctx):
        """Answers with pong"""
        await ctx.send("pong")

    # Message functionality
    async def send_message(message: Message, user_message: str) -> None:
        if not user_message:
            print("No parameters fed")
            return
        # If user starts a message with "?" get a response and send it.
        if client.user.mentioned_in(message):  # If bot is mentioned
            # Split user message into bot mention and the rest of the message
            user_message = " ".join(user_message.split(client.user.mention))
            try:
                response: str = get_response(user_message)
                print(f"Fart Bot: {response}")
                await message.channel.send(response)
            except Exception as e:
                print(e)

    # Add roles
    @client.command
    async def give_role(ctx, role: discord.Role, user: discord.Member):
        try:
            await user.add_roles(role)
            await ctx.send(f"Successfully given {role.mention} to {user.mention}.")
        except Exception as e:
            print(e)

    # Remove roles
    @client.command
    async def remove_role(ctx, role: discord.Role, user: discord.Member):
        try:
            await user.remove_roles(role)
            await ctx.send(f"Successfully removed {role} from {user.mention}.")
        except Exception as e:
            print(e)

    # Run from token
    client.run(settings.DISCORD_API_SECRET, root_logger=True)


# run
if __name__ == "__main__":
    main()
