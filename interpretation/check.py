from typing import List, Union

from discord import Message
from emoji import UNICODE_EMOJI

from config import prefix
from management.db import emoji_to_player
from management.position import roles_list


# Makes sure the message has at least the needed amount of users.
# If the message contains emojis, they should be converted to ids as well. Mentions have priority, however.
# The command should return the given amount of user ids, or, if equal to -1, should return them all.
def users(message: Message, amount: int = -1, delete_duplicates: bool = True)-> Union[bool, List[int]]:
    """
    :return: the requested amount of user ids in a list. If the amount is -1, all users are given.

    :param message: the Discord message to inspect
    :param amount: the wanted amount of users in a list
    :param delete_duplicates: filter out users that are mentioned twice in the message
    """
    user_table = [person.id for person in message.mentions] \
                 + [argument for argument in map(emoji_to_player, message.content.split(' ')) if argument is not None]

    if delete_duplicates:
        user_table = list(set(user_table))

    if max(amount, 1) > len(user_table):
        return False

    if amount == -1:
        return user_table

    return user_table[:amount]


# Makes sure the message has at least the needed amount of integers.
# The command should return the given amount of numbers, or, if equal to -1, should return them all.
def numbers(message: Message, amount: int = -1, delete_duplicates: bool = False) -> Union[bool, List[int]]:
    """
    :return: If the amount is -1, all ints are given. If there are not enough integers, or no integers at all, the function returns False.
    :param message: the Discord message to inspect
    :param amount: the wanted amount of integers in the list
    :param delete_duplicates: filter out integers that are mentioned twice in the message
    """
    number_table = [int(argument) for argument in message.content.split(' ') if check_for_int(argument)]

    if delete_duplicates:
        number_table = list(set(number_table))

    if max(amount, 1) > len(number_table):
        return False

    if amount == -1:
        return number_table

    return number_table[:amount]


# Makes sure the message has at least the needed amount of emojis.
# The command should return the given amount of numbers, or, if equal to -1, should return them all.
def emojis(message: Message, amount: int = -1, delete_duplicates: bool = True) -> Union[bool, List[str]]:
    """
    :return: the requested amount of (vanilla) emojis in a list from a message. If the amount is -1, all emojis are given. If there are not enough emojis, or no emojis at all, the function returns False.
    :param message: the Discord message to inspect
    :param amount: the wanted amount of emojis in the list
    :param delete_duplicates: filter out emojis that are mentioned twice in the message
    """

    emoji_table = [argument for argument in message.content.split(' ') if argument in UNICODE_EMOJI]

    if delete_duplicates:
        emoji_table = list(set(emoji_table))

    if max(amount, 1) > len(emoji_table):
        return False

    if amount == -1:
        return emoji_table

    return emoji_table[:amount]


# Makes sure the message has at least the needed amount of roles.
# The command should return the given amount of numbers, or, if equal to -1, should return them all.
def roles(message: Message, amount: int = -1, delete_duplicates: bool = False) -> Union[bool, List[str]]:
    """
    If there are not enough roles or none at all, the function returns False.


    :return: the requested amount of roles that are mentioned in the message as a list. If the amount is -1, all roles are given
    :param message: the Discord message to inspect
    :param amount: the wanted amount of integers in the list
    :param delete_duplicates: filter out roles that are mentioned twice in the message
    """

    role_table = [argument for argument in message.content.split(' ') if argument in roles_list]

    if delete_duplicates:
        role_table = list(set(role_table))

    if max(amount, 1) > len(role_table):
        return False

    if amount == -1:
        return role_table

    return role_table[:amount]


# Checks if a file can be converted into an integer.
# If it cannot, the function returns false.
def check_for_int(s) -> bool:
    """Returns True if the value s is or can be converted to an integer. Returns False otherwise."""
    try:
        int(s)
        return True
    except ValueError:
        return False


# Checks if an input requests a given command
def is_command(message: Message, commandlist: List[str], help: bool = False) -> bool:
    """Check if the message starts with the given command or its aliases.

    :param message: the Discord message
    :param commandlist: list of possible commands that return True if the prefix is put in front of them
    :param help: when set to True, return True when the message starts with the prefix, then help, and then the command.
    """
    for command in commandlist:
        if message.content.startswith(prefix + command) and not help:
            return True
        if message.content.startswith(prefix + 'help ' + command) and help:
            return True
    return False
