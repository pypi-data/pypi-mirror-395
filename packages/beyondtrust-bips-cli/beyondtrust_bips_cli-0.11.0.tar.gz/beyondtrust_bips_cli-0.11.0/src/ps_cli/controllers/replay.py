from secrets_safe_library import exceptions, replay

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Replay(CLIController):
    """
    Password Safe Replay functionality.
    """

    def __init__(self):
        super().__init__(
            name="replay",
            help="Replay sessions management commands",
        )

    @property
    def class_object(self) -> replay.Replay:
        if self._class_object is None and self.app is not None:
            self._class_object = replay.Replay(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("create-session")
    @option(
        "-id",
        "--session-id",
        help="Session ID to create replay for",
        type=str,
        required=True,
    )
    @option(
        "-k",
        "--record-key",
        help="Record key for the replay session",
        type=str,
        required=True,
    )
    @option(
        "-p",
        "--protocol",
        help=(
            "Protocol for the replay session. When session Type is 0 this should be "
            "RDP or for type 1 SSH"
        ),
        type=str,
        required=True,
        choices=["RDP", "SSH"],
    )
    @option(
        "-hl",
        "--headless",
        help="Whether to run in headless mode",
        action="store_true",
    )
    def create_replay_session(self, args):
        """
        Creates a new replay session.
        """
        try:
            self.display.v(f"Creating replay session for session ID {args.session_id}")
            replay_session = self.class_object.create_replay_session(
                session_id=args.session_id,
                record_key=args.record_key,
                protocol=args.protocol,
                headless=args.headless,
            )
            self.display.show(replay_session)
            self.display.v("Replay session created successfully")
        except exceptions.CreationError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it("It was not possible to create the replay session")

    @command
    @aliases("get-session")
    @option(
        "-id",
        "--replay-id",
        help="Replay ID to get session for",
        type=str,
        required=True,
    )
    @option(
        "-js",
        "--jpeg-scale",
        help="JPEG scale for the replay session",
        type=str,
    )
    @option(
        "-ps",
        "--png-scale",
        help="PNG scale for the replay session",
        type=str,
    )
    @option(
        "-s",
        "--screen",
        help="Whether to include screen in the replay",
        action="store_true",
    )
    def get_replay_session(self, args):
        """
        Gets a replay session by ID.
        """
        try:
            self.display.v(f"Getting replay session for ID {args.replay_id}")
            replay_session = self.class_object.get_replay_session(
                replay_id=args.replay_id,
                jpeg_scale=args.jpeg_scale,
                png_scale=args.png_scale,
                screen=args.screen,
            )
            self.display.show(replay_session)
            self.display.v("Replay session retrieved successfully")
        except exceptions.LookupError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it(
                f"It was not possible to get replay session for ID: {args.replay_id}"
            )

    @command
    @aliases("control-session")
    @option(
        "-id",
        "--replay-id",
        help="Replay ID to control",
        type=str,
        required=True,
    )
    @option(
        "-sp",
        "--speed",
        help="Speed for the replay session control",
        type=int,
    )
    @option(
        "-o",
        "--offset",
        help="Offset for the replay session control",
        type=int,
    )
    @option(
        "-nf",
        "--next-frame",
        help="Next frame for the replay session control",
        type=int,
    )
    def control_replay_session(self, args):
        """
        Controls a replay session by ID.
        """
        try:
            self.display.v(f"Controlling replay session for ID {args.replay_id}")
            replay_control = self.class_object.control_replay_session(
                replay_id=args.replay_id,
                speed=args.speed,
                offset=args.offset,
                next_frame=args.next_frame,
            )
            self.display.show(replay_control)
            self.display.v("Replay session controlled successfully")
        except exceptions.UpdateError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it(
                f"It was not possible to control replay session for ID: "
                f"{args.replay_id}"
            )

    @command
    @aliases("delete", "terminate")
    @option(
        "-id",
        "--replay-id",
        help="ID of the replay session to delete",
        type=str,
        required=True,
    )
    def delete_replay(self, args):
        """
        Terminates the replay session.
        """
        try:
            self.display.v(f"Deleting replay session by ID {args.replay_id}")
            self.class_object.delete_by_id(args.replay_id, expected_status_code=200)
            self.display.v(f"Replay session deleted successfully: {args.replay_id}")
        except exceptions.DeletionError as e:
            self.display.v(e, save_log=False)
            self.log.error(e)
            print_it(f"It was not possible to delete replay for ID: {args.replay_id}")
            print_it("Does replay exist and provided ID is valid?")
