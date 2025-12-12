from secrets_safe_library import exceptions, session_locking

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class SessionLocking(CLIController):
    """
    Secrets Safe Session Locking functionality.
    """

    def __init__(self):
        super().__init__(
            name="session-locking",
            help="Session locking management commands",
        )

    @property
    def class_object(self) -> session_locking.SessionLocking:
        if self._class_object is None and self.app is not None:
            self._class_object = session_locking.SessionLocking(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("lock")
    @option(
        "-id",
        "--session-id",
        help="To lock a session by ID",
        type=int,
        required=True,
    )
    def lock_session(self, args):
        """
        Locks a session by ID.
        """
        try:
            self.display.v(f"Locking session with ID {args.session_id}")
            self.class_object.post_session_lock_sessionid(args.session_id)
            success_msg = f"Session {args.session_id} locked successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to lock the session")

    @command
    @aliases("lock-by-managed-account-id")
    @option(
        "-id",
        "--managed-account-id",
        help="To lock a session by managed account ID",
        type=int,
        required=True,
    )
    def lock_session_by_managed_account_id(self, args):
        """
        Locks a session by managed account ID.
        """
        try:
            self.display.v(
                f"Locking session with managed account ID {args.managed_account_id}"
            )
            self.class_object.post_session_lock_managed_account_id(
                args.managed_account_id
            )
            success_msg = (
                f"Session with managed account ID {args.managed_account_id}"
                " locked successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to lock the session")

    @command
    @aliases("lock-by-managed-system-id")
    @option(
        "-id",
        "--managed-system-id",
        help="To lock a session by managed system ID",
        type=int,
        required=True,
    )
    def lock_session_by_managed_system_id(self, args):
        """
        Locks a session by managed system ID.
        """
        try:
            self.display.v(
                f"Locking session with managed system ID {args.managed_system_id}"
            )
            self.class_object.post_session_lock_managed_system_id(
                args.managed_system_id
            )
            success_msg = (
                f"Session with managed system ID {args.managed_system_id} "
                "locked successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to lock the session")
