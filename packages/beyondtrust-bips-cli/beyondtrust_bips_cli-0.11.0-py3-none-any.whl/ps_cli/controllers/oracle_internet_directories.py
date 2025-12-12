from secrets_safe_library import exceptions, oracle_internet_directories
from secrets_safe_library.constants.endpoints import (
    GET_ORACLE_INTERNET_DIRECTORIES,
    GET_ORACLE_INTERNET_DIRECTORIES_ID,
    POST_ORACLE_INTERNET_DIRECTORIES_ID_SERVICES_QUERY,
    POST_ORACLE_INTERNET_DIRECTORIES_ID_TEST,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.oracle_internet_directories import (
    fields as oid_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class OracleInternetDirectory(CLIController):
    """
    Password Safe Oracle Internet Directories functionality.
    """

    def __init__(self):
        super().__init__(
            name="oracle-internet-directories",
            help="Oracle Internet Directories management commands",
        )

    @property
    def class_object(self) -> oracle_internet_directories.OracleInternetDirectories:
        if self._class_object is None and self.app is not None:
            self._class_object = oracle_internet_directories.OracleInternetDirectories(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_oracle_internet_directories(self, args):
        """
        Returns all Oracle Internet Directories to which the current user has access.
        """
        try:
            fields = self.get_fields(
                GET_ORACLE_INTERNET_DIRECTORIES, oid_fields, Version.DEFAULT
            )
            self.display.v("Calling list_oracle_internet_directories function")
            oids = self.class_object.list()
            self.display.show(oids, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list Oracle Internet Directories")

    @command
    @aliases("get")
    @option(
        "-id",
        "--oid-id",
        help="To get an Oracle Internet Directory by ID (GUID)",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    def get_oracle_internet_directory(self, args):
        """
        Returns an Oracle Internet Directory by ID.
        """
        try:
            fields = self.get_fields(
                GET_ORACLE_INTERNET_DIRECTORIES_ID, oid_fields, Version.DEFAULT
            )
            self.display.v(f"Searching by ID {args.oid_id}")
            oid = self.class_object.get_by_id(args.oid_id)
            self.display.show(oid, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to get an Oracle Internet Directory for ID: "
                f"{args.oid_id}"
            )

    @command
    @aliases("query")
    @option(
        "-id",
        "--oid-id",
        help="The Oracle Internet Directory ID to query services for",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    def query_services(self, args):
        """
        Queries and returns DB Services for an Oracle Internet Directory by ID.
        """
        try:
            self.display.v(
                f"Querying services for Oracle Internet Directory ID {args.oid_id}"
            )
            services = self.class_object.query_services(args.oid_id)

            fields = self.get_fields(
                POST_ORACLE_INTERNET_DIRECTORIES_ID_SERVICES_QUERY,
                oid_fields,
                Version.DEFAULT,
            )

            self.display.show(services, fields)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to query services for Oracle Internet "
                f"Directory ID: {args.oid_id}"
            )

    @command
    @aliases("test-connection")
    @option(
        "-id",
        "--oid-id",
        help="The Oracle Internet Directory ID to test connection for",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    def test_connection(self, args):
        """
        Tests the connection to an Oracle Internet Directory by ID.
        """
        try:
            self.display.v(
                f"Testing connection for Oracle Internet Directory ID {args.oid_id}"
            )
            result = self.class_object.test_connection(args.oid_id)
            fields = self.get_fields(
                POST_ORACLE_INTERNET_DIRECTORIES_ID_TEST, oid_fields, Version.DEFAULT
            )

            self.display.show(result, fields)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to test connection for Oracle Internet "
                f"Directory ID: {args.oid_id}"
            )

    @command
    @aliases("list-by-org")
    @option(
        "-id",
        "--organization-id",
        help="To list Oracle Internet Directories by organization ID (GUID)",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    def list_by_organization(self, args):
        """
        Returns Oracle Internet Directories by organization ID.
        """
        try:
            fields = self.get_fields(
                GET_ORACLE_INTERNET_DIRECTORIES_ID, oid_fields, Version.DEFAULT
            )
            self.display.v(
                "Listing Oracle Internet Directories for organization ID "
                f"{args.organization_id}"
            )
            oids = self.class_object.list_by_organization(args.organization_id)
            self.display.show(oids, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to list Oracle Internet Directories for "
                f"organization ID: {args.organization_id}"
            )
