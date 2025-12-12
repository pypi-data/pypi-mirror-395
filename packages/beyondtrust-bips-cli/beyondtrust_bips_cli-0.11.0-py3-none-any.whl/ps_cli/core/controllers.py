import argparse
from typing import Callable, Dict, List

from ps_cli.core.app import App
from ps_cli.core.display import Display
from ps_cli.core.interfaces import ClassObjectInterface, ControllerInterface
from ps_cli.core.logger import Logger


class BaseCLIController(ControllerInterface):
    """
    Base class for implementing a Controller.

    A Controller is a group of commands that could be related to an API endpoint.

    This class provides a concrete implementation of the ControllerInterface, handling
    the registration of subcommands, commands, and subparsers.

    Example of command within a Controller class:
    >>> @command
    >>> @aliases("delete", "remove")
    >>> @option("-u", "--username", help="Cool help text", type=str, required=True)
    >>> def delete(self, args):
    >>>     print_it(f"Deleting account: {args.username}")
    """

    def __init__(self, name: str, help: str = "") -> None:
        """
        Initialize a new Controller instance.

        Args:
            name (str): The name of the Controller.
            help (str): The help text to show in CLI.
        """
        self.name = name
        self.help = help
        self.commands: Dict[str, Callable] = {}
        self.app: App = None
        self.register_commands()

    @property
    def log(self) -> Logger:
        """
        Shortcut to app.log.
        """
        if self.app:
            return self.app.log

    @property
    def display(self) -> Display:
        """
        Allows different levels of verbose messages (v, vv, vvv, vvvv, vvvvv).
        Shortcut to app.display.
        """
        if self.app:
            return self.app.display

    def register_subcommand(self, func: Callable) -> None:
        """
        Register a subcommand with the Controller.

        This method registers a subcommand function with the Controller instance,
        storing it in the `commands` dictionary. If the function has aliases defined,
        it also registers the aliases as keys pointing to the same function.

        Args:
            func (Callable): The subcommand function to register.
        """
        name = func.__name__.replace("_", "-")
        self.commands[name] = {"func": func, "aliases": func.__aliases__}

    def register_commands(self) -> None:
        """
        Register all decorated commands with the Controller.

        This method iterates over the attributes of the Controller instance and
        registers any callable attribute that has the `__options__` attribute
        (indicating it's a decorated command) by calling the `register_subcommand`
        method.
        """
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "__options__"):
                self.register_subcommand(attr)

    def register_subparsers(self, subparsers: argparse._SubParsersAction) -> None:
        """
        Register subparsers for the Controller's commands.

        This method creates a top-level parser for the Controller and subparsers
        for each registered command. It then adds arguments to each command parser
        based on the options defined for the corresponding command function.
        Finally, it sets the epilog of the top-level parser to display the list
        of available commands.

        Args:
            subparsers (argparse._SubParsersAction): The subparsers object from
            argparse.
        """
        help = self.help or f"Manage {self.name}"
        # Controller parser
        parser = subparsers.add_parser(
            self.name,
            help=help,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self.__doc__,
        )
        # Command subparsers
        subparsers = parser.add_subparsers(
            dest="command",
            required=True,
            description=f"Subcommands available for {self.name}",
        )
        for command_name, command_options in self.commands.items():
            command_func = command_options["func"]
            aliases = command_options["aliases"]

            command_help = command_func.__doc__

            # Command parser
            command_parser = subparsers.add_parser(
                command_name,
                aliases=aliases,
                description=command_help,
                help=command_help,
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )
            for option_data in getattr(command_func, "__options__", []):
                if "action" in option_data:
                    command_parser.add_argument(
                        *option_data["args"],
                        action=option_data["action"],
                        **option_data["kwargs"],
                    )
                else:
                    command_parser.add_argument(
                        *option_data["args"],
                        default=option_data["default"],
                        type=option_data["type"],
                        nargs=option_data["nargs"],
                        **option_data["kwargs"],
                    )
            command_parser.set_defaults(func=command_func)

    def setup(self, app: App) -> None:
        """
        Point controller class to the CLI App instance.

        Args:
            app (App): CLI App instance.

        Returns: None
        """
        self.app = app


class CLIController(BaseCLIController, ClassObjectInterface):
    """
    CLI Controller. Useful when directly interacting with Python Library.

    Authentication object is included automatically into class_object_args.
    """

    _class_object = None

    def __init__(
        self,
        name: str,
        help: str = "",
    ) -> None:
        """
        Initialize a new CLIController instance.

        Args:
            name (str): The name of the Controller.
            help (str): The help text to show in CLI.
        """
        super().__init__(name, help)

    def get_fields(self, key: str, fields_map: dict, version: str = None) -> List:
        """
        Return a list of fields for the given key using provided fields_map and
        configured API version in CLI app.

        Args:
            key (str): The key to search inside fields_map. Correspond to endpoint (
                secrets_safe_library.constants.endpoints)
            fields_map (dict): Mapping with fields related to object (Secrets, Folders,
                etc)
            version (str, optional): Version to get fields, if not provided then
                configured one (self.app.api_version) will be used.
        """
        version = version or self.app.api_version
        try:
            fields = fields_map[key][version]
            return fields
        except KeyError as e:
            message = (
                f"Could not get fields for key {key} and API version "
                f"{self.app.api_version}, Error: {e}"
            )
            self.app.log.error(message)


class ShortCommandController(BaseCLIController):
    def __init__(self, name: str, help: str = "") -> None:
        """
        Initialize a new ShortCommandController instance.
        This controller is for short commands functionality.

        Args:
            name (str): The name of the Controller.
            help (str): The help text to show in CLI.
        """
        super().__init__(name, help)
