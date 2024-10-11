from random import randint


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    if "hello" in lowered:
        return "hello"
    elif "dog pissing" in lowered:
        return "https://tenor.com/view/dog-long-ahh-pee-gif-9206364076996243934"
    # Conditions to trigger roll dice command
    # elif lowered[0] == "d" and len(lowered) > 1 and lowered[1] != "0":
    #     if lowered[1:4].isdigit() == True and len(lowered) == 4:
    #         return roll_dice(int(lowered[1:4]))
    #     elif lowered[1:3].isdigit() == True and len(lowered) == 3:
    #         return roll_dice(int(lowered[1:3]))
    #     elif lowered[1].isdigit() == True and len(lowered) == 2:
    #         return roll_dice(int(lowered[1]))

    # Bad input gets a what the sigma
    return "erm what the sigma"


# # Rolls a d1 through d99
# def roll_dice(sides: int) -> str:
#     result: int = randint(1, sides)
#     if sides < 100:
#         return f"Rolling D{sides}: You rolled a {result}!"
#     else:
#         return "Nah that's too big"
