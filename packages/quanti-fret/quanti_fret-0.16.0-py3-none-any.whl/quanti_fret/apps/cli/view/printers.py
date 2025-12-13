
import math


def print_phase(title: str, line_length: int):
    """ Print a phase title

    It displays a line of "-" above and below and surround the title with "*"s
    and limit the width to line_length chars.

    Args:
        title (str): The title to print
        line_length (int): The size of the line
    """
    line = _create_title_line(title, line_length, '*')
    separator = '*'*line_length
    print(f'\n{separator}')
    print(f'{line}')
    print(f'{separator}\n')


def print_title(title: str, line_length: int):
    """ Print a title

    It surround the title with "#"s and limit the width to line_length chars.

    Args:
        title (str): The title to print
        line_length (int): The size of the line
    """
    line = _create_title_line(title, line_length, '#')
    print(f'\n{line}\n')


def print_bullet_list(indent: int, lines: list[str]):
    """ Print a bullet list.

    Args:
        indent (int): Number of tabs to set before each line
        lines (str): The list of lines to print.
    """
    indent_str = '\t' * indent
    for line in lines:
        msg = f'{indent_str}* {line}'
        print(msg)


def print_error(msg: str, separator_length: int) -> None:
    """ Print an error message

    Args:
        msg (str): Error message to display
        separator_length (int): The size of the separator line
    """
    repeat = int(separator_length / 3)
    print('/!\\'*repeat)
    print(msg)
    print('/!\\'*repeat)


def _create_title_line(title: str, line_length: int, char: str) -> str:
    """ Compute the number of token to surround a message so that this message
    do not go above the limit of chars

    Args:
        msg (str): Message to print
        line_length (int): Line length
        char (str): char that surrounds the title

    Returns:
        str: the line to display
    """
    assert len(char) == 1
    if (line_length - len(title)) < 6:
        title = title[0:line_length-6]
    nb_token = line_length - len(title) - 2
    nb_token_before = math.floor(nb_token/2)
    nb_token_after = math.ceil(nb_token/2)
    return f'{char*nb_token_before} {title} {char*nb_token_after}'
