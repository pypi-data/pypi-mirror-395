from secrets_safe_library import exceptions, platforms
from secrets_safe_library.constants.endpoints import GET_PLATFORMS
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.platforms import fields as platform_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Platform(CLIController):
    """
    Password Safe Platforms functionality.
    """

    def __init__(self):
        super().__init__(
            name="platforms",
            help="Platforms management commands",
        )

    @property
    def class_object(self) -> platforms.Platform:
        if self._class_object is None and self.app is not None:
            self._class_object = platforms.Platform(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_platforms(self, args):
        """
        Returns a list of platforms for managed systems.
        """
        try:
            fields = self.get_fields(GET_PLATFORMS, platform_fields, Version.DEFAULT)
            self.display.v("Calling list_platforms function")
            platforms_list = self.class_object.list()
            self.display.show(platforms_list, fields)
            success_msg = "Platforms listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list platforms")

    @command
    @aliases("list-by-entity-type", "list-by-et")
    @option(
        "-id",
        "--entity-type-id",
        help="The ID of the entity type to filter platforms",
        type=int,
        required=True,
    )
    def list_platforms_by_entity_type(self, args):
        """
        Lists the platforms by entity type ID.
        """
        try:
            fields = self.get_fields(GET_PLATFORMS, platform_fields, Version.DEFAULT)
            self.display.v("Calling list_platforms_by_entity_type function")
            platforms_list = self.class_object.list_by_entity_type(
                entity_type_id=args.entity_type_id
            )
            self.display.show(platforms_list, fields)
            success_msg = "Platforms listed successfully by entity type"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list platforms by entity type")

    @command
    @aliases("get")
    @option(
        "-id",
        "--platform-id",
        help="The ID of the platform to retrieve",
        type=int,
        required=True,
    )
    def get_platform(self, args):
        """
        Returns a platform by ID.
        """
        try:
            fields = self.get_fields(GET_PLATFORMS, platform_fields, Version.DEFAULT)
            self.display.v("Calling get_by_id function")
            platform = self.class_object.get_by_id(args.platform_id)
            self.display.show(platform, fields)
            success_msg = f"Platform with ID {args.platform_id} retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the platform")
