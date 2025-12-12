from secrets_safe_library import exceptions, session_termination

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class SessionTermination(CLIController):
    """
    Secrets Safe Session Termination functionality.
    """

    def __init__(self):
        super().__init__(
            name="session-termination",
            help="Session termination management commands",
        )

    @property
    def class_object(self) -> session_termination.SessionTermination:
        if self._class_object is None and self.app is not None:
            self._class_object = session_termination.SessionTermination(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("terminate")
    @option(
        "-id",
        "--session-id",
        help="To terminate a session by ID",
        type=int,
        required=True,
    )
    def terminate_session(self, args):
        """
        Terminates a session by ID.
        """
        try:
            self.display.v(f"Terminating session with ID {args.session_id}")
            self.class_object.post_session_terminate_sessionid(args.session_id)
            success_msg = f"Session {args.session_id} terminated successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to terminate the session")

    @command
    @aliases("terminate-by-managed-account-id")
    @option(
        "-id",
        "--managed-account-id",
        help="To terminate a session by managed account ID",
        type=int,
        required=True,
    )
    def terminate_session_by_managed_account_id(self, args):
        """
        Terminates a session by managed account ID.
        """
        try:
            self.display.v(
                f"Terminating session for managed account ID {args.managed_account_id}"
            )
            self.class_object.post_session_terminate_managedaccountid(
                args.managed_account_id
            )
            success_msg = (
                f"Session for managed account ID {args.managed_account_id} "
                "terminated successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to terminate the session for the "
                "managed account ID"
            )

    @command
    @aliases("terminate-by-managed-system-id")
    @option(
        "-id",
        "--managed-system-id",
        help="To terminate a session by managed system ID",
        type=int,
        required=True,
    )
    def terminate_session_by_managed_system_id(self, args):
        """
        Terminates a session by managed system ID.
        """
        try:
            self.display.v(
                f"Terminating session for managed system ID {args.managed_system_id}"
            )
            self.class_object.post_session_terminate_managedsystemid(
                args.managed_system_id
            )
            success_msg = (
                f"Session for managed system ID {args.managed_system_id} "
                "terminated successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to terminate the session for the managed system ID"
            )
