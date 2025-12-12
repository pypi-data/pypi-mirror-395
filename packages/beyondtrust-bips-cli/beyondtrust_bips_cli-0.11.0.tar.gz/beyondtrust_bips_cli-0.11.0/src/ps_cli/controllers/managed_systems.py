import argparse

from secrets_safe_library import assets, exceptions, managed_systems, workgroups
from secrets_safe_library.constants.endpoints import (
    GET_MANAGED_SYSTEMS,
    GET_MANAGED_SYSTEMS_ASSETID,
    GET_MANAGED_SYSTEMS_DATABASEID,
    GET_MANAGED_SYSTEMS_FUNCTIONALACCOUNTID,
    GET_MANAGED_SYSTEMS_MANAGEDSYSTEMID,
    GET_MANAGED_SYSTEMS_WORKGROUPID,
    POST_MANAGED_SYSTEMS_ASSETID,
    POST_MANAGED_SYSTEMS_DATABASEID,
    POST_MANAGED_SYSTEMS_WORKGROUPID,
    PUT_MANAGED_SYSTEMS_MANAGEDSYSTEMID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.managed_systems import fields as managed_system_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class ManagedSystem(CLIController):
    """
    Works with Secrets Safe Managed Systems - Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="managed-systems",
            help="Managed Systems management commands",
        )

    _class_object_workgroup: workgroups.Workgroup = None
    _class_object_asset: assets.Asset = None

    @property
    def class_object(self) -> managed_systems.ManagedSystem:
        if self._class_object is None and self.app is not None:
            self._class_object = managed_systems.ManagedSystem(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def class_object_workgroup(self) -> workgroups.Workgroup:
        if self._class_object_workgroup is None and self.app is not None:
            self._class_object_workgroup = workgroups.Workgroup(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object_workgroup

    @property
    def class_object_asset(self) -> assets.Asset:
        if self._class_object_asset is None and self.app is not None:
            self._class_object_asset = assets.Asset(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object_asset

    @command
    @option(
        "id",
        type=int,
        nargs="?",
        default=None,
        help="To get a managed system by ID",
    )
    def list_systems(self, args):
        """
        If no ID is provided, lists all Managed Systems.
        If an ID is provided, gets the Managed System by ID.
        (Short-command).
        """
        try:
            if args.id:
                self.display.v("Getting managed system by ID")
                args = argparse.Namespace(managed_system_id=args.id)
                self.get_managed_system_by_id(args)
            else:
                args = argparse.Namespace(
                    limit=100000,
                    offset=0,
                    name=None,
                    type=None,
                )
                self.list_managed_systems(args)
        except Exception as e:
            self.display.v(e)
            self.log.error(f"Short command error: {e}")
            print_it("It was not possible to list managed systems")

    @command
    @aliases("list")
    @option(
        "-t",
        "--type",
        help="The type of managed system to get",
        type=int,
        required=False,
    )
    @option(
        "-n",
        "--name",
        help="The name of the managed system",
        type=str,
        required=False,
    )
    @option(
        "-l",
        "--limit",
        help="Limit the results. Default is 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help="Records to skip before returning results (use with limit).",
        type=int,
        required=False,
        default=0,
    )
    def list_managed_systems(self, args):
        """
        Returns a list of Managed Systems to which the current user has access.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_SYSTEMS, managed_system_fields, Version.DEFAULT
            )
            self.display.v("Calling list_managed_systems function")
            managed_systems = self.class_object.get_managed_systems(
                type=args.type,
                name=args.name,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(managed_systems, fields)
            success_msg = "Managed systems listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list managed systems")

    @command
    @aliases("get-by-id")
    @option(
        "-id",
        "--managed-system-id",
        help="To get a managed system by ID",
        type=int,
        required=True,
        default=None,
    )
    def get_managed_system_by_id(self, args):
        """
        Returns a Managed System by ID.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_SYSTEMS_MANAGEDSYSTEMID, managed_system_fields
            )
            managed_system = self.class_object.get_managed_system_by_id(
                managed_system_id=args.managed_system_id
            )
            self.display.show(managed_system, fields)
            success_msg = "Managed system retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"No managed system found for ID: {args.managed_system_id}")

    def process_multiple_assets(self, assets):
        """
        Processes a list of assets by their AssetIDs and retrieves managed systems.
        """
        self.display.v("Processing multiple assets.")
        asset_ids = [asset["AssetID"] for asset in assets if "AssetID" in asset]
        self.display.v(f"Extracted Asset IDs: {asset_ids}")

        for asset_id in asset_ids:
            self.display.v(f"Processing Asset ID: {asset_id}")
            try:
                self.class_object._authentication.get_api_access()
                fields = self.get_fields(
                    GET_MANAGED_SYSTEMS_ASSETID, managed_system_fields
                )
                managed_system = self.class_object.get_managed_system_by_asset_id(
                    asset_id=asset_id
                )
                self.display.show(managed_system, fields)
                success_msg = (
                    f"Managed system retrieved successfully for Asset ID: {asset_id}"
                )
                self.display.v(success_msg)
            except exceptions.LookupError as e:
                self.display.v(f"Error processing Asset ID {asset_id}: {e}")
                self.log.error(e)
                print_it(f"No managed system found for Asset ID: {asset_id}")

    @command
    @aliases("get-by-asset")
    @option(
        "-a-id",
        "--asset-id",
        help="The asset ID",
        type=int,
        required=False,
        default=None,
    )
    @option(
        "-a-name",
        "--asset-name",
        help="The asset name",
        type=str,
        required=False,
        default=None,
    )
    def get_managed_system_by_asset(self, args):
        """
        Returns a Managed System by Asset ID or Asset Name.
        """
        try:
            if args.asset_id and args.asset_name:
                print_it("Please provide only one of asset ID or asset name, not both.")
                return

            if not any([args.asset_id, args.asset_name]):
                print_it("Please provide either asset ID or asset name")
                return

            if args.asset_id:
                asset_id = args.asset_id
                self.display.v(f"Asset ID was provided: {args.asset_id}")
                fields = self.get_fields(
                    GET_MANAGED_SYSTEMS_ASSETID, managed_system_fields
                )
                managed_system = self.class_object.get_managed_system_by_asset_id(
                    asset_id=asset_id
                )
                self.display.show(managed_system, fields)
                success_msg = (
                    f"Managed system retrieved successfully for Asset ID: {asset_id}"
                )
                self.display.v(success_msg)
            else:
                self.display.v(f"Searching asset by name {args.asset_name}")
                assets = self.class_object_asset.search_assets(
                    asset_name=args.asset_name
                )

                if not assets or "Data" not in assets or not assets["Data"]:
                    print_it(f"No assets found with name {args.asset_name}")
                    return
                else:
                    self.process_multiple_assets(assets["Data"])
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"No managed system found for Asset ID: {args.asset_id}")

    @command
    @aliases("get-by-database-id")
    @option(
        "-d",
        "--database-id",
        help="The database ID",
        type=int,
        required=True,
        default=None,
    )
    def get_managed_system_by_database_id(self, args):
        """
        Returns a Managed System by Database ID.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_SYSTEMS_DATABASEID, managed_system_fields
            )
            managed_system = self.class_object.get_managed_system_by_database_id(
                database_id=args.database_id
            )
            self.display.show(managed_system, fields)
            success_msg = "Managed system retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"No managed system found for Database ID: {args.database_id}")

    @command
    @aliases("get-by-functional-account-id")
    @option(
        "-f",
        "--functional-account-id",
        help="The functional account ID",
        type=int,
        required=True,
        default=None,
    )
    @option(
        "-t",
        "--type",
        help="The type of managed system to get",
        type=int,
        required=False,
    )
    @option(
        "-n",
        "--name",
        help="The name of the managed system",
        type=str,
        required=False,
    )
    @option(
        "-l",
        "--limit",
        help="Limit the results. Default is 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help="Records to skip before returning results (use with limit).",
        type=int,
        required=False,
        default=0,
    )
    def get_managed_system_by_functional_account_id(self, args):
        """
        Returns a list of managed systems auto-managed by the functional account
        referenced by ID.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_SYSTEMS_FUNCTIONALACCOUNTID, managed_system_fields
            )
            managed_system = (
                self.class_object.get_managed_system_by_functional_account_id(
                    functional_account_id=args.functional_account_id,
                    type=args.type,
                    name=args.name,
                    limit=args.limit,
                    offset=args.offset,
                )
            )
            self.display.show(managed_system, fields)
            success_msg = "Managed system retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"No managed system found for Functional Account ID: "
                f"{args.functional_account_id}"
            )

    @command
    @aliases("get-by-workgroup-id")
    @option(
        "-w",
        "--workgroup-id",
        help="The workgroup ID",
        type=int,
        required=True,
        default=None,
    )
    @option(
        "-l",
        "--limit",
        help="Limit the results. Default is 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help="Records to skip before returning results (use with limit).",
        type=int,
        required=False,
        default=0,
    )
    def get_managed_system_by_workgroup_id(self, args):
        """
        Returns a list of managed systems by the workgroup referenced
        by ID.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_SYSTEMS_WORKGROUPID, managed_system_fields
            )
            managed_system = self.class_object.get_managed_system_by_workgroup_id(
                workgroup_id=args.workgroup_id,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(managed_system, fields)
            success_msg = "Managed system retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"No managed system found for Workgroup ID: {args.workgroup_id}")

    @command
    @aliases("create-by-asset")
    @option(
        "-a",
        "--asset-id",
        help="The asset ID",
        type=int,
        required=False,
        default=None,
    )
    @option(
        "-a-name",
        "--asset-name",
        help="The asset name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-w-name",
        "--workgroup-name",
        help="The workgroup name",
        type=str,
        required=False,
    )
    @option(
        "-p",
        "--platform-id",
        help="The platform ID",
        type=int,
        required=True,
    )
    @option(
        "-e",
        "--contact-email",
        help="The contact email",
        type=str,
        required=True,
    )
    @option(
        "-d",
        "--description",
        help="The description",
        type=str,
        required=True,
    )
    @option(
        "--port",
        help="The port number",
        type=int,
        required=False,
    )
    @option(
        "--timeout",
        help="The timeout value",
        type=int,
        default=30,
        required=True,
    )
    @option(
        "--ssh-key-enforcement-mode",
        help="The SSH key enforcement mode",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--password-rule-id",
        help="The password rule ID",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--dss-key-rule-id",
        help="The DSS key rule ID",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--login-account-id",
        help="The login account ID",
        type=int,
        required=False,
    )
    @option(
        "--release-duration",
        help="The release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--max-release-duration",
        help="The maximum release duration",
        type=int,
        default=525600,
        required=False,
    )
    @option(
        "--isa-release-duration",
        help="The ISA release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--auto-management-flag",
        help="The auto-management flag",
        action="store_true",
    )
    @option(
        "--functional-account-id",
        help="The functional account ID",
        type=int,
        required=False,
    )
    @option(
        "--elevation-command",
        help="The elevation command",
        type=str,
        choices=["sudo", "pbrun", "pmrun"],
        required=False,
    )
    @option(
        "--check-password-flag",
        help="The check password flag",
        action="store_true",
    )
    @option(
        "--change-password-after-any-release-flag",
        help="The change password after any release flag",
        action="store_true",
    )
    @option(
        "--reset-password-on-mismatch-flag",
        help="The reset password on mismatch flag",
        action="store_true",
    )
    @option(
        "--change-frequency-type",
        help="The change frequency type",
        type=str,
        default="first",
        choices=["first", "last", "xdays"],
        required=True,
    )
    @option(
        "--change-frequency-days",
        help="The change frequency in days",
        type=int,
        required=False,
    )
    @option(
        "--change-time",
        help="The change time",
        type=str,
        default="23:30",
        required=True,
    )
    @option(
        "--remote-client-type",
        help="The remote client type",
        type=str,
        required=False,
    )
    @option(
        "--application-host-id",
        help="The application host ID",
        type=int,
        default=None,
        required=False,
    )
    @option(
        "--is-application-host",
        help="Whether it is an application host",
        action="store_true",
    )
    def create_managed_system_by_asset(self, args):
        """
        Creates a new Managed System using the asset ID.
        """
        try:
            if not any([args.asset_id, all([args.asset_name, args.workgroup_name])]):
                print_it(
                    "Please provide either asset ID or asset name with workgroup name"
                )
                return

            if args.asset_id:
                asset_id = args.asset_id
                self.display.v(f"Asset ID was provided: {args.asset_id}")
            else:
                self.display.v(
                    f"Searching asset by name {args.asset_name},"
                    f" and workgroup name {args.workgroup_name}."
                )
                assets = self.class_object_asset.get_asset_by_workgroup_name(
                    asset_name=args.asset_name, workgroup_name=args.workgroup_name
                )

                if not assets:
                    print_it(
                        f"No assets found with name {args.asset_name},"
                        f" and workgroup name {args.workgroup_name}."
                    )
                    return
                elif isinstance(assets, dict):
                    asset_id = assets["AssetID"]
                    self.display.v(f"Found asset with ID: {asset_id}")
                else:
                    print_it(
                        "Can't continue since multiple assets matched name "
                        f"{args.asset_name} and workgroup name {args.workgroup_name}"
                    )
                    return

            fields = self.get_fields(
                POST_MANAGED_SYSTEMS_ASSETID, managed_system_fields
            )
            self.display.v("Calling create_managed_system_by_asset function")
            managed_system, status_code = (
                self.class_object.post_managed_system_by_asset_id(
                    asset_id=asset_id,
                    platform_id=args.platform_id,
                    contact_email=args.contact_email,
                    description=args.description,
                    port=args.port,
                    timeout=args.timeout,
                    ssh_key_enforcement_mode=args.ssh_key_enforcement_mode,
                    password_rule_id=args.password_rule_id,
                    dss_key_rule_id=args.dss_key_rule_id,
                    login_account_id=args.login_account_id,
                    release_duration=args.release_duration,
                    max_release_duration=args.max_release_duration,
                    isa_release_duration=args.isa_release_duration,
                    auto_management_flag=args.auto_management_flag,
                    functional_account_id=args.functional_account_id,
                    elevation_command=args.elevation_command,
                    check_password_flag=args.check_password_flag,
                    change_password_after_any_release_flag=(
                        args.change_password_after_any_release_flag
                    ),
                    reset_password_on_mismatch_flag=(
                        args.reset_password_on_mismatch_flag
                    ),
                    change_frequency_type=args.change_frequency_type,
                    change_frequency_days=args.change_frequency_days,
                    change_time=args.change_time,
                    remote_client_type=args.remote_client_type,
                    application_host_id=args.application_host_id,
                    is_application_host=args.is_application_host,
                )
            )
            self.display.show(managed_system, fields)
            if status_code == 201:
                self.display.v("Managed system created successfully")
            else:
                self.display.v("Managed system is already created")
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the managed system")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"No asset found for name: {args.asset_name},"
                f" and workgroup name: {args.workgroup_name}."
            )

    @command
    @aliases("create-by-database-id")
    @option(
        "-d",
        "--database-id",
        help="The database ID",
        type=int,
        required=True,
    )
    @option(
        "-e",
        "--contact-email",
        help="The contact email",
        type=str,
        required=True,
    )
    @option(
        "-desc",
        "--description",
        help="The description",
        type=str,
        required=True,
    )
    @option(
        "--timeout",
        help="The timeout value",
        type=int,
        default=30,
        required=True,
    )
    @option(
        "--password-rule-id",
        help="The password rule ID",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--release-duration",
        help="The release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--max-release-duration",
        help="The maximum release duration",
        type=int,
        default=525600,
        required=False,
    )
    @option(
        "--isa-release-duration",
        help="The ISA release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--auto-management-flag",
        help="The auto-management flag",
        action="store_true",
    )
    @option(
        "--check-password-flag",
        help="The check password flag",
        action="store_true",
    )
    @option(
        "--change-password-after-any-release-flag",
        help="The change password after any release flag",
        action="store_true",
    )
    @option(
        "--reset-password-on-mismatch-flag",
        help="The reset password on mismatch flag",
        action="store_true",
    )
    @option(
        "--change-frequency-type",
        help="The change frequency type",
        type=str,
        default="first",
        choices=["first", "last", "xdays"],
        required=True,
    )
    @option(
        "--change-frequency-days",
        help="The change frequency in days",
        type=int,
        required=False,
    )
    @option(
        "--change-time",
        help="The change time",
        type=str,
        default="23:30",
        required=True,
    )
    @option(
        "--functional-account-id",
        help="The functional account ID",
        type=int,
        required=False,
    )
    def create_managed_system_by_database_id(self, args):
        """
        Creates a new Managed System using the database ID.
        """
        try:
            fields = self.get_fields(
                POST_MANAGED_SYSTEMS_DATABASEID, managed_system_fields
            )
            self.display.v("Calling create_managed_system_by_database_id function")
            managed_system, status_code = (
                self.class_object.post_managed_system_by_database_id(
                    database_id=args.database_id,
                    contact_email=args.contact_email,
                    description=args.description,
                    timeout=args.timeout,
                    password_rule_id=args.password_rule_id,
                    release_duration=args.release_duration,
                    max_release_duration=args.max_release_duration,
                    isa_release_duration=args.isa_release_duration,
                    auto_management_flag=args.auto_management_flag,
                    check_password_flag=args.check_password_flag,
                    change_password_after_any_release_flag=(
                        args.change_password_after_any_release_flag
                    ),
                    reset_password_on_mismatch_flag=(
                        args.reset_password_on_mismatch_flag
                    ),
                    change_frequency_type=args.change_frequency_type,
                    change_frequency_days=args.change_frequency_days,
                    change_time=args.change_time,
                    functional_account_id=args.functional_account_id,
                )
            )
            self.display.show(managed_system, fields)
            if status_code == 201:
                self.display.v("Managed system created successfully")
            else:
                self.display.v("Managed system is already created")
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the managed system")
            print_it(f"Error: {e}")

    @command
    @aliases("create-by-workgroup-id")
    @option("-w", "--workgroup-id", help="The workgroup ID", type=int, required=False)
    @option(
        "-w-name",
        "--workgroup-name",
        help="The workgroup name",
        type=str,
        required=False,
    )
    @option(
        "-e", "--entity-type-id", help="The entity type ID", type=int, required=True
    )
    @option("--host-name", help="The host name", type=str, required=True)
    @option("--ip-address", help="The IP address", type=str, required=True)
    @option("--dns-name", help="The DNS name", type=str, required=True)
    @option("--instance-name", help="The instance name", type=str, required=True)
    @option("--template", help="The template", type=str, required=True)
    @option("--forest-name", help="The forest name", type=str, required=True)
    @option("-p", "--platform-id", help="The platform ID", type=int, required=True)
    @option("--net-bios-name", help="The NetBIOS name", type=str, required=True)
    @option("-c", "--contact-email", help="The contact email", type=str, required=True)
    @option("-d", "--description", help="The description", type=str, required=True)
    @option("--timeout", help="The timeout value", type=int, default=30, required=True)
    @option(
        "--password-rule-id",
        help="The password rule ID",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--account-name-format",
        help="The account name format",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--oracle-internet-directory-service-name",
        help="The Oracle Internet Directory service name",
        type=str,
        required=False,
    )
    @option(
        "--release-duration",
        help="The release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--max-release-duration",
        help="The maximum release duration",
        type=int,
        default=525600,
        required=False,
    )
    @option(
        "--isa-release-duration",
        help="The ISA release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--auto-management-flag",
        help="The auto-management flag",
        action="store_true",
    )
    @option(
        "--check-password-flag",
        help="The check password flag",
        action="store_true",
    )
    @option(
        "--change-password-after-any-release-flag",
        help="Change password after any release flag",
        action="store_true",
    )
    @option(
        "--reset-password-on-mismatch-flag",
        help="Reset password on mismatch flag",
        action="store_true",
    )
    @option(
        "--change-frequency-type",
        help="The change frequency type",
        type=str,
        default="first",
        choices=["first", "last", "xdays"],
        required=True,
    )
    @option(
        "--change-frequency-days",
        help="The change frequency in days",
        type=int,
        required=False,
    )
    @option(
        "--change-time",
        help="The change time",
        type=str,
        default="23:30",
        required=True,
    )
    @option(
        "--remote-client-type", help="The remote client type", type=str, required=False
    )
    @option(
        "--is-application-host",
        help="Whether it is an application host",
        action="store_true",
    )
    @option(
        "--access-url", help="The URL used for cloud access", type=str, required=False
    )
    @option(
        "--is-default-instance",
        help="Whether it is the default instance",
        action="store_true",
    )
    @option(
        "--use-ssl",
        help="Whether to use SSL",
        action="store_true",
    )
    @option("--port", help="The port number", type=int, required=False)
    @option(
        "--ssh-key-enforcement-mode",
        help="The SSH key enforcement mode",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--dss-key-rule-id",
        help="The DSS key rule ID",
        type=int,
        default=0,
        required=False,
    )
    @option("--login-account-id", help="The login account ID", type=int, required=False)
    @option(
        "--oracle-internet-directory-id",
        help="The Oracle Internet Directory ID",
        type=int,
        required=False,
    )
    @option(
        "--functional-account-id",
        help="The functional account ID",
        type=int,
        required=False,
    )
    @option(
        "--elevation-command",
        help="The elevation command",
        choices=["sudo", "pbrun", "pmrun"],
        type=str,
        required=False,
    )
    @option(
        "--application-host-id",
        help="The application host ID",
        type=int,
        required=False,
    )
    def create_managed_system_by_workgroup(self, args):
        """
        Creates a new Managed System using the workgroup ID or name.
        If both workgroup ID and name are provided, the ID will be used.
        If neither is provided, an error will be raised.
        """
        try:
            if not any([args.workgroup_id, args.workgroup_name]):
                print_it("Please provide either workgroup ID or workgroup name")
                return

            if args.workgroup_id:
                workgroup_id = args.workgroup_id
                self.display.v(f"Workgroup ID was provided: {args.workgroup_id}")
            else:
                self.display.v(f"Searching workgroup by name {args.workgroup_name}")
                workgroups = self.class_object_workgroup.get_workgroup_by_name(
                    workgroup_name=args.workgroup_name
                )

                if not workgroups:
                    print_it(f"No workgroups found with name {args.workgroup_name}")
                    return
                elif isinstance(workgroups, dict):
                    workgroup_id = workgroups["ID"]
                    self.display.v(f"Found workgroup with ID: {workgroup_id}")
                else:
                    print_it(
                        "Can't continue since multiple workgroups matched name "
                        f"{args.workgroup_name}"
                    )
                    return

            fields = self.get_fields(
                POST_MANAGED_SYSTEMS_WORKGROUPID, managed_system_fields
            )
            self.display.v("Calling create_managed_system_by_workgroup function")
            managed_system, status_code = (
                self.class_object.post_managed_system_by_workgroup_id(
                    workgroup_id=workgroup_id,
                    entity_type_id=args.entity_type_id,
                    host_name=args.host_name,
                    ip_address=args.ip_address,
                    dns_name=args.dns_name,
                    instance_name=args.instance_name,
                    template=args.template,
                    forest_name=args.forest_name,
                    platform_id=args.platform_id,
                    net_bios_name=args.net_bios_name,
                    contact_email=args.contact_email,
                    description=args.description,
                    timeout=args.timeout,
                    password_rule_id=args.password_rule_id,
                    account_name_format=args.account_name_format,
                    oracle_internet_directory_service_name=(
                        args.oracle_internet_directory_service_name
                    ),
                    release_duration=args.release_duration,
                    max_release_duration=args.max_release_duration,
                    isa_release_duration=args.isa_release_duration,
                    auto_management_flag=args.auto_management_flag,
                    check_password_flag=args.check_password_flag,
                    change_password_after_any_release_flag=(
                        args.change_password_after_any_release_flag
                    ),
                    reset_password_on_mismatch_flag=(
                        args.reset_password_on_mismatch_flag
                    ),
                    change_frequency_type=args.change_frequency_type,
                    change_frequency_days=args.change_frequency_days,
                    change_time=args.change_time,
                    remote_client_type=args.remote_client_type,
                    is_application_host=args.is_application_host,
                    access_url=args.access_url,
                    is_default_instance=args.is_default_instance,
                    use_ssl=args.use_ssl,
                    port=args.port,
                    ssh_key_enforcement_mode=args.ssh_key_enforcement_mode,
                    dss_key_rule_id=args.dss_key_rule_id,
                    login_account_id=args.login_account_id,
                    oracle_internet_directory_id=args.oracle_internet_directory_id,
                    functional_account_id=args.functional_account_id,
                    elevation_command=args.elevation_command,
                    application_host_id=args.application_host_id,
                )
            )
            self.display.show(managed_system, fields)
            if status_code == 201:
                self.display.v("Managed system created successfully")
            else:
                self.display.v("Managed system is already created")
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the managed system")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"No workgroup found by name: {args.workgroup_name}")

    @command
    @aliases("delete-by-id", "delete")
    @option(
        "-id",
        "--managed-system-id",
        help="The managed system ID",
        type=int,
        required=True,
    )
    def delete_managed_system_by_id(self, args):
        """
        Deletes a Managed System by ID.
        """
        try:
            self.display.v(f"Deleting managed system by ID {args.managed_system_id}")
            self.class_object.delete_managed_system_by_id(
                managed_system_id=args.managed_system_id
            )
            success_msg = (
                f"Managed system deleted successfully {args.managed_system_id}"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(
                f"It was not possible to delete a managed system for ID: "
                f"{args.managed_system_id}"
            )

    @command
    @aliases("update-by-id")
    @option(
        "-id",
        "--managed-system-id",
        help="The managed system ID",
        type=int,
        required=True,
    )
    @option("-w", "--workgroup-id", help="The workgroup ID", type=int, required=False)
    @option("--host-name", help="The host name", type=str, required=True)
    @option("--ip-address", help="The IP address", type=str, required=True)
    @option("--dns-name", help="The DNS name", type=str, required=True)
    @option("--instance-name", help="The instance name", type=str, required=True)
    @option("--template", help="The template", type=str, required=True)
    @option("--forest-name", help="The forest name", type=str, required=True)
    @option("-p", "--platform-id", help="The platform ID", type=int, required=True)
    @option("--net-bios-name", help="The NetBIOS name", type=str, required=True)
    @option("-c", "--contact-email", help="The contact email", type=str, required=True)
    @option("-d", "--description", help="The description", type=str, required=True)
    @option("--timeout", help="The timeout value", type=int, default=30, required=True)
    @option(
        "--password-rule-id",
        help="The password rule ID",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--release-duration",
        help="The release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--max-release-duration",
        help="The maximum release duration",
        type=int,
        default=525600,
        required=False,
    )
    @option(
        "--isa-release-duration",
        help="The ISA release duration",
        type=int,
        default=120,
        required=False,
    )
    @option(
        "--auto-management-flag",
        help="The auto-management flag",
        action="store_true",
    )
    @option(
        "--check-password-flag",
        help="The check password flag",
        action="store_true",
    )
    @option(
        "--change-password-after-any-release-flag",
        help="Change password after any release flag",
        action="store_true",
    )
    @option(
        "--reset-password-on-mismatch-flag",
        help="Reset password on mismatch flag",
        action="store_true",
    )
    @option(
        "--change-frequency-type",
        help="The change frequency type",
        type=str,
        default="first",
        choices=["first", "last", "xdays"],
        required=True,
    )
    @option(
        "--change-frequency-days",
        help="The change frequency in days",
        type=int,
        required=False,
    )
    @option(
        "--change-time",
        help="The change time",
        type=str,
        default="23:30",
        required=True,
    )
    @option(
        "--remote-client-type", help="The remote client type", type=str, required=False
    )
    @option(
        "--is-application-host",
        help="Whether it is an application host",
        action="store_true",
    )
    @option(
        "--access-url", help="The URL used for cloud access", type=str, required=False
    )
    @option(
        "--is-default-instance",
        help="Whether it is the default instance",
        action="store_true",
    )
    @option(
        "--use-ssl",
        help="Whether to use SSL",
        action="store_true",
    )
    @option("--port", help="The port number", type=int, required=False)
    @option(
        "--ssh-key-enforcement-mode",
        help="The SSH key enforcement mode",
        type=int,
        default=0,
        required=False,
    )
    @option(
        "--dss-key-rule-id",
        help="The DSS key rule ID",
        type=int,
        default=0,
        required=False,
    )
    @option("--login-account-id", help="The login account ID", type=int, required=False)
    @option(
        "--functional-account-id",
        help="The functional account ID",
        type=int,
        required=False,
    )
    @option(
        "--elevation-command",
        help="The elevation command",
        choices=["sudo", "pbrun", "pmrun"],
        type=str,
        required=False,
    )
    @option(
        "--application-host-id",
        help="The application host ID",
        type=int,
        required=False,
    )
    def update_managed_system_by_id(self, args):
        """
        Updates a Managed System by ID.
        """
        try:
            fields = self.get_fields(
                PUT_MANAGED_SYSTEMS_MANAGEDSYSTEMID, managed_system_fields
            )

            self.display.v(f"Updating managed system by ID {args.managed_system_id}")
            managed_system = self.class_object.put_managed_system_by_id(
                managed_system_id=args.managed_system_id,
                workgroup_id=args.workgroup_id,
                host_name=args.host_name,
                ip_address=args.ip_address,
                dns_name=args.dns_name,
                instance_name=args.instance_name,
                template=args.template,
                forest_name=args.forest_name,
                platform_id=args.platform_id,
                net_bios_name=args.net_bios_name,
                contact_email=args.contact_email,
                description=args.description,
                timeout=args.timeout,
                password_rule_id=args.password_rule_id,
                release_duration=args.release_duration,
                max_release_duration=args.max_release_duration,
                isa_release_duration=args.isa_release_duration,
                auto_management_flag=args.auto_management_flag,
                check_password_flag=args.check_password_flag,
                change_password_after_any_release_flag=(
                    args.change_password_after_any_release_flag
                ),
                reset_password_on_mismatch_flag=(args.reset_password_on_mismatch_flag),
                change_frequency_type=args.change_frequency_type,
                change_frequency_days=args.change_frequency_days,
                change_time=args.change_time,
                remote_client_type=args.remote_client_type,
                is_application_host=args.is_application_host,
                access_url=args.access_url,
                is_default_instance=args.is_default_instance,
                use_ssl=args.use_ssl,
                port=args.port,
                ssh_key_enforcement_mode=args.ssh_key_enforcement_mode,
                dss_key_rule_id=args.dss_key_rule_id,
                login_account_id=args.login_account_id,
                functional_account_id=args.functional_account_id,
                elevation_command=args.elevation_command,
                application_host_id=args.application_host_id,
            )
            self.display.show(managed_system, fields)
            success_msg = (
                f"Managed system updated successfully ID: {args.managed_system_id}"
            )
            print_it(success_msg)
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            print_it(
                f"It was not possible to update the managed system for "
                f"ID: {args.managed_system_id}"
            )
            print_it(f"Error: {e}")
