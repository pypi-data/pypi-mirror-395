from secrets_safe_library import exceptions, operating_systems
from secrets_safe_library.constants.endpoints import GET_OPERATING_SYSTEMS
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.operating_systems import fields as os_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command
from ps_cli.core.display import print_it


class OperatingSystem(CLIController):
    """
    Secret Safe Operating Systems functionality.
    """

    def __init__(self):
        super().__init__(
            name="operating-systems",
            help="Operating Systems commands",
        )

    @property
    def class_object(self) -> operating_systems.OperatingSystem:
        if self._class_object is None and self.app is not None:
            self._class_object = operating_systems.OperatingSystem(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_os(self, args):
        """
        Returns a list of operating systems.
        """
        try:
            fields = self.get_fields(GET_OPERATING_SYSTEMS, os_fields, Version.DEFAULT)
            self.display.v("Calling list function")
            operating_systems_list = self.class_object.list()
            self.display.show(operating_systems_list, fields)
            success_msg = "Operating systems listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list operating systems")
