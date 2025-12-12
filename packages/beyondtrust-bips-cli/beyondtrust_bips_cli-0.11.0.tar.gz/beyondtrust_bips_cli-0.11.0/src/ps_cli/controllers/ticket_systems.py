from secrets_safe_library import exceptions, ticket_systems
from secrets_safe_library.constants.endpoints import GET_TICKET_SYSTEMS
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.ticket_systems import fields as ticket_systems_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command
from ps_cli.core.display import print_it


class TicketSystems(CLIController):
    """
    Secret Safe Ticket Systems functionality.
    """

    def __init__(self):
        super().__init__(
            name="ticket-systems",
            help="Ticket Systems management commands",
        )

    @property
    def class_object(self) -> ticket_systems.TicketSystems:
        if self._class_object is None and self.app is not None:
            self._class_object = ticket_systems.TicketSystems(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_ticket_systems(self, args):
        """
        List registered ticket systems.
        """
        try:
            fields = self.get_fields(
                GET_TICKET_SYSTEMS, ticket_systems_fields, Version.DEFAULT
            )
            self.display.v("Calling list function")
            ticket_systems = self.class_object.list()
            self.display.show(ticket_systems, fields)
            success_msg = "Ticket systems listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list ticket systems")
