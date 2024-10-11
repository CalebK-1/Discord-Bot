import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("client")


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = commands.Bot(command_prefix="?", intents=intents)

    @client.event
    async def on_ready():
        logger.info(f"User: {client.user} (ID: {client.user.id})")

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("command error")

    client.main(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    main()
