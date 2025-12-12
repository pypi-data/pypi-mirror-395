from secrets_safe_library import access_levels, exceptions
from secrets_safe_library.constants.endpoints import GET_ACCESS_LEVELS
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.access_levels import fields as access_level_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class AccessLevels(CLIController):
    """
    List or set Access Levels for Beyond Insight.
    Requires Beyond Insight Role Management (Read).
    """

    def __init__(self):
        super().__init__(
            name="access-levels",
            help="Access levels commands",
        )

    @property
    def class_object(self) -> access_levels.AccessLevels:
        if self._class_object is None and self.app is not None:
            self._class_object = access_levels.AccessLevels(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_access_levels(self, args):
        """
        Returns a list of Password Safe access levels.
        """
        try:
            fields = self.get_fields(
                GET_ACCESS_LEVELS, access_level_fields, Version.DEFAULT
            )
            self.display.v("Calling list_access_levels function")
            access_levels = self.class_object.get_access_levels()
            self.display.show(access_levels, fields)
            success_msg = "Access levels listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list access levels")

    @command
    @aliases("set")
    @option(
        "-u-g-id",
        "--user-group-id",
        help="The user group ID to set the access level for",
        type=int,
        required=True,
    )
    @option(
        "-s-r-id",
        "--smart-rule-id",
        help="The smart rule ID to set the access level for",
        type=int,
        required=True,
    )
    @option(
        "-a-l-id",
        "--access-level-id",
        help="The access level ID to set",
        type=int,
        required=True,
    )
    def set_access_level(self, args):
        """
        Sets an access level for a usergroup and smart rule.
        """
        try:
            self.display.v("Calling set_access_level function")
            self.class_object.post_access_levels_usergroupid_smartruleid(
                usergroupid=args.user_group_id,
                smartruleid=args.smart_rule_id,
                accesslevelid=args.access_level_id,
            )
            success_msg = "Access level set successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to set the access level")
