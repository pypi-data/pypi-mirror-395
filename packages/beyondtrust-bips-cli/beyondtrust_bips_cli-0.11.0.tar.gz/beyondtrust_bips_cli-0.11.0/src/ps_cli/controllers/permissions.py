from secrets_safe_library import exceptions, permissions, usergroups
from secrets_safe_library.constants.endpoints import (
    GET_PERMISSIONS,
    GET_USERGROUP_PERMISSIONS,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.permissions import fields as permission_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Permission(CLIController):
    """
    Beyond Insight Permissions functionality.
    """

    def __init__(self):
        super().__init__(
            name="permissions",
            help="Permissions management commands",
        )

    _usergroup_object: usergroups.Usergroups = None

    @property
    def class_object(self) -> permissions.Permission:
        if self._class_object is None and self.app is not None:
            self._class_object = permissions.Permission(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def usergroup_object(self) -> usergroups.Usergroups:
        if self._usergroup_object is None and self.app is not None:
            self._usergroup_object = usergroups.Usergroups(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._usergroup_object

    @command
    @aliases("list")
    def list_permissions(self, args):
        """
        Returns a list of permissions.
        """
        try:
            fields = self.get_fields(
                GET_PERMISSIONS, permission_fields, Version.DEFAULT
            )
            self.display.v("Calling list_permissions function")
            permissions_list = self.class_object.list()
            self.display.show(permissions_list, fields)
            success_msg = "Permissions listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list permissions")

    def _get_usergroup_by_name(self, name) -> dict:
        """
        Helper function to get usergroup by name.
        """
        try:
            self.display.v(f"Searching for usergroup by name: {name}")
            usergroups_list = self.usergroup_object.get_usergroups_by_name(name=name)
            for usergroup in usergroups_list:
                if usergroup["Name"].lower() == name.lower():
                    return usergroup
            print_it(f"Usergroup '{name}' not found")
            return None

        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the usergroup list")

    @command
    @aliases("get-usergroup-permissions")
    @option(
        "-id",
        "--usergroup-id",
        help="To get permissions for a usergroup by ID (GUID)",
        type=int,
        required=False,
    )
    @option(
        "-name",
        "--usergroup-name",
        help="To get permissions for a usergroup by name",
        type=str,
        required=False,
    )
    def get_usergroup_permissions(self, args):
        """
        Returns a list of permissions for a usergroup by ID or name.
        """
        try:
            fields = self.get_fields(
                GET_USERGROUP_PERMISSIONS, permission_fields, Version.DEFAULT
            )
            if args.usergroup_id:
                # Directly get permissions using usergroup ID
                self.display.v(f"Searching by ID {args.usergroup_id}")
                permissions_list = self.class_object.get_usergroup_permissions(
                    usergroup_id=args.usergroup_id
                )
            elif args.usergroup_name:
                # Search for usergroup by name and then get permissions
                usergroup = self._get_usergroup_by_name(args.usergroup_name)
                if usergroup is None:
                    return

                permissions_list = self.class_object.get_usergroup_permissions(
                    usergroup_id=usergroup["GroupID"]
                )
            else:
                print_it("Please provide either a usergroup ID or name")
                return

            self.display.show(permissions_list, fields)
            success_msg = "Usergroup permissions retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to get permissions for the usergroup")
        except IndexError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the usergroup ID from the list")

    @command
    @aliases("set-ug-permissions")
    @option(
        "-id",
        "--usergroup-id",
        help="To set permissions for a usergroup by ID",
        type=int,
        required=False,
    )
    @option(
        "-name",
        "--usergroup-name",
        help="To set permissions for a usergroup by name",
        type=str,
        required=False,
    )
    @option(
        "-perm",
        "--permissions",
        help="""Permissions and access levels to set for the new user group."
        "{ 'PermissionID': int, 'AccessLevelID': int }" "..." """,
        type=str,
        required=True,
        nargs="+",
    )
    def set_usergroup_permissions(self, args):
        """
        Sets permissions for the user group referenced by ID or name.
        The permissions should be provided in the format:
        "{ 'PermissionID': int, 'AccessLevelID': int }" "..."
        """
        try:
            if not args.usergroup_id and not args.usergroup_name:
                print_it("Please provide either a usergroup ID or name")
                return

            if args.usergroup_name:
                usergroup = self._get_usergroup_by_name(args.usergroup_name)
                if usergroup is None:
                    return
                usergroup_id = usergroup["GroupID"]
            else:
                usergroup_id = args.usergroup_id

            self.display.v(f"Permissions to set: {args.permissions}")
            self.display.v(f"Setting permissions for user group ID {usergroup_id}")

            response_code = self.class_object.set_usergroup_permissions(
                usergroup_id=usergroup_id, permissions=args.permissions
            )
            self.display.v(f"Response code: {response_code}")

            if args.usergroup_name:
                success_msg = (
                    "Permissions set successfully for the user group "
                    f"'{args.usergroup_name}'"
                )
                self.display.v(success_msg)
            else:
                success_msg = (
                    f"Permissions set successfully for the user group ID {usergroup_id}"
                )
                self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it(
                f"It was not possible to set the permissions for the usergroup: {e}"
            )

    @command
    @aliases("delete-ug-permissions")
    @option(
        "-id",
        "--usergroup-id",
        help="To delete permissions for a usergroup by ID",
        type=int,
        required=False,
    )
    @option(
        "-name",
        "--usergroup-name",
        help="To delete permissions for a usergroup by name",
        type=str,
        required=False,
    )
    def delete_usergroup_permissions(self, args):
        """
        Deletes all permissions for the user group referenced by ID or name.
        """
        try:
            if not args.usergroup_id and not args.usergroup_name:
                print_it("Please provide either a usergroup ID or name")
                return

            if args.usergroup_name:
                self.display.v(
                    f"Searching for user group by name: {args.usergroup_name}"
                )
                usergroup = self._get_usergroup_by_name(args.usergroup_name)
                if usergroup is None:
                    return
                usergroup_id = usergroup["GroupID"]
            else:
                usergroup_id = args.usergroup_id

            self.display.v(f"Deleting permissions for user group ID {usergroup_id}")
            self.class_object.delete_usergroup_permissions(usergroup_id=usergroup_id)
            success_msg = "Permissions deleted successfully for the user group"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to delete the permissions for the user group")
