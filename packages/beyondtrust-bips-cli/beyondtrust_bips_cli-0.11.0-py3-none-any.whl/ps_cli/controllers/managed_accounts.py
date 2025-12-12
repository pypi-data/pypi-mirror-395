import argparse

from secrets_safe_library import exceptions, managed_account, quick_rules, smart_rules
from secrets_safe_library.constants.endpoints import (
    GET_MANAGED_ACCOUNTS_ID,
    GET_MANAGED_ACCOUNTS_ID_ATTRIBUTES,
    GET_MANAGED_SYSTEMS_SYSTEM_ID_MANAGED_ACCOUNTS,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.managed_accounts import (
    fields as managed_account_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class ManagedAccount(CLIController):
    """
    Create, Delete, List, retrive, or print BeyondInsight ManagedAccounts that API user
    has rights to.

    Requires PasswordSafe Account Management (Read/Write, depending)
    """

    def __init__(self):
        super().__init__(
            name="managed-accounts",
            help="Managed accounts management commands",
        )

    _smart_rule_object: smart_rules.SmartRule | None = None
    _quick_rule_object: quick_rules.QuickRule | None = None

    @property
    def class_object(self) -> managed_account.ManagedAccount:
        if self._class_object is None and self.app is not None:
            self._class_object = managed_account.ManagedAccount(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def smart_rule_object(self) -> smart_rules.SmartRule:
        if self._smart_rule_object is None and self.app is not None:
            self._smart_rule_object = smart_rules.SmartRule(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._smart_rule_object

    @property
    def quick_rule_object(self) -> quick_rules.QuickRule:
        if self._quick_rule_object is None and self.app is not None:
            self._quick_rule_object = quick_rules.QuickRule(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._quick_rule_object

    @command
    @option(
        "type",
        help="The type of the managed account to return. Options are: "
        "'system', 'recent', 'domainlinked', 'database', 'cloud', 'application'.",
        type=str,
        nargs="?",
        default=None,
        choices=[
            "system",
            "recent",
            "domainlinked",
            "database",
            "cloud",
            "application",
        ],
    )
    @option(
        "workgroup_name",
        help="To get a managed account by workgroup name",
        type=str,
        nargs="?",
        default=None,
    )
    @option(
        "account_name",
        help="To get a managed account by managed account name",
        type=str,
        nargs="?",
        default=None,
    )
    @option(
        "system_name",
        help="To get a managed account by managed system name",
        type=str,
        nargs="?",
        default=None,
    )
    def list_accounts(self, args):
        """
        Returns a list of all managed accounts by Managed System name, Account name,
        Workgroup name, and Account type.
        (Short-command).
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_ACCOUNTS_ID, managed_account_fields, Version.DEFAULT
            )
            self.display.v("Calling get_managed_accounts function")
            managed_accounts = self.class_object.get_managed_accounts(
                system_name=args.system_name,
                account_name=args.account_name,
                workgroup_name=args.workgroup_name,
                type=args.type,
            )
            if isinstance(managed_accounts, dict):
                # If a single account is returned, wrap it in a list
                # to maintain consistency with how multiple accounts are handled
                managed_accounts = [managed_accounts]

                managed_account_list = [
                    account
                    for account in managed_accounts
                    if account.get("AccountName") == args.account_name
                ]
                self.display.show(managed_account_list, fields)
            else:
                self.display.show(managed_accounts, fields)
        except Exception as e:
            self.display.v(e)
            self.log.error(f"Short command error: {e}")
            print_it("It was not possible to list managed accounts")

    @command
    @aliases("list")
    @option(
        "-id",
        "--managed-system-id",
        help="Managed System ID",
        type=int,
        required=True,
    )
    def list_managed_accounts(self, args):
        """
        Returns a list of managed accounts by managed system ID.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_SYSTEMS_SYSTEM_ID_MANAGED_ACCOUNTS,
                managed_account_fields,
                Version.DEFAULT,
            )
            self.display.v("Calling list_by_managed_system function")
            managed_accounts = self.class_object.list_by_managed_system(
                managed_system_id=args.managed_system_id
            )
            self.display.show(managed_accounts, fields)
            success_msg = "Managed accounts listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list managed accounts")

    @command
    @aliases("get")
    @option(
        "-id",
        "--account-id",
        help="To get a managed account by ID",
        type=int,
        required=False,
    )
    @option(
        "-an",
        "--account-name",
        help="To get a managed account by name and managed system name",
        type=str,
        required=False,
    )
    @option(
        "-sn",
        "--system-name",
        help="To get a managed account by name and managed system name",
        type=str,
        required=False,
    )
    def get_managed_account(self, args):
        """
        Returns a managed account by ID or a list when searching by Account and
        System's name.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_ACCOUNTS_ID, managed_account_fields, Version.DEFAULT
            )

            if args.account_id:
                self.display.v("Searching directly by account ID")
                managed_account = self.class_object.get_by_id(args.account_id)
                self.display.show(managed_account, fields)
            elif args.account_name and args.system_name:
                self.display.v("Searching by account and system's name")
                managed_accounts = self.class_object.get_managed_accounts(
                    account_name=args.account_name,
                    system_name=args.system_name,
                )

                if isinstance(managed_accounts, dict):
                    # If a single account is returned, wrap it in a list
                    # to maintain consistency with how multiple accounts are handled
                    managed_accounts = [managed_accounts]

                managed_account_list = [
                    account
                    for account in managed_accounts
                    if account.get("AccountName") == args.account_name
                ]
                self.display.show(managed_account_list, fields)
            else:
                print_it(
                    "You must provide either an account ID or both an account name and "
                    "a system name"
                )
                return
            success_msg = "Managed account retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.account_id:
                print_it(
                    "It was not possible to get a managed account for ID: "
                    f"{args.account_id}"
                )
            else:
                print_it(
                    "It was not possible to get a managed account for Account Name: "
                    f"{args.account_name} and System Name: {args.system_name}"
                )

    @command
    @aliases("list-by-smart-rule", "list-by-sr")
    @option(
        "-id",
        "--smart-rule-id",
        help="To list managed accounts by Smart Rule ID",
        type=int,
        required=False,
    )
    @option(
        "-t",
        "--smart-rule-title",
        help="To list managed accounts by Smart Rule Title",
        type=str,
        required=False,
    )
    def list_managed_accounts_by_smart_rule(self, args):
        """
        List managed accounts by Smart Rule's ID or Title.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_ACCOUNTS_ID, managed_account_fields, Version.DEFAULT
            )
            if args.smart_rule_id:
                self.display.v(f"Searching by Smart Rule ID {args.smart_rule_id}")
                managed_accounts = self.class_object.list_by_smart_rule_id(
                    smart_rule_id=args.smart_rule_id
                )
            elif args.smart_rule_title:
                self.display.v(f"Searching by Smart Rule Name {args.smart_rule_title}")
                smart_rule = self.smart_rule_object.list_by_key(
                    "title", args.smart_rule_title
                )

                if not smart_rule:
                    print_it(
                        f"Smart Rule with title {args.smart_rule_title} not found."
                    )
                    return

                managed_accounts = self.class_object.list_by_smart_rule_id(
                    smart_rule_id=smart_rule.get("SmartRuleID")
                )
            else:
                print_it("You must provide either a Smart Rule ID or a Smart Rule Name")
                return
            self.display.show(managed_accounts, fields)
            success_msg = "Managed accounts listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.smart_rule_id:
                print_it(
                    "It was not possible to get a managed account for Smart Rule ID: "
                    f"{args.smart_rule_id}"
                )
            else:
                print_it(
                    "It was not possible to get a managed account for Smart Rule "
                    f"Title: {args.smart_rule_title}"
                )

    @command
    @aliases("list-by-quick-rule", "list-by-qr")
    @option(
        "-id",
        "--quick-rule-id",
        help="To list managed accounts by Quick Rule ID",
        type=int,
        required=False,
    )
    @option(
        "-t",
        "--quick-rule-title",
        help="To list managed accounts by Quick Rule Title",
        type=str,
        required=False,
    )
    def list_managed_accounts_by_quick_rule(self, args):
        """
        List managed accounts by Quick Rule's ID or Title.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_ACCOUNTS_ID, managed_account_fields, Version.DEFAULT
            )
            if args.quick_rule_id:
                self.display.v(f"Searching by Quick Rule ID {args.quick_rule_id}")
                managed_accounts = self.class_object.list_by_quick_rule_id(
                    quick_rule_id=args.quick_rule_id
                )
            elif args.quick_rule_title:
                self.display.v(f"Searching by Quick Rule Name {args.quick_rule_title}")
                quick_rule = self.quick_rule_object.list_by_key(
                    "title", args.quick_rule_title
                )

                if not quick_rule:
                    print_it(
                        f"Quick Rule with title {args.quick_rule_title} not found."
                    )
                    return

                managed_accounts = self.class_object.list_by_quick_rule_id(
                    quick_rule_id=quick_rule.get("SmartRuleID")
                )
            else:
                print_it("You must provide either a Quick Rule ID or a Quick Rule Name")
                return
            self.display.show(managed_accounts, fields)
            success_msg = "Managed accounts listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.quick_rule_id:
                print_it(
                    "It was not possible to get a managed account for Quick Rule ID: "
                    f"{args.quick_rule_id}"
                )
            else:
                print_it(
                    "It was not possible to get a managed account for Quick Rule "
                    f"Title: {args.quick_rule_title}"
                )

    @command
    @aliases("create")
    @option(
        "-s",
        "--system-id",
        help="Managed System ID",
        type=int,
        required=True,
    )
    @option(
        "-an",
        "--account-name",
        help="Managed Account Name",
        type=str,
        required=True,
    )
    @option(
        "-p",
        "--password",
        help="Managed Account Password",
        type=str,
        required=False,
    )
    @option(
        "-dn",
        "--domain-name",
        help="Managed Account Domain Name",
        type=str,
        required=False,
    )
    @option(
        "-upn",
        "--user-principal-name",
        help="Managed Account User Principal Name",
        type=str,
        required=False,
    )
    @option(
        "-sam",
        "--sam-account-name",
        help="Managed Account SAM Account Name",
        type=str,
        required=False,
    )
    @option(
        "-dnm",
        "--distinguished-name",
        help="Managed Account Distinguished Name",
        type=str,
        required=False,
    )
    @option(
        "-pk",
        "--private-key",
        help="Managed Account Private Key",
        type=str,
        required=False,
    )
    @option(
        "-pp",
        "--passphrase",
        help="Managed Account Passphrase",
        type=str,
        required=False,
    )
    @option(
        "-pbf",
        "--password-fallback-flag",
        help="Managed Account Password Fallback Flag",
        action="store_true",
    )
    @option(
        "-laf",
        "--login-account-flag",
        help="Managed Account Login Account Flag",
        action="store_true",
    )
    @option(
        "-d",
        "--description",
        help="Managed Account Description",
        type=str,
        required=False,
    )
    @option(
        "-prid",
        "--password-rule-id",
        help="Managed Account Password Rule ID",
        type=int,
        required=False,
    )
    @option(
        "-ae",
        "--api-enabled",
        help="Managed Account API Enabled Flag",
        action="store_true",
    )
    @option(
        "-rne",
        "--release-notification-email",
        help="Managed Account Release Notification Email",
        type=str,
        required=False,
    )
    @option(
        "-csf",
        "--change-services-flag",
        help="Managed Account Change Services Flag",
        action="store_true",
    )
    @option(
        "-rsf",
        "--restart-services-flag",
        help="Managed Account Restart Services Flag",
        action="store_true",
    )
    @option(
        "-ctf",
        "--change-tasks-flag",
        help="Managed Account Change Tasks Flag",
        action="store_true",
    )
    @option(
        "-rd",
        "--release-duration",
        help="Managed Account Release Duration (in minutes)",
        type=int,
        required=False,
    )
    @option(
        "-mrd",
        "--max-release-duration",
        help="Managed Account Max Release Duration (in minutes)",
        type=int,
        required=False,
    )
    @option(
        "-isard",
        "--isa-release-duration",
        help="Managed Account ISA Release Duration (in minutes)",
        type=int,
        required=False,
    )
    @option(
        "-mcr",
        "--max-concurrent-requests",
        help="Managed Account Max Concurrent Requests (0 for unlimited)",
        type=int,
        required=False,
    )
    @option(
        "-amf",
        "--auto-management-flag",
        help="Managed Account Auto Management Flag",
        action="store_true",
    )
    @option(
        "-dsamf",
        "--dss-auto-management-flag",
        help="Managed Account DSS Auto Management Flag",
        action="store_true",
    )
    @option(
        "-cpf",
        "--check-password-flag",
        help="Managed Account Check Password Flag",
        action="store_true",
    )
    @option(
        "-rpf",
        "--reset-password-on-mismatch-flag",
        help="Managed Account Reset Password On Mismatch Flag",
        action="store_true",
    )
    @option(
        "-cpafr",
        "--change-password-after-any-release-flag",
        help="Managed Account Change Password After Any Release Flag",
        action="store_true",
    )
    @option(
        "-cft",
        "--change-frequency-type",
        help="Managed Account Change Frequency Type (first, last, xdays)",
        type=str,
        choices=["first", "last", "xdays"],
        default="first",
        required=False,
    )
    @option(
        "-cfd",
        "--change-frequency-days",
        help=(
            "Managed Account Change Frequency Days (1-999) When ChangeFrequencyType is "
            "xdays, password changes take place this configured number of days."
        ),
        type=int,
        required=False,
    )
    @option(
        "-ct",
        "--change-time",
        help="Managed Account Change Time (24hr format: 00:00-23:59)",
        type=str,
        required=False,
    )
    @option(
        "-ncd",
        "--next-change-date",
        help="Managed Account Next Change Date (YYYY-MM-DD)",
        type=str,
        required=False,
    )
    @option(
        "-uoc",
        "--use-own-credentials",
        help="Managed Account Use Own Credentials Flag",
        action="store_true",
    )
    @option(
        "-ciapf",
        "--change-iis-app-pool-flag",
        help="Managed Account Change IIS App Pool Flag",
        action="store_true",
    )
    @option(
        "-riapf",
        "--restart-iis-app-pool-flag",
        help="Managed Account Restart IIS App Pool Flag",
        action="store_true",
    )
    @option(
        "-wgid",
        "--workgroup-id",
        help="Managed Account Workgroup ID (can be null)",
        type=int,
        required=False,
    )
    @option(
        "-cwal",
        "--change-windows-auto-logon-flag",
        help="Managed Account Change Windows Auto Logon Flag",
        action="store_true",
    )
    @option(
        "-ccpf",
        "--change-com-plus-flag",
        help="Managed Account Change COM+ Flag",
        action="store_true",
    )
    @option(
        "-cdcf",
        "--change-dcom-flag",
        help="Managed Account Change DCOM Flag",
        action="store_true",
    )
    @option(
        "-cscf",
        "--change-scom-flag",
        help="Managed Account Change SCOM Flag",
        action="store_true",
    )
    @option(
        "-oid",
        "--object-id",
        help=(
            "Managed Account Object ID (required when Platform.RequiresObjectID is "
            "true)"
        ),
        type=str,
        required=False,
    )
    def create_managed_account(self, args):
        """
        Create a new managed account with the provided parameters.
        """
        try:
            self.display.v("Creating a new managed account")
            managed_account_obj, _ = self.class_object.create_managed_account(
                system_id=args.system_id,
                account_name=args.account_name,
                password=args.password,
                domain_name=args.domain_name,
                user_principal_name=args.user_principal_name,
                sam_account_name=args.sam_account_name,
                distinguished_name=args.distinguished_name,
                private_key=args.private_key,
                passphrase=args.passphrase,
                password_fallback_flag=args.password_fallback_flag,
                login_account_flag=args.login_account_flag,
                description=args.description,
                password_rule_id=args.password_rule_id,
                api_enabled=args.api_enabled,
                release_notification_email=args.release_notification_email,
                change_services_flag=args.change_services_flag,
                restart_services_flag=args.restart_services_flag,
                change_tasks_flag=args.change_tasks_flag,
                release_duration=args.release_duration,
                max_release_duration=args.max_release_duration,
                isa_release_duration=args.isa_release_duration,
                max_concurrent_requests=args.max_concurrent_requests,
                auto_management_flag=args.auto_management_flag,
                dss_auto_management_flag=args.dss_auto_management_flag,
                check_password_flag=args.check_password_flag,
                reset_password_on_mismatch_flag=args.reset_password_on_mismatch_flag,
                change_password_after_any_release_flag=(
                    args.change_password_after_any_release_flag
                ),
                change_frequency_type=args.change_frequency_type,
                change_frequency_days=args.change_frequency_days,
                change_time=args.change_time,
                next_change_date=args.next_change_date,
                use_own_credentials=args.use_own_credentials,
                change_iis_app_pool_flag=args.change_iis_app_pool_flag,
                restart_iis_app_pool_flag=args.restart_iis_app_pool_flag,
                workgroup_id=args.workgroup_id,
                change_windows_auto_logon_flag=args.change_windows_auto_logon_flag,
                change_com_plus_flag=args.change_com_plus_flag,
                change_dcom_flag=args.change_dcom_flag,
                change_scom_flag=args.change_scom_flag,
                object_id=args.object_id,
            )
            fields = self.get_fields(GET_MANAGED_ACCOUNTS_ID, managed_account_fields)
            self.display.show(managed_account_obj, fields)
            self.display.v("Managed account created successfully")
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to create the managed account. {e}")
        except exceptions.OptionsError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Options error: {e}")

    @command
    @aliases("delete")
    @option(
        "-id",
        "--managed-account-id",
        help="To delete a managed account by ID",
        type=int,
        required=True,
        enforce_uuid=False,
    )
    def delete_managed_account(self, args):
        """
        Deletes a Managed Account by ID.
        """
        try:
            self.display.v(f"Deleting managed account by ID {args.managed_account_id}")
            self.class_object.delete_by_id(
                args.managed_account_id, expected_status_code=200
            )
            success_msg = (
                f"Managed account deleted successfully {args.managed_account_id}"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(
                "It was not possible to delete a managed account for ID: "
                f"{args.managed_account_id}"
            )
            print_it("Does managed account exist and provided ID is valid?")
            self.log.error(e)

    @command
    @aliases("add-attribute")
    @option(
        "-id",
        "--managed-account-id",
        help="Managed account by ID",
        type=int,
        required=True,
    )
    @option(
        "-aid",
        "--attribute-id",
        help="ID of the attribute to assign",
        type=int,
        required=True,
    )
    def assign_attribute(self, args):
        """
        Assigns an attribute to a managed account.
        """
        try:
            self.display.v(
                f"Assigning attribute ID {args.attribute_id} to managed account ID "
                f"{args.managed_account_id}"
            )

            attribute = self.class_object.assign_attribute(
                args.managed_account_id, args.attribute_id
            )
            fields = self.get_fields(
                GET_MANAGED_ACCOUNTS_ID_ATTRIBUTES, managed_account_fields
            )
            self.display.show(attribute, fields)
            success_msg = (
                f"Attribute {args.attribute_id} assigned to managed account "
                f"{args.managed_account_id} successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            print_it(
                f"It was not possible to assign the attribute {args.attribute_id} to "
                f"the managed account ID: {args.managed_account_id}"
            )
            self.log.error(e)

    @command
    @aliases("delete-attribute")
    @option(
        "-id",
        "--managed-account-id",
        help="Managed account by ID",
        type=int,
        required=True,
    )
    @option(
        "-aid",
        "--attribute-id",
        help="ID of the attribute to delete",
        type=int,
        required=True,
    )
    def delete_attribute(self, args):
        """
        Deletes a managed account attribute by managed account ID and attribute ID.
        """
        try:
            self.display.v(
                f"Deleting attribute ID {args.attribute_id} from managed account ID "
                f"{args.managed_account_id}"
            )

            self.class_object.delete_attribute(
                args.managed_account_id, args.attribute_id
            )
            success_msg = (
                f"Attribute {args.attribute_id} deleted from managed account "
                f"{args.managed_account_id} successfully"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(
                f"It was not possible to delete the attribute {args.attribute_id} from "
                f"the managed account ID: {args.managed_account_id}"
            )
            self.log.error(e)

    @command
    @aliases("delete-all-attributes")
    @option(
        "-id",
        "--managed-account-id",
        help="Managed account by ID",
        type=int,
        required=True,
    )
    def delete_all_attributes(self, args):
        """
        Deletes all attributes from a managed account by ID.
        """
        try:
            self.display.v(
                "Deleting all attributes from managed account ID "
                f"{args.managed_account_id}"
            )

            self.class_object.delete_all_attributes(args.managed_account_id)
            success_msg = (
                f"All attributes deleted from managed account {args.managed_account_id}"
                " successfully"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(
                "It was not possible to delete all attributes from the managed "
                f"account ID: {args.managed_account_id}"
            )
            self.log.error(e)

    @command
    @option(
        "-id",
        "--managed-account-id",
        help="Managed account by ID",
        type=int,
        required=True,
    )
    @option(
        "-p",
        "--password",
        help="New password for the managed account",
        type=str,
        required=False,
    )
    @option(
        "-puk",
        "--public-key",
        help="New public key for the managed account",
        type=str,
        required=False,
    )
    @option(
        "-pk",
        "--private-key",
        help="New private key for the managed account",
        type=str,
        required=False,
    )
    @option(
        "-pp",
        "--passphrase",
        help="New passphrase for the managed account",
        type=str,
        required=False,
    )
    @option(
        "-not-upd-sys",
        "--do-not-update-system",
        help="Flag to indicate if the system shouldn't be updated with the new "
        "credentials",
        action="store_false",
        dest="update_system",
        required=False,
    )
    def update_credentials(self, args):
        """
        Updates the credentials of a managed account.
        """
        try:
            self.display.v(
                f"Updating credentials for managed account ID {args.managed_account_id}"
            )
            self.class_object.update_credentials(
                managed_account_id=args.managed_account_id,
                password=args.password,
                public_key=args.public_key,
                private_key=args.private_key,
                passphrase=args.passphrase,
                update_system=args.update_system,
            )
            success_msg = (
                f"Credentials updated successfully for managed account ID "
                f"{args.managed_account_id}"
            )
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.display.v(e)
            print_it(
                f"It was not possible to update credentials for managed account ID: "
                f"{args.managed_account_id}"
            )
            self.log.error(e)

    @command
    @option(
        "passphrase",
        help="The passphrase to use for an encrypted private key.",
        type=str,
        nargs="?",
        default="",
    )
    @option(
        "private_key",
        help="The new private key to set on the host",
        type=str,
        nargs="?",
        default="",
    )
    @option(
        "public_key",
        help="The new public key to set on the host",
        type=str,
        nargs="?",
        default="",
    )
    @option(
        "-not-upd-sys",
        "--do-not-update-system",
        help="Flag to indicate if the system shouldn't be updated with the new "
        "credentials",
        action="store_false",
        dest="update_system",
    )
    @option(
        "password",
        help="New password, use empty quotes to auto-generate a value.",
        type=str,
        nargs="?",
        default="",
    )
    @option(
        "account_name",
        help="Managed account name.",
        type=str,
        nargs="?",
        default=None,
    )
    @option(
        "system_name",
        help="Managed system name.",
        type=str,
        nargs="?",
        default=None,
    )
    def force_reset(self, args):
        """
        Updates a managed account password, public and private key.
        Requires both 'account_name' and 'system_name' parameters to identify
        the account.
        The parameters 'password', 'public_key', 'private_key', and 'passphrase'
        are optional.
        """
        try:
            if not args.account_name or not args.system_name:
                print_it(
                    "You must provide both an account name and a system name to "
                    "proceed."
                )
                return

            self.display.v("Calling force_reset function")
            self.display.v("Searching by account and system's name")
            managed_accounts = self.class_object.get_managed_accounts(
                account_name=args.account_name,
                system_name=args.system_name,
            )

            if isinstance(managed_accounts, dict):
                # If a single account is returned, wrap it in a list
                # to maintain consistency with how multiple accounts are handled
                managed_accounts = [managed_accounts]

            managed_account_list = [
                account
                for account in managed_accounts
                if account.get("AccountName") == args.account_name
            ]

            for managed_account_obj in managed_account_list:
                arg_update = argparse.Namespace(
                    managed_account_id=managed_account_obj.get("AccountId"),
                    password=args.password,
                    public_key=args.public_key,
                    private_key=args.private_key,
                    passphrase=args.passphrase,
                    update_system=args.update_system,
                )
                self.update_credentials(arg_update)
        except Exception as e:
            self.display.v(e)
            self.log.error(f"Short command error: {e}")
            print_it("It was not possible to update managed accounts")
