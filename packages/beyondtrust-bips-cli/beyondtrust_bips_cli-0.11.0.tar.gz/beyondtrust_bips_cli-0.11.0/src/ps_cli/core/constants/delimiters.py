from enum import Enum


class Delimiter(Enum):
    """
    Available delimiters when showing results as CSV or TSV in CLI.
    """

    COMMA = ","
    SEMICOLON = ";"
    TAB = "\t"
    PIPE = "|"
    SPACE = " "
