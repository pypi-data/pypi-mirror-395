from secrets_safe_library import exceptions, sessions
from secrets_safe_library.constants.endpoints import (
    GET_SESSIONS,
    GET_SESSIONS_ID,
    POST_SESSIONS_REQUEST_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.sessions import fields as session_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Session(CLIController):
    """
    Secrets Safe Sessions functionality.
    """

    def __init__(self):
        super().__init__(
            name="sessions",
            help="Sessions management commands",
        )

    @property
    def class_object(self) -> sessions.Session:
        if self._class_object is None and self.app is not None:
            self._class_object = sessions.Session(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_sessions(self, args):
        """
        Returns a list of sessions to which the current user has access.
        """
        try:
            fields = self.get_fields(GET_SESSIONS, session_fields, Version.DEFAULT)
            self.display.v("Calling list_sessions function")
            sessions = self.class_object.get_sessions()
            self.display.show(sessions, fields)
            success_msg = "Sessions listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it("It was not possible to list sessions")

    @command
    @aliases("get")
    @option(
        "-id",
        "--session-id",
        help="To get a session by ID",
        type=int,
        required=True,
    )
    def get_session_by_id(self, args):
        """
        Returns a session by ID.
        """
        try:
            fields = self.get_fields(GET_SESSIONS_ID, session_fields, Version.DEFAULT)
            self.display.v(f"Searching by ID {args.session_id}")
            session = self.class_object.get_by_id(args.session_id)
            self.display.show(session, fields)
            success_msg = "Session retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it(f"It was not possible to get a session for ID: {args.session_id}")

    @command
    @aliases("create")
    @option(
        "-r-id",
        "--request-id",
        help="The ID of the session request",
        type=int,
        required=True,
    )
    @option(
        "-type",
        "--session-type",
        help="The type of the session",
        type=str,
        required=True,
    )
    @option(
        "-n",
        "--node-id",
        help="The ID of the node",
        type=int,
        required=False,
    )
    def create_session(self, args):
        """
        Creates a new session.
        """
        try:
            fields = self.get_fields(
                POST_SESSIONS_REQUEST_ID, session_fields, Version.DEFAULT
            )
            self.display.v(f"Creating session with request ID {args.request_id}")
            session = self.class_object.post_sessions_request_id(
                request_id=args.request_id,
                session_type=args.session_type,
                node_id=args.node_id,
            )
            self.display.show(session, fields)
            self.display.v("Session created successfully")
        except exceptions.CreationError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it("It was not possible to create the session")

    @command
    @aliases("admin-session")
    @option(
        "-type",
        "--session-type",
        help="The type of the session",
        type=str,
        required=True,
        choices=["SSH", "sshticket", "RDP", "rdpticket", "rdpfile"],
    )
    @option(
        "-h-n",
        "--host-name",
        help="The host name",
        type=str,
        required=True,
    )
    @option(
        "-u-n",
        "--user-name",
        help="The user name",
        type=str,
        required=True,
    )
    @option(
        "-psw",
        "--password",
        help="The password",
        type=str,
        required=True,
    )
    @option(
        "-p",
        "--port",
        help="The port",
        type=int,
        required=False,
    )
    @option(
        "-d-n",
        "--domain-name",
        help="The domain name",
        type=str,
        required=False,
    )
    @option(
        "-r",
        "--reason",
        help="The reason for the session request",
        type=str,
        required=False,
    )
    @option(
        "-re",
        "--resolution",
        help="The resolution for the session request",
        type=str,
        required=False,
    )
    @option(
        "-r-a-s",
        "--rdp-admin-switch",
        help="Whether to use RDP admin switch",
        action="store_true",
        required=False,
    )
    @option(
        "-s-si",
        "--smart-sizing",
        help="Whether to use smart sizing",
        action="store_true",
        required=False,
    )
    @option(
        "-n",
        "--node-id",
        help="The ID of the node",
        type=int,
        required=False,
    )
    @option(
        "-rec-off",
        "--record-off",
        help="if present the session will not be recorded",
        action="store_false",
        required=False,
        dest="record",
    )
    def create_session_admin(self, args):
        """
        Create a new admin session.
        """
        try:
            self.display.v("Creating admin session")
            session = self.class_object.post_sessions_admin(
                session_type=args.session_type,
                host_name=args.host_name,
                user_name=args.user_name,
                password=args.password,
                port=args.port,
                domain_name=args.domain_name,
                reason=args.reason,
                resolution=args.resolution,
                rdp_admin_switch=args.rdp_admin_switch,
                smart_sizing=args.smart_sizing,
                node_id=args.node_id,
                record=args.record,
            )
            self.display.show(session)
            self.display.v("Admin session created successfully")
        except exceptions.CreationError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it("It was not possible to create the admin session")
