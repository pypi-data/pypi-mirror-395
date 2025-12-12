from secrets_safe_library import exceptions, keystrokes
from secrets_safe_library.constants.endpoints import (
    GET_KEYSTROKES_ID,
    GET_SESSIONS_SESSIONID_KEYSTROKES,
    POST_KEYSTROKES_SEARCH,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.keystrokes import fields as keystroke_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Keystroke(CLIController):
    """
    Returns a list of Keystrokes, a single keystroke, or search keystrokes.

    Requires Password Safe Auditor or ISA Role on an Asset, or
    member of BeyondInsight Administrators group.
    """

    def __init__(self):
        super().__init__(
            name="keystrokes",
            help="Keystrokes management commands",
        )

    @property
    def class_object(self) -> keystrokes.Keystroke:
        if self._class_object is None and self.app is not None:
            self._class_object = keystrokes.Keystroke(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("by-session")
    @option(
        "-id",
        "--session-id",
        help="Session ID to get keystrokes for",
        type=int,
        required=True,
    )
    def get_keystrokes_by_session(self, args):
        """
        Returns all keystrokes for a specific session ID.
        """
        try:
            fields = self.get_fields(
                GET_SESSIONS_SESSIONID_KEYSTROKES, keystroke_fields, Version.DEFAULT
            )
            self.display.v(
                f"Calling get_keystrokes_by_session_id for session {args.session_id}"
            )
            keystrokes = self.class_object.get_keystrokes_by_session_id(args.session_id)
            self.display.show(keystrokes, fields)
            success_msg = (
                f"Keystrokes for session ID {args.session_id} retrieved successfully"
            )
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.log.error(e)
            print_it(
                f"It was not possible to get keystrokes for session ID: "
                f"{args.session_id}. {e}"
            )

    @command
    @aliases("get")
    @option(
        "-id",
        "--keystroke-id",
        help="Keystroke ID to retrieve",
        type=int,
        required=True,
    )
    def get_keystroke(self, args):
        """
        Returns a keystroke by ID.
        """
        try:
            fields = self.get_fields(
                GET_KEYSTROKES_ID, keystroke_fields, Version.DEFAULT
            )
            self.display.v(f"Searching keystroke by ID {args.keystroke_id}")
            keystroke = self.class_object.get_by_id(args.keystroke_id)
            self.display.show(keystroke, fields)
            success_msg = (
                f"Keystroke with ID {args.keystroke_id} retrieved successfully"
            )
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.log.error(e)
            print_it(
                f"It was not possible to get keystroke for ID: {args.keystroke_id}. {e}"
            )

    @command
    @aliases("search")
    @option(
        "-d",
        "--data",
        help="Keyword(s) for which to search",
        type=str,
        required=True,
    )
    @option(
        "-t",
        "--type",
        help=(
            "Type of keystrokes (0: All, 1: StdIn, 2: StdOut, 4: Window Event, "
            "5: User Event)"
        ),
        type=int,
        default=0,
        choices=[0, 1, 2, 4, 5],
    )
    def search_keystrokes(self, args):
        """
        Searches keystrokes by data and type.
        """
        try:
            fields = self.get_fields(
                POST_KEYSTROKES_SEARCH, keystroke_fields, Version.DEFAULT
            )
            self.display.v(
                f"Searching keystrokes with data: {args.data}, type: {args.type}"
            )
            keystrokes = self.class_object.search_keystrokes(
                data=args.data, type=args.type
            )
            self.display.show(keystrokes, fields)
            success_msg = "Keystrokes search completed successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it(
                "It was not possible to search keystrokes with the provided criteria: "
                f"{e}"
            )
