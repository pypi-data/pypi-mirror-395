from secrets_safe_library import exceptions, safes
from secrets_safe_library.constants.endpoints import (
    GET_SECRETS_SAFE_SAFES,
    GET_SECRETS_SAFE_SAFES_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.safes import fields as safe_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Safe(CLIController):
    """
    Secret Safe Safes functionality.
    """

    def __init__(self):
        super().__init__(
            name="safes",
            help="Safes management commands",
        )

    @property
    def class_object(self) -> safes.Safe:
        if self._class_object is None and self.app is not None:
            self._class_object = safes.Safe(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_safes(self, args):
        """
        Returns all safes to which the current user has access.
        """
        try:
            fields = self.get_fields(
                GET_SECRETS_SAFE_SAFES, safe_fields, Version.DEFAULT
            )
            self.display.v("Calling list_safes function")
            safes = self.class_object.list()
            self.display.show(safes, fields)
            success_msg = "Safes listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list safes")

    @command
    @aliases("get")
    @option(
        "-id",
        "--safe-id",
        help="To get a safe by ID (GUID)",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    def get_safe(self, args):
        """
        Returns a safe by ID.
        """
        try:
            fields = self.get_fields(
                GET_SECRETS_SAFE_SAFES_ID, safe_fields, Version.DEFAULT
            )
            self.display.v(f"Searching by ID {args.safe_id}")
            safe = self.class_object.get_by_id(args.safe_id)
            self.display.show(safe, fields)
            success_msg = "Safe retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to get a safe for ID: {args.safe_id}")

    @command
    @aliases("create")
    @option("-n", "--name", help="The name of the safe", type=str, required=True)
    @option(
        "-d",
        "--description",
        help="The description of the safe",
        type=str,
        required=False,
    )
    def create_safe(self, args):
        """
        Creates a new Safe.
        """
        try:
            self.display.v("Calling create_safe function")

            safe = self.class_object.create_safe(
                name=args.name,
                description=args.description,
            )
            self.display.show(safe)
            success_msg = "Safe created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the safe")

    @command
    @aliases("update")
    @option(
        "-id",
        "--safe-id",
        help="ID of the safe to update",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    @option("-n", "--name", help="The name of the safe", type=str, required=True)
    @option(
        "-d",
        "--description",
        help="The description of the safe",
        type=str,
        required=False,
    )
    def update_safe(self, args):
        """
        Updates an existing Safe using its ID.
        """
        try:
            result_msg = ""
            self.display.v("Calling update_safe function")
            response_text, status_code = self.class_object.update_safe(
                safe_id=args.safe_id,
                name=args.name,
                description=args.description,
            )
            if status_code == 409:
                self.display.v(response_text)
                result_msg = "Name already exists"
            else:
                result_msg = "Safe updated successfully"
            self.display.v(result_msg)
        except exceptions.UpdateError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to update the safe")

    @command
    @aliases("delete")
    @option(
        "-id",
        "--safe-id",
        help="To delete a safe by ID (GUID)",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    def delete_safe(self, args):
        """
        Deletes a Safe by ID.
        """
        try:
            self.display.v(f"Deleting safe by ID {args.safe_id}")
            self.class_object.delete_by_id(args.safe_id)
            success_msg = f"Safe deleted successfully {args.safe_id}"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(f"It was not possible to delete a safe for ID: {args.safe_id}")
            print_it("Does safe exist and provided ID is valid?")
            self.log.error(e)
