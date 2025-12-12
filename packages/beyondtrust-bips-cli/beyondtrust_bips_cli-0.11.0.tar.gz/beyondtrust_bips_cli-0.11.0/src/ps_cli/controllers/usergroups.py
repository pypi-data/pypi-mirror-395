import argparse

from secrets_safe_library import exceptions, usergroups
from secrets_safe_library.constants.endpoints import (
    GET_USERGROUPS,
    GET_USERGROUPS_ID,
    GET_USERGROUPS_NAME,
    POST_USERGROUPS_AD,
    POST_USERGROUPS_BI,
    POST_USERGROUPS_ENTRAID,
    POST_USERGROUPS_LDAP,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.usergroups import fields as usergroup_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Usergroups(CLIController):
    """
    Works with Secrets Safe Usergroups - Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="usergroups",
            help="Usergroups management commands",
        )

    @property
    def class_object(self) -> usergroups.Usergroups:
        if self._class_object is None and self.app is not None:
            self._class_object = usergroups.Usergroups(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @option(
        "identifier",
        type=str,
        nargs="?",
        default=None,
        help="To get a Usergroup by ID or Name.",
    )
    def list_groups(self, args):
        """
        If no ID or name is provided, lists all Usergroups.
        If an ID or name is provided, gets the Usergroup using that.
        (Short-command).
        """
        try:
            if args.identifier:
                if args.identifier.isdigit():
                    args_get = argparse.Namespace(
                        usergroup_id=int(args.identifier), usergroup_name=None
                    )
                else:
                    args_get = argparse.Namespace(
                        usergroup_id=None, usergroup_name=args.identifier
                    )
                self.get_usergroup(args_get)
            else:
                args_list = argparse.Namespace()
                self.list_usergroups(args_list)
        except Exception as e:
            self.display.v(e)
            self.log.error(f"Short command error: {e}")
            print_it("It was not possible to get usergroups")

    @command
    @aliases("list")
    def list_usergroups(self, args):
        """
        Returns a list of Usergroups to which the current user has access.
        """
        try:
            fields = self.get_fields(GET_USERGROUPS, usergroup_fields, Version.DEFAULT)
            self.display.v("Calling list_usergroups function")
            usergroups = self.class_object.get_usergroups()
            self.display.show(usergroups, fields)
            success_msg = "Usergroups listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list usergroups")

    @command
    @aliases("get")
    @option(
        "-id",
        "--usergroup-id",
        help="To get a usergroup by ID (GUID)",
        type=int,
        required=False,
    )
    @option(
        "-n",
        "--usergroup-name",
        help="To get a usergroup by name",
        type=str,
        required=False,
    )
    def get_usergroup(self, args):
        """
        Returns a usergroup by ID or name.
        """
        try:
            if args.usergroup_id:
                fields = self.get_fields(
                    GET_USERGROUPS_ID, usergroup_fields, Version.DEFAULT
                )
                self.display.v("Calling get_usergroup_by_id function")
                usergroup = self.class_object.get_usergroup_by_id(args.usergroup_id)
            elif args.usergroup_name:
                fields = self.get_fields(
                    GET_USERGROUPS_NAME, usergroup_fields, Version.DEFAULT
                )
                self.display.v("Calling get_usergroup_by_name function")
                usergroup = self.class_object.get_usergroups_by_name(
                    args.usergroup_name
                )
            else:
                print_it("You must provide either a usergroup ID or name.")
                return
            self.display.show(usergroup, fields)
            success_msg = "Usergroup retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            error_msg = (
                f"by ID: {args.usergroup_id}"
                if args.usergroup_id
                else f"by name: {args.usergroup_name}"
            )
            print_it(f"It was not possible to get usergroup {error_msg}")

    @command
    @aliases("create-usergroup-bi")
    @option(
        "-n",
        "--name",
        help="The Usergroup name",
        type=str,
        required=True,
    )
    @option(
        "-d",
        "--description",
        help="The Usergroup description",
        type=str,
        required=True,
    )
    @option(
        "-non-act",
        "--non-active",
        help="Indicates if the Usergroup should not be active by default.",
        action="store_false",
        dest="is_active",
        required=False,
    )
    @option(
        "-perm",
        "--permissions",
        help="Permissions and access levels to set for the new user group."
        "Format: '{ 'PermissionID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-s-rules",
        "--smart-rule-access",
        help="Smart Rules and access levels to set for the new user group."
        "Format: '{ 'SmartRuleID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-app-r-ids",
        "--application-registration-ids",
        help="IDs representing the API application registrations to grant "
        "the new user group. Format: int ... ",
        type=str,
        required=False,
        nargs="*",
    )
    def create_usergroup_beyond_insight(self, args):
        """
        Creates a new Usergroup with UserType "BeyondInsight".
        """
        try:
            fields = self.get_fields(
                POST_USERGROUPS_BI, usergroup_fields, Version.DEFAULT
            )
            self.display.v("Calling create_usergroup_beyond_insight function")
            usergroup = self.class_object.post_usergroups_beyondinsight(
                group_name=args.name,
                description=args.description,
                is_active=args.is_active,
                permissions=args.permissions,
                smart_rule_access=args.smart_rule_access,
                application_registration_ids=args.application_registration_ids,
            )
            self.display.show(usergroup, fields)
            success_msg = "Usergroup created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the usergroup")
            print_it(f"Error: {e}")

    @command
    @aliases("create-usergroup-entra")
    @option(
        "-d",
        "--description",
        help="The Usergroup description",
        type=str,
        required=True,
    )
    @option(
        "-n",
        "--name",
        help="The Usergroup name",
        type=str,
        required=True,
    )
    @option(
        "-c-id",
        "--client-id",
        help="The client ID",
        type=int,
        required=True,
    )
    @option(
        "-c-secret",
        "--client-secret",
        help="The client secret",
        type=str,
        required=True,
    )
    @option(
        "-t-id",
        "--tenant-id",
        help="The tenant ID",
        type=int,
        required=True,
    )
    @option(
        "-a-i",
        "--azure-instance",
        help="The Azure instance",
        type=str,
        required=False,
    )
    @option(
        "-non-act",
        "--non-active",
        help="Indicates if the Usergroup should not be active by default.",
        action="store_false",
        dest="is_active",
        required=False,
    )
    @option(
        "-perm",
        "--permissions",
        help="Permissions and access levels to set for the new user group."
        "Format: '{ 'PermissionID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-s-rules",
        "--smart-rule-access",
        help="Smart Rules and access levels to set for the new user group."
        "Format: '{ 'SmartRuleID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-app-r-ids",
        "--application-registration-ids",
        help="IDs representing the API application registrations to grant "
        "the new user group. Format: int ... ]",
        type=str,
        required=False,
        nargs="*",
    )
    def create_usergroup_entraid(self, args):
        """
        Creates a new Usergroup with UserType "EntraId".
        """
        try:
            fields = self.get_fields(
                POST_USERGROUPS_ENTRAID, usergroup_fields, Version.DEFAULT
            )
            self.display.v("Calling create_usergroup_entraid function")
            usergroup = self.class_object.post_usergroups_entraid(
                description=args.description,
                group_name=args.name,
                client_id=args.client_id,
                client_secret=args.client_secret,
                tenant_id=args.tenant_id,
                azure_instance=args.azure_instance,
                is_active=args.is_active,
                permissions=args.permissions,
                smart_rule_access=args.smart_rule_access,
                application_registration_ids=args.application_registration_ids,
            )
            self.display.show(usergroup, fields)
            success_msg = "Usergroup created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the usergroup")
            print_it(f"Error: {e}")

    @command
    @aliases("create-usergroup-ad")
    @option(
        "-n",
        "--name",
        help="The Usergroup name",
        type=str,
        required=True,
    )
    @option(
        "-d-na",
        "--domain-name",
        help="The Domain name",
        type=str,
        required=True,
    )
    @option(
        "-d",
        "--description",
        help="The Usergroup description",
        type=str,
        required=True,
    )
    @option(
        "-fo-na",
        "--forest-name",
        help="The Forest name",
        type=str,
        required=False,
    )
    @option(
        "-b-user",
        "--bind-user",
        help="The Bind User name",
        type=str,
        required=False,
    )
    @option(
        "-b-pa",
        "--bind-password",
        help="The Bind Password",
        type=str,
        required=False,
    )
    @option(
        "-ssl",
        "--use-ssl",
        help="Use SSL",
        action="store_true",
        required=False,
    )
    @option(
        "-non-act",
        "--non-active",
        help="Indicates if the Usergroup should not be active by default.",
        action="store_false",
        dest="is_active",
        required=False,
    )
    @option(
        "-e-g-s",
        "--excluded-from-global-sync",
        help="Indicates if the Usergroup is excluded from global sync.",
        action="store_true",
        required=False,
    )
    @option(
        "-o-g-s",
        "--override-global-sync-settings",
        help="Overridden global sync settings.",
        action="store_true",
        required=False,
    )
    @option(
        "-perm",
        "--permissions",
        help="Permissions and access levels to set for the new user group."
        "Format: '{ 'PermissionID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-s-rules",
        "--smart-rule-access",
        help="Smart Rules and access levels to set for the new user group."
        "Format: '{ 'SmartRuleID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-app-r-ids",
        "--application-registration-ids",
        help="IDs representing the API application registrations to grant "
        "the new user group. Format: int ... ",
        type=str,
        required=False,
        nargs="*",
    )
    def create_usergroup_active_directory(self, args):
        """
        Creates a new Usergroup with UserType "ActiveDirectory".
        """
        try:
            fields = self.get_fields(
                POST_USERGROUPS_AD, usergroup_fields, Version.DEFAULT
            )
            self.display.v("Calling create_usergroup_active_directory function")
            usergroup = self.class_object.post_usergroups_ad(
                group_name=args.name,
                domain_name=args.domain_name,
                description=args.description,
                forest_name=args.forest_name,
                bind_user=args.bind_user,
                bind_password=args.bind_password,
                use_ssl=args.use_ssl,
                is_active=args.is_active,
                excluded_from_global_sync=args.excluded_from_global_sync,
                override_global_sync_settings=args.override_global_sync_settings,
                permissions=args.permissions,
                smart_rule_access=args.smart_rule_access,
                application_registration_ids=args.application_registration_ids,
            )
            self.display.show(usergroup, fields)
            success_msg = "Usergroup created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the usergroup")
            print_it(f"Error: {e}")

    @command
    @aliases("create-usergroup-ldap")
    @option(
        "-n",
        "--name",
        help="The Usergroup name",
        type=str,
        required=True,
    )
    @option(
        "-g-d-n",
        "--group-distinguished-name",
        help="The Group distinguished name",
        type=str,
        required=True,
    )
    @option(
        "-h-n",
        "--host-name",
        help="The Host name",
        type=str,
        required=True,
    )
    @option(
        "-m-a",
        "--membership-attribute",
        help="The Membership attribute",
        type=str,
        required=True,
    )
    @option(
        "-a-attr",
        "--account-attribute",
        help="The Account attribute",
        type=str,
        required=True,
    )
    @option(
        "-b-user",
        "--bind-user",
        help="The Bind User name",
        type=str,
        required=False,
    )
    @option(
        "-b-pa",
        "--bind-password",
        help="The Bind Password",
        type=str,
        required=False,
    )
    @option(
        "-p",
        "--port",
        help="The Port number",
        type=int,
        required=False,
    )
    @option(
        "-ssl",
        "--use-ssl",
        help="Use SSL",
        action="store_true",
        required=False,
    )
    @option(
        "-non-act",
        "--non-active",
        help="Indicates if the Usergroup should not be active by default.",
        action="store_false",
        dest="is_active",
        required=False,
    )
    @option(
        "-perm",
        "--permissions",
        help="Permissions and access levels to set for the new user group."
        "Format: '{ 'PermissionID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-s-rules",
        "--smart-rule-access",
        help="Smart Rules and access levels to set for the new user group."
        "Format: '{ 'SmartRuleID': int, 'AccessLevelID': int } ...' ",
        type=str,
        required=False,
        nargs="*",
    )
    @option(
        "-app-r-ids",
        "--application-registration-ids",
        help="IDs representing the API application registrations to grant "
        "the new user group. Format: int ... ",
        type=str,
        required=False,
        nargs="*",
    )
    def create_usergroup_ldap(self, args):
        """
        Creates a new Usergroup with UserType "LDAP".
        """
        try:
            fields = self.get_fields(
                POST_USERGROUPS_LDAP, usergroup_fields, Version.DEFAULT
            )
            self.display.v("Calling create_usergroup_ldap function")
            usergroup = self.class_object.post_usergroups_ldap(
                group_name=args.name,
                group_distinguished_name=args.group_distinguished_name,
                host_name=args.host_name,
                membership_attribute=args.membership_attribute,
                account_attribute=args.account_attribute,
                bind_user=args.bind_user,
                bind_password=args.bind_password,
                port=args.port,
                use_ssl=args.use_ssl,
                is_active=args.is_active,
                permissions=args.permissions,
                smart_rule_access=args.smart_rule_access,
                application_registration_ids=args.application_registration_ids,
            )
            self.display.show(usergroup, fields)
            success_msg = "Usergroup created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the usergroup")
            print_it(f"Error: {e}")

    @command
    @aliases("delete-usergroup")
    @option(
        "-id",
        "--usergroup-id",
        help="The Usergroup ID",
        type=int,
        required=False,
    )
    @option(
        "-n",
        "--name",
        help="The Usergroup name",
        type=str,
        required=False,
    )
    def delete_usergroup(self, args):
        """
        Deletes a Usergroup by ID or name.
        """
        try:
            success_msg = ""
            if args.usergroup_id:
                self.display.v(f"Deleting usergroup by ID {args.usergroup_id}")
                self.class_object.delete_usergroup_by_id(usergroup_id=args.usergroup_id)
                success_msg = (
                    f"Usergroup with ID {args.usergroup_id} deleted successfully."
                )
            elif args.name:
                self.display.v(f"Deleting usergroup with name {args.name}")
                self.class_object.delete_usergroup_by_name(name=args.name)
                success_msg = f"Usergroup with name {args.name} deleted successfully."
            else:
                print_it("You must provide either a usergroup ID or name.")
                return
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            if args.usergroup_id:
                print_it(
                    "It was not possible to delete a usergroup with "
                    f"ID: {args.usergroup_id}"
                )
            elif args.name:
                print_it(
                    f"It was not possible to delete a usergroup with name: {args.name}"
                )
            self.log.error(e)
            print_it(f"Error: {e}")
