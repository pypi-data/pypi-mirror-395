from secrets_safe_library import assets, databases, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_DATABASES,
    GET_DATABASES_ASSET_ID,
    GET_DATABASES_ID,
    POST_DATABASES_ASSET_ID,
    PUT_DATABASES_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.databases import fields as database_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Database(CLIController):
    """
    Controller for managing databases.

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self) -> None:
        super().__init__(
            name="databases",
            help="Databases management commands",
        )

    _class_object_asset: assets.Asset = None

    @property
    def class_object(self) -> databases.Database:
        if self._class_object is None and self.app is not None:
            self._class_object = databases.Database(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def class_object_asset(self) -> assets.Asset:
        if self._class_object_asset is None and self.app is not None:
            self._class_object_asset = assets.Asset(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object_asset

    @command
    @aliases("list")
    def list_databases(self, args):
        """
        Returns all databases to which the current user has access.
        """
        try:
            fields = self.get_fields(GET_DATABASES, database_fields, Version.DEFAULT)
            self.display.v("Calling list_databases function")
            databases = self.class_object.get_databases()
            self.display.show(databases, fields)
            success_msg = "Databases listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list databases")

    @command
    @aliases("get")
    @option(
        "-d-id",
        "--database-id",
        help="To get a database by ID",
        type=int,
        required=True,
    )
    def get_database_by_id(self, args):
        """
        Returns a database by ID.
        """
        try:
            fields = self.get_fields(GET_DATABASES_ID, database_fields, Version.DEFAULT)
            self.display.v(f"Searching by ID {args.database_id}")
            database = self.class_object.get_database_by_id(args.database_id)
            self.display.show(database, fields)
            success_msg = "Database retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to get a database for ID: {args.database_id}"
            )

    def process_multiple_assets(self, assets):
        """
        Process multiple assets and get databases for each asset.
        """
        self.display.v("Processing multiple assets.")
        asset_ids = [asset["AssetID"] for asset in assets if "AssetID" in asset]
        self.display.v(f"Extracted Asset IDs: {asset_ids}")

        for asset_id in asset_ids:
            self.display.v(f"Processing Asset ID: {asset_id}")
            try:
                self.class_object._authentication.get_api_access()
                fields = self.get_fields(
                    GET_DATABASES_ASSET_ID, database_fields, Version.DEFAULT
                )
                self.display.v(
                    "Calling get_databases_by_asset_id function for asset ID"
                    f" {asset_id}"
                )
                database = self.class_object.get_databases_by_asset_id(asset_id)
                self.display.show(database, fields)
                success_msg = (
                    f"Databases for asset ID {asset_id} retrieved successfully"
                )
                self.display.v(success_msg)
            except exceptions.LookupError as e:
                self.display.v(e)
                self.log.error(e)
                print_it(
                    f"It was not possible to get databases for asset ID: {asset_id}"
                )

    @command
    @aliases("get-by-asset")
    @option(
        "-a-id",
        "--asset-id",
        help="The asset ID",
        type=int,
        required=False,
    )
    @option(
        "-a-name",
        "--asset-name",
        help="The asset name",
        type=str,
        required=False,
    )
    def get_databases_by_asset(self, args):
        """
        Returns a list of databases by asset ID or name.
        """
        try:
            if args.asset_id:
                fields = self.get_fields(
                    GET_DATABASES_ASSET_ID, database_fields, Version.DEFAULT
                )
                self.display.v("Calling get_databases_by_asset_id function")
                databases = self.class_object.get_databases_by_asset_id(args.asset_id)
                self.display.show(databases, fields)
                success_msg = (
                    f"Databases for asset ID {args.asset_id} retrieved successfully"
                )
                self.display.v(success_msg)
            elif args.asset_name:
                self.display.v(f"Searching asset by name {args.asset_name}")
                assets = self.class_object_asset.search_assets(
                    asset_name=args.asset_name
                )
                if not (assets and assets.get("Data")):
                    print_it(f"No assets found with name {args.asset_name}")
                    return
                else:
                    self.process_multiple_assets(assets["Data"])
            else:
                print_it("You must provide either an asset ID or an asset name")
                return
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.asset_id:
                print_it(
                    "It was not possible to get databases for asset ID:"
                    f" {args.asset_id}"
                )
            elif args.asset_name:
                print_it(
                    "It was not possible to get databases for asset name:"
                    f" {args.asset_name}"
                )

    @command
    @aliases("create")
    @option(
        "-a-id",
        "--asset-id",
        help="The asset ID",
        type=int,
        required=True,
    )
    @option(
        "-p-id",
        "--platform-id",
        help="The platform ID",
        type=int,
        required=True,
    )
    @option(
        "-p",
        "--port",
        help="The port number",
        type=int,
        required=True,
    )
    @option(
        "-in",
        "--instance-name",
        help="The instance name",
        type=str,
        required=False,
    )
    @option(
        "-is-def-inst",
        "--is-default-instance",
        help="Is default instance",
        action="store_true",
    )
    @option(
        "-v",
        "--version",
        help="The version",
        type=str,
        required=False,
    )
    @option(
        "-t",
        "--template",
        help="The template",
        type=str,
        required=False,
    )
    def create_database_by_asset_id(self, args):
        """
        Creates a new database by asset ID.
        """
        try:
            fields = self.get_fields(
                POST_DATABASES_ASSET_ID, database_fields, Version.DEFAULT
            )
            self.display.v("Calling post_database_by_asset_id function")
            database = self.class_object.post_database_by_asset_id(
                asset_id=args.asset_id,
                platform_id=args.platform_id,
                port=args.port,
                instance_name=args.instance_name,
                is_default_instance=args.is_default_instance,
                version=args.version,
                template=args.template,
            )
            self.display.show(database, fields)
            success_msg = f"Database created successfully for asset ID: {args.asset_id}"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to create a database for asset ID:"
                f" {args.asset_id}"
            )

    @command
    @aliases("update")
    @option(
        "-d-id",
        "--database-id",
        help="The database ID",
        type=int,
        required=True,
    )
    @option(
        "-p-id",
        "--platform-id",
        help="The platform ID",
        type=int,
        required=True,
    )
    @option(
        "-in",
        "--instance-name",
        help="The instance name",
        type=str,
        required=False,
    )
    @option(
        "-is-def-inst",
        "--is-default-instance",
        help="Is default instance",
        action="store_true",
    )
    @option(
        "-p",
        "--port",
        help="The port number",
        type=int,
        default=None,
        required=False,
    )
    @option(
        "-v",
        "--version",
        help="The version",
        type=str,
        default=None,
        required=False,
    )
    @option(
        "-t",
        "--template",
        help="The template",
        type=str,
        default=None,
        required=False,
    )
    def update_database_by_id(self, args):
        """
        Updates a database by ID.
        """
        try:
            get_database = self.class_object.get_database_by_id(args.database_id)
            if not get_database:
                print_it(f"No database found with ID {args.database_id}")
                return

            fields = self.get_fields(PUT_DATABASES_ID, database_fields, Version.DEFAULT)
            self.display.v("Calling put_database_by_id function")
            database = self.class_object.put_database_by_id(
                database_id=args.database_id,
                platform_id=args.platform_id,
                instance_name=(
                    args.instance_name
                    if args.instance_name is not None
                    else get_database["InstanceName"]
                ),
                is_default_instance=(
                    args.is_default_instance
                    if args.is_default_instance is not None
                    else get_database["IsDefaultInstance"]
                ),
                port=(args.port if args.port is not None else get_database["Port"]),
                version=(
                    args.version
                    if args.version is not None
                    else get_database["Version"]
                ),
                template=(
                    args.template
                    if args.template is not None
                    else get_database["Template"]
                ),
            )
            self.display.show(database, fields)
            success_msg = "Database updated successfully"
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to update a database for ID: {args.database_id}"
            )

    @command
    @aliases("delete")
    @option(
        "-d-id",
        "--database-id",
        help="The database ID",
        type=int,
        required=True,
    )
    def delete_database_by_id(self, args):
        """
        Deletes a database by ID.
        """
        try:
            self.display.v("Calling delete_database_by_id function")
            self.class_object.delete_database_by_id(args.database_id)
            success_msg = f"Database with ID {args.database_id} deleted successfully."
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete a database for ID:"
                f" {args.database_id}"
            )
