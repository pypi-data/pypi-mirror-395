from enum import Enum


class Format(Enum):
    """
    Output formats available for CLI.
    """

    JSON = "json"
    CSV = "csv"
    TSV = "tsv"
