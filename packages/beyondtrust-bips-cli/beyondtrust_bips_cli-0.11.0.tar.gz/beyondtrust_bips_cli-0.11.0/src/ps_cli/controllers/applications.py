from secrets_safe_library import applications, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_APPLICATIONS,
    GET_APPLICATIONS_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.applications import fields as application_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Application(CLIController):
    """
    Application functionality.
    """

    def __init__(self):
        super().__init__(
            name="applications",
            help=(
                "List Applications or Applications by User. Allows assigning/"
                "unassigning Applications to Managed Accounts. "
                "Users need the Application ID to do operations to managed accounts."
            ),
        )

    @property
    def class_object(self) -> applications.Application:
        if self._class_object is None and self.app is not None:
            self._class_object = applications.Application(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_applications(self, args):
        """
        Returns a list of all applications.
        """
        try:
            fields = self.get_fields(
                GET_APPLICATIONS, application_fields, Version.DEFAULT
            )
            self.display.v("Calling list_applications function")
            applications = self.class_object.list()
            self.display.show(applications, fields)
            success_msg = "Applications listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list applications")

    @command
    @aliases("get")
    @option(
        "-id",
        "--application-id",
        help="To get an application by ID",
        type=int,
        required=True,
    )
    def get_application(self, args):
        """
        Returns an application by ID.
        """
        try:
            fields = self.get_fields(
                GET_APPLICATIONS_ID, application_fields, Version.DEFAULT
            )
            self.display.v(f"Searching by ID {args.application_id}")
            application = self.class_object.get_by_id(args.application_id)
            self.display.show(application, fields)
            success_msg = "Application retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get an application for ID: "
                f"{args.application_id}"
            )

    @command
    @aliases("get-managed-account-apps")
    @option(
        "-account-id",
        "--account-id",
        help="The managed account ID to get applications for",
        type=int,
        required=True,
    )
    def get_managed_account_apps(self, args):
        """
        Returns applications associated with a managed account.
        """
        try:
            fields = self.get_fields(
                GET_APPLICATIONS, application_fields, Version.DEFAULT
            )
            self.display.v(
                f"Getting applications for managed account ID {args.account_id}"
            )
            applications = self.class_object.get_managed_account_apps(args.account_id)
            self.display.show(applications, fields)
            success_msg = "Applications retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get applications for managed account ID: "
                f"{args.account_id}"
            )

    @command
    @aliases("assign-to-managed-account")
    @option(
        "-account-id",
        "--account-id",
        help="The managed account ID to assign application to",
        type=int,
        required=True,
    )
    @option(
        "-app-id",
        "--application-id",
        help="The application ID to assign to managed account",
        type=int,
        required=True,
    )
    def assign_app_to_managed_account(self, args):
        """
        Assigns an application to a managed account.
        """
        try:
            self.display.v(
                f"Assigning application ID {args.application_id} "
                f"to managed account ID {args.account_id}"
            )
            result = self.class_object.assign_app_to_managed_account(
                args.account_id, args.application_id
            )
            fields = self.get_fields(
                GET_APPLICATIONS_ID, application_fields, Version.DEFAULT
            )
            self.display.show(result, fields)
            self.display.v(
                f"Application {args.application_id} assigned to "
                f"managed account {args.account_id} successfully"
            )
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to assign application {args.application_id} "
                f"to managed account {args.account_id}: {e}"
            )

    @command
    @aliases("remove-from-managed-account")
    @option(
        "-account-id",
        "--account-id",
        help="The managed account ID to remove application from",
        type=int,
        required=True,
    )
    @option(
        "-app-id",
        "--application-id",
        help="The application ID to remove from managed account",
        type=int,
        required=True,
    )
    def remove_app_from_managed_account(self, args):
        """
        Removes an application from a managed account.
        """
        try:
            self.display.v(
                f"Removing application ID {args.application_id} "
                f"from managed account ID {args.account_id}"
            )
            self.class_object.remove_app_from_managed_account(
                args.account_id, args.application_id
            )
            success_msg = (
                f"Application {args.application_id} removed from "
                f"managed account {args.account_id} successfully"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to remove application {args.application_id} "
                f"from managed account {args.account_id}: {e}"
            )

    @command
    @aliases("unassign-all-from-managed-account")
    @option(
        "-account-id",
        "--account-id",
        help="The managed account ID to unassign all applications from",
        type=int,
        required=True,
    )
    def unassign_all_apps_from_managed_account(self, args):
        """
        Unassigns all applications from a managed account.
        """
        try:
            self.display.v(
                "Unassigning all applications from "
                f"managed account ID {args.account_id}"
            )
            self.class_object.unassign_all_apps_from_managed_account(args.account_id)
            success_msg = (
                f"All applications unassigned from managed account {args.account_id} "
                "successfully"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to unassign all applications "
                f"from managed account {args.account_id}: {e}"
            )
