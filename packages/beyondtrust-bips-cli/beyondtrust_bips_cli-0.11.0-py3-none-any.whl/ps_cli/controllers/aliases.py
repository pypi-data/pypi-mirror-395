import argparse

from secrets_safe_library import aliases, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_ALIASES,
    GET_ALIASES_ID,
    GET_ALIASES_NAME,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.aliases import fields as aliases_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases as aliases_decorator
from ps_cli.core.decorators import command, option
from ps_cli.core.display import print_it


class Aliases(CLIController):
    """
    Controller for managing aliases.

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self) -> None:
        super().__init__(
            name="aliases",
            help="Aliases management commands",
        )

    @property
    def class_object(self) -> aliases.Aliases:
        if self._class_object is None and self.app is not None:
            self._class_object = aliases.Aliases(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @option(
        "identifier",
        type=str,
        nargs="?",
        default=None,
        help="To get an alias by ID or Name.",
    )
    def list_get_aliases(self, args):
        """
        If no ID or name is provided, lists all Aliases.
        If an ID or name is provided, gets the Alias using that.
        (Short-command).
        """
        try:
            if args.identifier:
                if args.identifier.isdigit():
                    args_get = argparse.Namespace(
                        id_alias=int(args.identifier), name_alias=None
                    )
                else:
                    args_get = argparse.Namespace(
                        id_alias=None, name_alias=args.identifier
                    )
                self.get_alias_by_id_name(args_get)
            else:
                args_list = argparse.Namespace(state=[1, 2])
                self.list_aliases(args_list)
        except Exception as e:
            self.display.v(e)
            self.log.error(f"Short command error: {e}")
            print_it("It was not possible to list aliases")

    @command
    @aliases_decorator("list")
    @option(
        "-s",
        "--state",
        help="Zero or more state values. (Default: 1,2) "
        "i.e., 'state=2', 'state=1,2', 'state=0,1,2' "
        "0: Unmapped, 1: Mapped, 2: Highly Available",
        type=int,
        required=False,
        default=[1, 2],
        nargs="*",
    )
    def list_aliases(self, args):
        """
        Lists all aliases, optionally filtered by state.
        """
        try:
            fields = self.get_fields(GET_ALIASES, aliases_fields, Version.DEFAULT)
            self.display.v("Calling list_aliases function")
            aliases = self.class_object.get_aliases(state=args.state)
            self.display.show(aliases, fields)
            success_msg = "Aliases listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list aliases")

    @command
    @aliases_decorator("get")
    @option(
        "-id",
        "--id-alias",
        help="The ID of the alias to retrieve.",
        type=int,
        required=False,
    )
    @option(
        "-name",
        "--name-alias",
        help="The name of the alias to retrieve.",
        type=str,
        required=False,
    )
    def get_alias_by_id_name(self, args):
        """
        Retrieves an alias by its ID or Name.
        """
        try:
            if args.id_alias:
                fields = self.get_fields(
                    GET_ALIASES_ID, aliases_fields, Version.DEFAULT
                )
                self.display.v("Calling get_alias_by_id function")
                alias = self.class_object.get_by_id(object_id=args.id_alias)
                self.display.show(alias, fields)
                success_msg = "Alias retrieved successfully using Alias ID"
                self.display.v(success_msg)
            elif args.name_alias:
                fields = self.get_fields(
                    GET_ALIASES_NAME, aliases_fields, Version.DEFAULT
                )
                self.display.v("Calling get_alias_by_name function")
                alias = self.class_object.list_by_key(key="name", value=args.name_alias)
                self.display.show(alias, fields)
                success_msg = "Alias retrieved successfully using Alias Name"
                self.display.v(success_msg)
            else:
                print_it(
                    "You must provide either an ID or a Name to retrieve an alias."
                )
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the alias")
