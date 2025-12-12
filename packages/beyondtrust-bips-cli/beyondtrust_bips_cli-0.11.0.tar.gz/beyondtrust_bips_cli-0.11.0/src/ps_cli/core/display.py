import csv
import json
import sys
from io import StringIO
from typing import Any, Dict, List, Optional, TextIO

from ps_cli.core.constants import Delimiter, Format
from ps_cli.core.exceptions import InvalidFormatException
from ps_cli.core.logger import Logger


class Display:
    """
    A class for displaying verbose messages based on a configured verbosity level.
    Also includes utility methods to show different outputs (JSON, CSV, TSV).

    Attributes:
        verbosity (int): The verbosity level, ranging from 0 (no output) to 5 (maximum
        output).
        logger (Logger): Logger instance.
    """

    def __init__(
        self,
        verbosity: int = 0,
        logger: Logger = None,
        format: Format = Format.CSV.value,
        delimiter: Delimiter = Delimiter.COMMA.value,
    ):
        self.verbosity = verbosity
        self.logger = logger
        self.format = format
        self.delimiter = delimiter

    def v(self, msg: str, save_log: bool = True) -> None:
        """
        Prints the given message if the verbosity level is set at least to 1.
        Saves the message to logs.
        """
        if self.verbosity >= 1:
            print_it(msg)
        if self.logger and save_log:
            self.logger.debug(msg)

    def vv(self, msg: str, save_log: bool = True) -> None:
        """
        Prints the given message if the verbosity level is set at least to 2.
        Saves the message to logs.
        """
        if self.verbosity >= 2:
            print_it(msg)
        if self.logger and save_log:
            self.logger.debug(msg)

    def vvv(self, msg: str, save_log: bool = True) -> None:
        """
        Prints the given message if the verbosity level is set at least to 3.
        Saves the message to logs.
        """
        if self.verbosity >= 3:
            print_it(msg)
        if self.logger and save_log:
            self.logger.debug(msg)

    def vvvv(self, msg: str, save_log: bool = True) -> None:
        """
        Prints the given message if the verbosity level is set at least to 4.
        Saves the message to logs.
        """
        if self.verbosity >= 4:
            print_it(msg)
        if self.logger and save_log:
            self.logger.debug(msg)

    def vvvvv(self, msg: str, save_log: bool = True) -> None:
        """
        Prints the given message if the verbosity level is set at least to 5.
        Saves the message to logs.
        """
        if self.verbosity >= 5:
            print_it(msg)
        if self.logger and save_log:
            self.logger.debug(msg)

    def show(
        self,
        data: str | dict | List[Dict[str, any]],
        fields: List[str] = None,
        format: Format = None,
    ):
        """
        Show a message using App configured output format.

        Args:
            data (str | dict | List[Dict[str, any]]): The data to be shown. It can be
                either a string, dictionary or a list of dictionaries.
            fields (List[str], optional): A list of field names (keys) to include in
                the output if `data` is a list of dictionaries. If not provided, all
                fields from the dictionaries will be included.
            format (Format, optional): Override Display format.
        """
        display_format = format or self.format

        # Some endpoints return a dict[Data, TotalCount] when using limit and offset
        # in that case we only need data inside "Data" key.
        # String and List data is processed as it is.
        process_data = data if isinstance(data, (str, list)) else data.get("Data", data)

        try:
            match display_format:
                case Format.JSON.value:
                    print_as_json(process_data)
                case Format.CSV.value:
                    print_as_delimited(
                        process_data, delimiter=self.delimiter, fields=fields
                    )
                case Format.TSV.value:
                    print_as_delimited(
                        process_data, delimiter=Delimiter.TAB.value, fields=fields
                    )
                case _:
                    msg = f"Can't generate output using format {display_format}"
                    if self.logger:
                        self.logger.error(msg)
                    raise InvalidFormatException(msg)
        except (TypeError, ValueError, IndexError) as e:
            if self.logger:
                self.logger.error(f"Error showing data: {e}")


