from secrets_safe_library import exceptions, workgroups
from secrets_safe_library.constants.endpoints import (
    GET_WORKGROUPS,
    GET_WORKGROUPS_ID,
    GET_WORKGROUPS_NAME,
    POST_WORKGROUPS,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.workgroups import fields as workgroup_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Workgroup(CLIController):
    """
    Works with Secrets Safe Workgroups - Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="workgroups",
            help="Workgroups management commands",
        )

    @property
    def class_object(self) -> workgroups.Workgroup:
        if self._class_object is None and self.app is not None:
            self._class_object = workgroups.Workgroup(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_workgroups(self, args):
        """
        Returns a list of Workgroups to which the current user has access.
        """
        try:
            fields = self.get_fields(GET_WORKGROUPS, workgroup_fields, Version.DEFAULT)
            self.display.v("Calling list_workgroups function")
            workgroups = self.class_object.get_workgroups()
            self.display.show(workgroups, fields)
            success_msg = "Workgroups listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list workgroups")

    @command
    @aliases("get")
    @option(
        "-n",
        "--name",
        help="The Workgroup name",
        type=str,
        required=False,
    )
    @option(
        "-id",
        "--id",
        help="The Workgroup id",
        type=int,
        required=False,
    )
    def get_workgroup(self, args):
        """
        Returns a Workgroup by name or id.
        """
        try:
            success_msg = ""
            if args.id:
                fields = self.get_fields(
                    GET_WORKGROUPS_ID, workgroup_fields, Version.DEFAULT
                )
                self.display.v("Calling get_workgroup_by_id function")
                workgroup = self.class_object.get_workgroup_by_id(args.id)
                self.display.show(workgroup, fields)
                success_msg = "Workgroup retrieved successfully by ID"
            elif args.name:
                fields = self.get_fields(
                    GET_WORKGROUPS_NAME, workgroup_fields, Version.DEFAULT
                )
                self.display.v("Calling get_workgroup_by_name function")
                workgroup = self.class_object.get_workgroup_by_name(args.name)
                self.display.show(workgroup, fields)
                success_msg = "Workgroup retrieved successfully by name"
            else:
                print_it("You must provide either a name or an id")
                return
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.id:
                print_it(f"It was not possible to get workgroup by ID: {args.id}")
            else:
                print_it(f"It was not possible to get workgroup by name: {args.name}")

    @command
    @aliases("create")
    @option(
        "-n",
        "--name",
        help="The Workgroup name",
        type=str,
        required=True,
    )
    @option(
        "-org",
        "--organization",
        help="The organization ID (UUID)",
        type=str,
        required=False,
        enforce_uuid=True,
    )
    def create_workgroup(self, args):
        """
        Creates a new Workgroup.
        """
        try:
            fields = self.get_fields(POST_WORKGROUPS, workgroup_fields, Version.DEFAULT)
            self.display.v("Calling create_workgroup function")
            workgroup = self.class_object.post_workgroup(
                name=args.name, organization_id=args.organization
            )
            self.display.show(workgroup, fields)
            self.display.v("Workgroup created successfully")
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create workgroup")
