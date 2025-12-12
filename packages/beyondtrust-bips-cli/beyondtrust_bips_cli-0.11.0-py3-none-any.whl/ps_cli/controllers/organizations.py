from secrets_safe_library import exceptions, organizations
from secrets_safe_library.constants.endpoints import GET_ORGANIZATIONS
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.organizations import fields as organization_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Organization(CLIController):
    """
    BeyondInsight Organizations functionality.
    """

    def __init__(self):
        super().__init__(
            name="organizations",
            help="Organizations management commands",
        )

    @property
    def class_object(self) -> organizations.Organization:
        if self._class_object is None and self.app is not None:
            self._class_object = organizations.Organization(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_organizations(self, args):
        """
        Returns a list of organizations to which the current user has permission.
        """
        try:
            fields = self.get_fields(
                GET_ORGANIZATIONS, organization_fields, Version.DEFAULT
            )
            self.display.v("Calling list_organizations function")
            organizations = self.class_object.list_organizations()
            self.display.show(organizations, fields)
            success_msg = "Organizations listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list organizations")

    @command
    @aliases("get")
    @option(
        "-id",
        "--organization-id",
        help="To get a organization by ID (GUID)",
        type=str,
        required=False,
        enforce_uuid=True,
    )
    @option(
        "-n",
        "--organization-name",
        help="To get a organization by Name",
        type=str,
        required=False,
    )
    def get_organization(self, args):
        """
        Returns an organization by ID or Name.
        """
        try:
            if args.organization_id is None and args.organization_name is None:
                print_it(
                    "You must provide either an organization ID (-id) or name (-n)"
                )
                return

            if args.organization_id is not None:
                self.display.v(f"Searching by ID {args.organization_id}")
                organization = self.class_object.get_organization_by_id(
                    args.organization_id
                )
            else:
                self.display.v(f"Searching by Name {args.organization_name}")
                organization = self.class_object.get_organization_by_name(
                    args.organization_name
                )

            # Using same fields as list, since structure right now is the same
            fields = self.get_fields(
                GET_ORGANIZATIONS, organization_fields, Version.DEFAULT
            )
            self.display.show(organization, fields)
            success_msg = "Organization retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.organization_id is not None:
                print_it(
                    "It was not possible to get an organization for ID: "
                    f"{args.organization_id}"
                )
            else:
                print_it(
                    "It was not possible to get an organization for Name: "
                    f"{args.organization_name}"
                )