def print_as_json(data: str | List[Dict[str, any]]) -> None:
    """
    Prints a data as a JSON string if valid json.
    """
    try:
        json_str = json.dumps(data, indent=4)
        print_it(json_str)
    except (TypeError, ValueError) as e:
        raise e


def print_as_delimited(
    data: str | dict | List[Dict[str, any]], delimiter: str, fields: List[str] = None
) -> None:
    """
    Prints the given data as a delimited string (CSV or TSV) with the specified
    delimiter.

    Args:
        data (str | dict | List[Dict[str, any]]): The data to be printed. It can be a
        string, a dictionary, or a list of dictionaries.
        delimiter (str): The delimiter character to use for the delimited string (e.g.,
        ',' for CSV or '\t' for TSV).
        fields (List[str], optional): A list of field names (keys) to include in the
        output if `data` is a dictionary or a list of dictionaries. If not provided,
        all fields from the dictionaries will be included.

    Raises:
        TypeError: If the `data` argument is not a string, dictionary, or list of
        dictionaries.
        ValueError: If there is an issue with the input data or the specified fields.
        IndexError: If there is an issue with accessing the keys or values in the input
        data.

    Note:
        If `data` is a string, it will be printed as is.
        If `data` is a dictionary, it will be printed as a single row in the delimited
        format.
        If `data` is a list of dictionaries, each dictionary will be printed as a
        separate row in the delimited format.
    """
    try:
        if isinstance(data, str):
            print_it(data)
        elif isinstance(data, dict):
            print_dict_as_delimited(data, fields, delimiter)
        else:
            print_list_as_delimited(data, fields, delimiter)
    except (TypeError, ValueError, IndexError) as e:
        raise e


def print_dict_as_delimited(data: dict, fields: list, delimiter: str):
    """
    Prints a dictionary as a delimited string (CSV or TSV) with the specified delimiter.

    Args:
        data (Dict[str, Any]): The dictionary to be printed.
        delimiter (str): The delimiter character to use for the delimited string (e.g.,
        ',' for CSV or '\t' for TSV).
        fields (List[str], optional): A list of field names (keys) to include in the
        output. If not provided, all fields from the dictionary will be included.
    """
    output = StringIO(newline=None)
    # Ensure fieldnames is an ordered list. If fields were provided use their
    # order. Otherwise preserve the insertion order from the dict keys.
    fieldnames = list(fields) if fields else list(data.keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=delimiter)
    writer.writeheader()
    filtered_dict = {k: data[k] for k in fieldnames if k in data}
    writer.writerow(filtered_dict)
    delimited_str = output.getvalue().strip()
    print_it(delimited_str)


def print_list_as_delimited(data: list, fields: list, delimiter: str):
    """
    Prints a list of dictionaries as a delimited string (CSV or TSV) with the specified
    delimiter.

    Args:
        data (List[Dict[str, Any]]): The list of dictionaries to be printed.
        delimiter (str): The delimiter character to use for the delimited string (e.g.,
        ',' for CSV or '\t' for TSV).
        fields (List[str], optional): A list of field names (keys) to include in the
        output. If not provided, all fields from the dictionaries will be included. If a
        field is present in the `fields` list but not in a dictionary, an empty string
        will be printed for that field.
    """
    output = StringIO(newline=None)
    # If fields were provided, preserve their order. Otherwise build an
    # ordered list of fieldnames based on the first occurrence across the
    # list of dictionaries so output is deterministic and predictable.
    if fields:
        fieldnames = list(fields)
    else:
        ordered = []
        for row in data:
            # row.keys() preserves insertion order for dicts
            for k in row.keys():
                if k not in ordered:
                    ordered.append(k)
        fieldnames = ordered

    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=delimiter)
    writer.writeheader()
    writer.writerows(({k: row[k] for k in fieldnames if k in row} for row in data))
    delimited_str = output.getvalue().strip()
    print_it(delimited_str)


def print_it(
    *args: Any,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """
    Custom printing function intended to be compatible with the target OS.
    """

    if file is None:
        file = sys.stdout  # Use the current sys.stdout

    # TODO: Confirm and adjust according target OS (Win, Mac, Linux, etc)
    print(*args, sep=sep, end=end, file=file, flush=flush)
