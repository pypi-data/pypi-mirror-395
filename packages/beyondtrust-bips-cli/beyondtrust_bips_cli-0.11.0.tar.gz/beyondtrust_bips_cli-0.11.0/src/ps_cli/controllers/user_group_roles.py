from secrets_safe_library import exceptions, user_group_roles
from secrets_safe_library.constants.endpoints import GET_USERGROUPS_ID_SMARTRULES_ROLES
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.user_group_roles import fields as roles_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class UserGroupRoles(CLIController):
    """
    Secret Safe User Group Roles functionality.
    """

    def __init__(self):
        super().__init__(
            name="user-group-roles",
            help="User Group Roles management commands",
        )

    @property
    def class_object(self) -> user_group_roles.UserGroupRoles:
        if self._class_object is None and self.app is not None:
            self._class_object = user_group_roles.UserGroupRoles(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("get")
    @option(
        "-ug",
        "--user-group-id",
        help="User Group ID",
        type=int,
        required=True,
    )
    @option(
        "-sr",
        "--smart-rule-id",
        help="Smart Rule ID",
        type=int,
        required=True,
    )
    def get_roles(self, args):
        """
        Returns a list of roles for the user group and Smart Rule referenced by ID.
        """
        try:
            fields = self.get_fields(
                GET_USERGROUPS_ID_SMARTRULES_ROLES, roles_fields, Version.DEFAULT
            )
            self.display.v(
                f"Getting roles for user group {args.user_group_id} "
                f"and smart rule {args.smart_rule_id}"
            )
            roles = self.class_object.get_roles(
                user_group_id=args.user_group_id, smart_rule_id=args.smart_rule_id
            )
            self.display.show(roles, fields)
            success_msg = "Roles retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get roles for user group "
                f"{args.user_group_id} and smart rule {args.smart_rule_id}"
            )

    @command
    @aliases("set")
    @option(
        "-ug",
        "--user-group-id",
        help="User Group ID",
        type=int,
        required=True,
    )
    @option(
        "-sr",
        "--smart-rule-id",
        help="Smart Rule ID",
        type=int,
        required=True,
    )
    @option("-r", "--roles", help="Role IDs", type=int, nargs="*")
    @option(
        "-ap",
        "--access-policy-id",
        help="Access Policy ID",
        type=int,
        required=False,
    )
    def set_roles(self, args):
        """
        Sets Password Safe roles for the user group and Smart Rule referenced by ID.

        Valid Roles by Smart Rule Type:

        > Asset Smart Rules:
        4 - Information Security Administrator (ISA)
        5 - Auditor

        > Managed Account Smart Rules:
        1 - Requestor (requires AccessPolicyID)
        2 - Approver
        3 - Requestor & Approver (requires AccessPolicyID)
        7 - Credentials Manager
        8 - Recorded Session Reviewer
        9 - Active Session Reviewer

        Note: For Managed Account Smart Rules, only one of Requestor (1), Approver (2),
        or Requestor & Approver (3) can be assigned per user group/smart rule
        combination.
        """
        try:
            self.display.v(
                f"Setting roles for user group {args.user_group_id} "
                f"and smart rule {args.smart_rule_id}"
            )
            self.class_object.set_roles(
                user_group_id=args.user_group_id,
                smart_rule_id=args.smart_rule_id,
                roles=args.roles,
                access_policy_id=args.access_policy_id,
            )
            success_msg = "Roles set successfully"
            print_it(success_msg)
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to set roles for user group "
                f"{args.user_group_id} and smart rule {args.smart_rule_id}"
            )

    @command
    @aliases("delete")
    @option(
        "-ug",
        "--user-group-id",
        help="User Group ID",
        type=int,
        required=True,
    )
    @option(
        "-sr",
        "--smart-rule-id",
        help="Smart Rule ID",
        type=int,
        required=True,
    )
    def delete_roles(self, args):
        """
        Deletes all Password Safe roles for the user group and Smart Rule referenced by
        ID.
        """
        try:
            self.display.v(
                f"Deleting roles for user group {args.user_group_id} "
                f"and smart rule {args.smart_rule_id}"
            )
            self.class_object.delete_roles(
                user_group_id=args.user_group_id, smart_rule_id=args.smart_rule_id
            )
            success_msg = "Roles deleted successfully"
            print_it(success_msg)
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete roles for user group "
                f"{args.user_group_id} and smart rule {args.smart_rule_id}"
            )
