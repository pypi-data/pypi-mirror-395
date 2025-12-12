import socket

from secrets_safe_library import assets, exceptions, smart_rules, workgroups
from secrets_safe_library.constants.endpoints import (
    GET_ASSETS_ID,
    GET_ASSETS_ID_ATTRIBUTES,
    GET_WORKGROUPS_ID_ASSETS,
    GET_WORKGROUPS_NAME_ASSETS_NAME,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.assets import fields as asset_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Asset(CLIController):
    """
    List, create, retrive, or print BeyondInsight Asset Information
    That API user has rights to.

    See the 'Assets' Section of the PBPS API Guide.
    Requires permissions: Asset Management.
    """

    def __init__(self):
        super().__init__(
            name="assets",
            help="Asset management commands",
        )

    _workgroup_object: workgroups.Workgroup = None
    _smartrule_object: smart_rules.SmartRule = None

    @property
    def class_object(self) -> assets.Asset:
        if self._class_object is None and self.app is not None:
            self._class_object = assets.Asset(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def smartrule_object(self) -> smart_rules.SmartRule:
        if self._smartrule_object is None and self.app is not None:
            self._smartrule_object = smart_rules.SmartRule(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._smartrule_object

    @property
    def workgroup_object(self) -> workgroups.Workgroup:
        if self._workgroup_object is None and self.app is not None:
            self._workgroup_object = workgroups.Workgroup(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._workgroup_object

    @command
    @aliases("list")
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either name or ID is requied",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either name or ID is requied",
        type=int,
        required=False,
    )
    @option(
        "-l",
        "--limit",
        help="Number of records to return. Default 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help=(
            "Number of records to skip before returning records (can only be used in "
            "conjunction with limit). Default 0"
        ),
        type=int,
        required=False,
    )
    def list_assets(self, args):
        """
        Returns a list of assets by Workgroup name (-wgn) or ID (-wgi).
        """
        try:
            if not args.workgroup_id and not args.workgroup_name:
                print_it("Please provide either --workgroup-id or --workgroup-name")
                return

            fields = self.get_fields(
                GET_WORKGROUPS_ID_ASSETS, asset_fields, Version.DEFAULT
            )
            self.display.v("Calling list_assets function")
            assets = self.class_object.list_assets(
                workgroup_id=args.workgroup_id,
                workgroup_name=args.workgroup_name,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(assets, fields)
            success_msg = "Assets listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list assets")

    @command
    @aliases("list-attributes")
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either name or ID is requied if using asset name",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either name or ID is requied if using asset name",
        type=int,
        required=False,
    )
    @option(
        "-id",
        "--asset-id",
        help="Asset ID",
        type=int,
        required=False,
    )
    @option(
        "-an",
        "--asset-name",
        help="Asset name",
        type=str,
        required=False,
    )
    def list_assets_attributes(self, args):
        """
        Returns a list of assets by Asset ID or Asset name (Using Workgroup name (-wgn)
        or ID (-wgi)).
        """
        try:
            if args.asset_id:
                self.display.v("Getting asset attributes using asset ID")
                asset_attributes = self.class_object.list_asset_attributes(
                    asset_id=args.asset_id
                )
            elif args.asset_name:
                if not (args.workgroup_id or args.workgroup_name):
                    print_it(
                        "Please provide either --workgroup-id or --workgroup-name if "
                        "using asset's name"
                    )
                    return

                self.display.v("Getting asset attributes using asset name")
                workgroup = self._get_workgroup_info(
                    args.workgroup_id, args.workgroup_name
                )
                workgroup_name = workgroup.get("Name")

                asset = self.class_object.get_asset_by_workgroup_name(
                    workgroup_name=workgroup_name,
                    asset_name=args.asset_name,
                )
                asset_attributes = self.class_object.list_asset_attributes(
                    asset_id=asset["AssetID"]
                )
            else:
                print_it("Please provide either --asset-id or --asset-name")
                return

            fields = self.get_fields(
                GET_ASSETS_ID_ATTRIBUTES, asset_fields, Version.DEFAULT
            )
            self.display.show(asset_attributes, fields)
            success_msg = "Assets attributes listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list assets' attributes")

    @command
    @aliases("list-by-smart-rule", "list-by-sr")
    @option(
        "-t",
        "--title",
        help="Smart Rule title",
        type=str,
        required=False,
    )
    @option(
        "-id",
        "--smart-rule-id",
        help="Smart Rule ID",
        type=int,
        required=False,
    )
    @option(
        "-l",
        "--limit",
        help="Number of records to return. Default 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help=(
            "Number of records to skip before returning records (can only be used in "
            "conjunction with limit). Default 0"
        ),
        type=int,
        required=False,
    )
    def list_assets_by_smart_rule(self, args):
        """
        Returns a list of assets by Smart Rule title or ID.
        """
        try:
            if args.smart_rule_id:
                self.display.v("Using provided smart rule ID")
                smart_rule_id = args.smart_rule_id
            elif args.title:
                self.display.v("Calling list_by_key function")
                smart_rule = self.smartrule_object.list_by_key("title", args.title)
                smart_rule_id = smart_rule["SmartRuleID"]
            else:
                print_it("Please provide either --title or --smart-rule-id")
                return

            assets = self.smartrule_object.list_assets_by_smart_rule_id(
                smart_rule_id=smart_rule_id,
                limit=args.limit,
                offset=args.offset,
            )

            fields = self.get_fields(GET_ASSETS_ID, asset_fields, Version.DEFAULT)
            self.display.show(assets, fields)
            success_msg = "Assets listed successfully by smart rule"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list assets by smart rule")

    @command
    @aliases("get-by-id")
    @option(
        "-id",
        "--asset-id",
        help="Asset ID",
        type=int,
        required=True,
    )
    def get_asset_by_id(self, args):
        """
        Returns an asset by Asset ID (-id).
        """
        try:
            fields = self.get_fields(GET_ASSETS_ID, asset_fields, Version.DEFAULT)
            self.display.v("Getting asset by ID")
            asset = self.class_object.get_asset_by_id(asset_id=args.asset_id)
            self.display.show(asset, fields)
            success_msg = "Asset retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to get the asset for ID: {args.asset_id}")

    @command
    @aliases("get-by-wg")
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either workgroup name or ID is required",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either workgroup name or ID is required",
        type=int,
        required=False,
    )
    @option(
        "-an",
        "--asset-name",
        help="Asset name",
        type=str,
        required=True,
    )
    def get_asset_by_workgroup(self, args):
        """
        Returns an asset by workgroup name or ID (-wgn | -wgi) and asset name (-an).
        """
        try:
            if not args.workgroup_id and not args.workgroup_name:
                print_it("Please provide either workgroup name (-wgn) or ID (-wgi)")
                return

            fields = self.get_fields(
                GET_WORKGROUPS_NAME_ASSETS_NAME, asset_fields, Version.DEFAULT
            )

            if args.workgroup_id:
                self.display.v("Getting workgroup name using its ID")
                workgroup = self.workgroup_object.get_workgroup_by_id(args.workgroup_id)
                workgroup_name = workgroup["Name"]
            elif args.workgroup_name:
                self.display.v("Getting asset by workgroup name directly")
                workgroup_name = args.workgroup_name

            asset = self.class_object.get_asset_by_workgroup_name(
                workgroup_name=workgroup_name,
                asset_name=args.asset_name,
            )
            self.display.show(asset, fields)
            success_msg = "Asset retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to get the asset")

    @command
    @aliases("search")
    @option("-n", "--asset-name", help="Asset name", type=str)
    @option("-dns", "--dns-name", help="DNS name", type=str)
    @option("-domain", "--domain-name", help="Domain name", type=str)
    @option("-ip", "--ip-address", help="IP address", type=str)
    @option("-mac", "--mac-address", help="MAC address", type=str)
    @option("-t", "--asset-type", help="Asset type", type=str)
    @option(
        "-l",
        "--limit",
        help="Number of records to return. Default 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help=(
            "Number of records to skip before returning records (can only be used in "
            "conjunction with limit). Default 0"
        ),
        type=int,
        required=False,
    )
    def search_assets(self, args):
        """
        Returns a list of assets that match the given search options.

        At least one search option should be provided; any property not provided is
        ignored. All search criteria is case insensitive and is an exact match
        (equality), except for IPAddress.
        """
        try:
            fields = self.get_fields(
                GET_WORKGROUPS_ID_ASSETS, asset_fields, Version.DEFAULT
            )
            self.display.v("Calling search_assets function")
            assets = self.class_object.search_assets(
                asset_name=args.asset_name,
                dns_name=args.dns_name,
                domain_name=args.domain_name,
                ip_address=args.ip_address,
                mac_address=args.mac_address,
                asset_type=args.asset_type,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(assets, fields)
            success_msg = "Assets listed successfully by search"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to search the assets")
        except exceptions.OptionsError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("At least one search option should be provided")

    def get_host_by_name(self, hostname: str) -> str:
        """
        Returns the IP address of a given hostname.
        """
        try:
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.gaierror as e:
            self.display.v(e)
            self.log.error(f"Could not resolve hostname: {hostname} error: {e}")
            return None

    @command
    @aliases("create")
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either workgroup name or ID is required",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either workgroup name or ID is required",
        type=int,
        required=False,
    )
    @option("-ip", "--ip-address", help="IP address", type=str)
    @option("-n", "--asset-name", help="Asset name", type=str)
    @option("-dns", "--dns-name", help="DNS name", type=str)
    @option("-domain", "--domain-name", help="Domain name", type=str)
    @option("-mac", "--mac-address", help="MAC address", type=str)
    @option("-t", "--asset-type", help="Asset type", type=str)
    @option(
        "-d",
        "--description",
        help=(
            "Asset description. Only set if API Version is 3.1 or greater. Max "
            "string length is 255."
        ),
        type=str,
    )
    @option("-os", "--operating-system", help="Operating system", type=str)
    def create_asset(self, args):
        """
        Create a new asset in the Workgroup.
        """
        try:
            if not args.workgroup_id and not args.workgroup_name:
                print_it("Please provide either workgroup name (-wgn) or ID (-wgi)")
                return

            ip_address = self._resolve_ip_address(args)

            # Using same fields for get asset since there's no difference right now.
            fields = self.get_fields(
                GET_WORKGROUPS_ID_ASSETS, asset_fields, Version.DEFAULT
            )
            self.display.v("Calling create_asset function")
            asset = self.class_object.create_asset(
                workgroup_id=args.workgroup_id,
                workgroup_name=args.workgroup_name,
                ip_address=ip_address or args.ip_address,
                asset_name=args.asset_name,
                dns_name=args.dns_name,
                domain_name=args.domain_name,
                mac_address=args.mac_address,
                asset_type=args.asset_type,
                description=args.description,
                operating_system=args.operating_system,
            )
            self.display.show(asset, fields)
            success_msg = "Asset created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the asset")
        except exceptions.OptionsError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Options error: {e}")

    @command
    @aliases("update")
    @option(
        "-pwgn",
        "--prev-workgroup-name",
        help=(
            "Previous Workgroup name, either previous workgroup name or ID is required"
        ),
        type=str,
        required=False,
    )
    @option(
        "-pwgi",
        "--prev-workgroup-id",
        help="Previous Workgroup ID, either previous workgroup name or ID is required",
        type=int,
        required=False,
    )
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either workgroup name or ID is required",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either workgroup name or ID is required",
        type=int,
        required=False,
    )
    @option(
        "-id",
        "--asset-id",
        help=(
            "Asset ID, either asset ID or previous name is required, to identify the "
            "asset to update"
        ),
        type=int,
        required=False,
    )
    @option(
        "-pn",
        "--prev-asset-name",
        help=(
            "Asset previous name, if searching by asset name before updating it. Either"
            " asset name or ID is required"
        ),
        type=str,
    )
    @option("-ip", "--ip-address", help="IP address", type=str)
    @option("-n", "--asset-name", help="New asset name", type=str)
    @option("-dns", "--dns-name", help="DNS name", type=str)
    @option("-domain", "--domain-name", help="Domain name", type=str)
    @option("-mac", "--mac-address", help="MAC address", type=str)
    @option("-t", "--asset-type", help="Asset type", type=str)
    @option(
        "-d",
        "--description",
        help=(
            "Asset description. Only set if API Version is 3.1 or greater. Max "
            "string length is 255."
        ),
        type=str,
    )
    @option("-os", "--operating-system", help="Operating system", type=str)
    def update_asset(self, args):
        """
        Updates an existing asset by Asset ID or Asset and Workgroup's name.
        """
        try:
            # Validate input arguments
            if not self._validate_arguments_to_update(args):
                return

            # Resolve IP address if needed
            ip_address = self._resolve_ip_address(args)

            # Get previous workgroup name
            prev_workgroup = self._get_workgroup_info(
                args.prev_workgroup_id, args.prev_workgroup_name
            )

            # Get workgroup name and ID
            workgroup = self._get_workgroup_info(args.workgroup_id, args.workgroup_name)

            # Get the asset to update
            if args.asset_id:
                self.display.v("Getting asset by ID")
                asset = self.class_object.get_asset_by_id(asset_id=args.asset_id)
            elif args.prev_asset_name:
                self.display.v("Getting asset by workgroup name and asset name")
                asset = self.class_object.get_asset_by_workgroup_name(
                    workgroup_name=prev_workgroup.get("Name") or workgroup.get("Name"),
                    asset_name=args.prev_asset_name,
                )

            # Update the asset
            self._update_asset(asset, workgroup["ID"], ip_address, args)

        except exceptions.LookupError as e:
            self._handle_exception(e, "It was not possible to get the workgroup")
        except exceptions.UpdateError as e:
            self._handle_exception(e, "It was not possible to update the asset")
        except exceptions.OptionsError as e:
            self._handle_exception(e, f"Options error: {e}")

    def _validate_arguments_to_update(self, args):
        """Validate required arguments."""
        if not args.workgroup_id and not args.workgroup_name:
            print_it("Please provide either workgroup name (-wgn) or ID (-wgi)")
            return False

        if (
            not args.prev_workgroup_id
            and not args.prev_workgroup_name
            and not args.asset_id
        ):
            print_it("Please provide either prev. workgroup name (-pwgn) or ID (-pwgi)")
            return False
        return True

    def _validate_asset_name_and_workgroup(
        self, *, asset_id: int, asset_name: str, workgroup_id: int, workgroup_name: str
    ) -> bool:
        """
        Validates the provided asset and workgroup information.
        This method checks if the required parameters for identifying an asset
        and its associated workgroup are provided. It ensures that either an
        asset ID or asset name is specified, and if an asset name is used,
        a workgroup ID or workgroup name must also be provided.
        Args:
            asset_id (int): The unique identifier of the asset.
            asset_name (str): The name of the asset.
            workgroup_id (int): The unique identifier of the workgroup.
            workgroup_name (str): The name of the workgroup.
        Returns:
            bool: True if the input parameters are valid, False otherwise.
        Raises:
            None
        Notes:
            - If neither `asset_id` nor `asset_name` is provided, the method
              will print an error message and return False.
            - If `asset_name` is provided without a corresponding `workgroup_id`
              or `workgroup_name`, the method will print an error message and
              return False.
        """
        if not asset_id and not asset_name:
            print_it("Please provide either asset ID (-id) or asset name (-an)")
            return False

        if asset_name and not (workgroup_id or workgroup_name):
            print_it(
                "Please provide either workgroup name (-wgn) or ID (-wgi) if using "
                "asset's name"
            )
            return False
        return True

    def _resolve_ip_address(self, args):
        """Resolve IP address if it's set to the default placeholder."""
        if args.ip_address == "1.1.1.1":
            self.display.v("Trying to look up IP address instead of 1.1.1.1")
            return self.get_host_by_name(args.asset_name)
        return args.ip_address

    def _get_workgroup_info(self, workgroup_id, workgroup_name) -> dict:
        """Retrieve workgroup using its ID or name."""
        if workgroup_id:
            self.display.v("Getting workgroup by ID")
            workgroup = self.workgroup_object.get_workgroup_by_id(workgroup_id)
            return workgroup
        elif workgroup_name:
            self.display.v("Getting workgroup by name")
            workgroup = self.workgroup_object.get_workgroup_by_name(
                workgroup_name=workgroup_name
            )
            return workgroup
        return {}

    def _get_asset_by_workgroup_id_or_name(
        self, asset_name, workgroup_id=None, workgroup_name=None
    ) -> dict:
        """
        Retrieve an asset by workgroup ID or name and asset name.
        """
        self.display.v("Getting asset by workgroup ID/Name and asset name")
        workgroup = self._get_workgroup_info(workgroup_id, workgroup_name)
        asset = self.class_object.get_asset_by_workgroup_name(
            workgroup_name=workgroup.get("Name"),
            asset_name=asset_name,
        )
        return asset

    def _update_asset(self, asset, workgroup_id, ip_address, args):
        """Perform the asset update."""
        fields = self.get_fields(
            GET_WORKGROUPS_ID_ASSETS, asset_fields, Version.DEFAULT
        )
        self.display.v("Calling update_asset function")
        asset_obj = self.class_object.update_asset(
            asset_id=asset["AssetID"],
            workgroup_id=(workgroup_id or asset.get("WorkgroupID")),
            ip_address=(ip_address or asset.get("IPAddress")),
            asset_name=(args.asset_name or asset.get("AssetName")),
            dns_name=(args.dns_name or asset.get("DnsName")),
            domain_name=(args.domain_name or asset.get("DomainName")),
            mac_address=(args.mac_address or asset.get("MacAddress")),
            asset_type=(args.asset_type or asset.get("AssetType")),
            description=(args.description or asset.get("Description")),
            operating_system=(args.operating_system or asset.get("OperatingSystem")),
        )
        self.display.show(asset_obj, fields)
        success_msg = "Asset updated successfully"
        self.display.v(success_msg)

    def _handle_exception(self, exception, message):
        """Handle exceptions by logging and displaying an error message."""
        self.display.v(exception)
        self.log.error(exception)
        print_it(message)

    @command
    @aliases("delete")
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either workgroup name or ID is required",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either workgroup name or ID is required",
        type=int,
        required=False,
    )
    @option(
        "-id",
        "--asset-id",
        help=(
            "Asset ID, either asset ID or previous name is required, to identify the "
            "asset to delete"
        ),
        type=int,
        required=False,
    )
    @option(
        "-n",
        "--asset-name",
        help=(
            "Asset name, if searching by asset name before deleting it. Either asset "
            "name or ID is required"
        ),
        type=str,
    )
    def delete_asset(self, args):
        """
        Delete an existing asset by Asset ID or Asset and Workgroup's name.
        """
        try:
            if args.asset_id:
                self.display.v("Getting asset by ID")
                self.class_object.delete_asset_by_id(asset_id=args.asset_id)
                success_msg = f"Asset with ID {args.asset_id} deleted successfully."
                print_it(success_msg)
                self.log.info(success_msg)
            elif args.asset_name:
                if not (args.workgroup_name or args.workgroup_id):
                    print_it("Please provide either workgroup name (-wgn) or ID (-wgi)")
                    return

                self.display.v("Getting asset by workgroup name and asset name")
                workgroup = self._get_workgroup_info(
                    args.workgroup_id, args.workgroup_name
                )
                asset = self.class_object.get_asset_by_workgroup_name(
                    workgroup_name=workgroup["Name"],
                    asset_name=args.asset_name,
                )
                self.class_object.delete_asset_by_id(asset_id=asset["AssetID"])
                success_msg = f"Asset with name {args.asset_name} deleted successfully."
                self.display.v(success_msg)
            else:
                print_it("Please provide either asset ID (-id) or asset name (-n)")
                return

        except exceptions.LookupError as e:
            self._handle_exception(e, "It was not possible to get the workgroup")
        except exceptions.DeletionError as e:
            self._handle_exception(e, "It was not possible to delete the asset")
        except exceptions.OptionsError as e:
            self._handle_exception(e, f"Options error: {e}")

    @command
    @aliases("assign-attribute", "add-attribute")
    @option(
        "-aid",
        "--attribute-id",
        help="Attribute ID",
        type=str,
        required=True,
    )
    @option(
        "-id",
        "--asset-id",
        help="Asset ID, either asset ID or name is required",
        type=int,
        required=False,
    )
    @option(
        "-an",
        "--asset-name",
        help="Asset name, either asset ID or name is required",
        type=str,
        required=False,
    )
    @option(
        "-wgn",
        "--workgroup-name",
        help=(
            "Workgroup name, either workgroup name or ID is required if using asset"
            "name"
        ),
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help=(
            "Workgroup ID, either workgroup name or ID is required if using asset"
            "name"
        ),
        type=int,
        required=False,
    )
    def assign_asset_attribute(self, args):
        """
        Assign an attribute to an asset.
        """
        try:
            if not self._validate_asset_name_and_workgroup(
                asset_id=args.asset_id,
                asset_name=args.asset_name,
                workgroup_id=args.workgroup_id,
                workgroup_name=args.workgroup_name,
            ):
                return

            # Get the asset ID
            asset_id = (
                args.asset_id
                or self._get_asset_by_workgroup_id_or_name(
                    asset_name=args.asset_name,
                    workgroup_id=args.workgroup_id,
                    workgroup_name=args.workgroup_name,
                )["AssetID"]
            )

            # Assign the attribute to the asset
            self.display.v("Calling assign_asset_attribute function")
            self.class_object.assign_asset_attribute(
                asset_id=asset_id,
                attribute_id=args.attribute_id,
            )
            success_msg = f"Attribute {args.attribute_id} assigned to asset {asset_id}"
            self.display.v(success_msg)

        except exceptions.CreationError as e:
            self._handle_exception(e, "It was not possible to assign the attribute")

    @command
    @aliases("delete-attribute")
    @option(
        "-aid",
        "--attribute-id",
        help="Attribute ID",
        type=int,
        required=True,
    )
    @option(
        "-id",
        "--asset-id",
        help="Asset ID, either asset ID or name is required",
        type=int,
        required=False,
    )
    @option(
        "-an",
        "--asset-name",
        help="Asset name, either asset ID or name is required",
        type=str,
        required=False,
    )
    @option(
        "-wgn",
        "--workgroup-name",
        help=(
            "Workgroup name, either workgroup name or ID is required if using asset"
            "name"
        ),
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help=(
            "Workgroup ID, either workgroup name or ID is required if using asset"
            "name"
        ),
        type=int,
        required=False,
    )
    def delete_asset_attribute(self, args):
        """
        Delete an attribute from an asset.
        """
        try:
            if not self._validate_asset_name_and_workgroup(
                asset_id=args.asset_id,
                asset_name=args.asset_name,
                workgroup_id=args.workgroup_id,
                workgroup_name=args.workgroup_name,
            ):
                return

            # Get the asset ID
            asset_id = (
                args.asset_id
                or self._get_asset_by_workgroup_id_or_name(
                    asset_name=args.asset_name,
                    workgroup_id=args.workgroup_id,
                    workgroup_name=args.workgroup_name,
                )["AssetID"]
            )

            # Delete the attribute from the asset
            self.display.v("Calling delete_asset_attribute function")
            self.class_object.delete_asset_attribute(
                asset_id=asset_id,
                attribute_id=args.attribute_id,
            )
            success_msg = f"Attribute {args.attribute_id} deleted from asset {asset_id}"
            self.display.v(success_msg)

        except exceptions.DeletionError as e:
            self._handle_exception(e, "It was not possible to delete the attribute")
