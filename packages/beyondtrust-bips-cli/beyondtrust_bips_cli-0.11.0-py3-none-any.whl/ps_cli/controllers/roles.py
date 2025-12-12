from secrets_safe_library import exceptions, roles
from secrets_safe_library.constants.endpoints import GET_ROLES
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.roles import fields as roles_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command
from ps_cli.core.display import print_it


class Roles(CLIController):
    """
    Password Safe Roles functionality.
    """

    def __init__(self):
        super().__init__(
            name="roles",
            help="Roles commands",
        )

    @property
    def class_object(self) -> roles.Roles:
        if self._class_object is None and self.app is not None:
            self._class_object = roles.Roles(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_roles(self, args):
        """
        List available roles.
        """
        try:
            fields = self.get_fields(GET_ROLES, roles_fields, Version.DEFAULT)
            self.display.v("Calling list function")
            roles = self.class_object.list()
            self.display.show(roles, fields)
            success_msg = "Roles listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list roles")
