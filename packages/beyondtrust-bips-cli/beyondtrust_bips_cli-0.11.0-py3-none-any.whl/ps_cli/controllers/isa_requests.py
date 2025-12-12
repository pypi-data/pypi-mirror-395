from secrets_safe_library import exceptions, isa_requests

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class ISARequest(CLIController):
    """
    Password Safe ISA Requests functionality.
    """

    def __init__(self):
        super().__init__(
            name="isa-requests",
            help="ISA Requests management commands",
        )

    @property
    def class_object(self) -> isa_requests.ISARequest:
        if self._class_object is None and self.app is not None:
            self._class_object = isa_requests.ISARequest(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("create")
    @option(
        "-s",
        "--system-id",
        help="The ID of the system for which the ISA request is being created",
        type=int,
        required=True,
    )
    @option(
        "-a",
        "--account-id",
        help="The ID of the account for which the ISA request is being created",
        type=int,
        required=True,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="The duration of the ISA request in minutes",
        type=int,
        required=False,
    )
    @option(
        "-r",
        "--reason",
        help="The reason for the ISA request",
        type=str,
        required=False,
    )
    @option(
        "-t",
        "--type",
        help="the type of credentials to retrieve. "
        "Options are 'password', 'dsskey', 'passphrase'. Default is 'password'",
        type=str,
        required=False,
        choices=["password", "dsskey", "passphrase"],
        default="password",
    )
    def create_isa_request(self, args):
        """
        Creates a new Information Systems Administrator (ISA) release request and
        returns the requested credentials.
        """
        try:
            self.display.v("Calling create_isa_request function")
            isa_request = self.class_object.create_isa_request(
                system_id=args.system_id,
                account_id=args.account_id,
                duration_minutes=args.duration_minutes,
                reason=args.reason,
                type=args.type,
            )
            self.display.show(isa_request)
            success_msg = "ISA request created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the ISA request")
