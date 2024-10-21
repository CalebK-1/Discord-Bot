from random import randint
import discord
from discord import Message

import settings

logger = settings.logging.getLogger("client")


async def run(client: discord.Object) -> None:
    print("Running responses.py")

    # Handling incoming messages
    @client.listen()
    async def on_message(message: Message) -> None:
        # Returns for bot messages or commands
        if message.author == client.user:
            return

        username: str = str(message.author)
        message_content: str = message.content
        channel: str = str(message.channel)
        logger.info((f"[{channel}] {username}: {message_content}"))

        if message.content[0] == "?":
            return

        if client.user.mentioned_in(message):  # If bot is mentioned
            # Remove @Fart Bot from the message
            message_no_mention = "".join(message.content.split(client.user.mention))
            try:
                # Get a response from the get_response command and send it to the channel as a message
                response: str = get_response(message_no_mention)
                logger.info(f"[{channel}] Fart Bot: {response}")
                await message.channel.send(response)
            except Exception as e:
                print(e)


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    if "hello" in lowered:
        return "hello"
    elif "dog pissing" in lowered:
        return "https://tenor.com/view/dog-long-ahh-pee-gif-9206364076996243934"
    # More to be implemented

    # Bad input gets a what the sigma
    return "erm what the sigma"
