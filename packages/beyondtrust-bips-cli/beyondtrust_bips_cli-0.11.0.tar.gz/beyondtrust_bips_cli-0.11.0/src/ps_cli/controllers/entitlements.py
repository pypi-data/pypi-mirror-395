from secrets_safe_library import entitlements, exceptions
from secrets_safe_library.constants.endpoints import GET_ENTITLEMENTS
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.entitlements import fields as entitlement_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Entitlement(CLIController):
    """
    BeyondInsight Entitlements functionality.
    """

    def __init__(self):
        super().__init__(
            name="entitlements",
            help="Entitlements management commands",
        )

    @property
    def class_object(self) -> entitlements.Entitlement:
        if self._class_object is None and self.app is not None:
            self._class_object = entitlements.Entitlement(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    @option(
        "-g",
        "--group-ids",
        help="List of group IDs to filter the entitlements",
        type=int,
        required=False,
        nargs="*",  # Allows multiple IDs
    )
    def list_entitlements(self, args):
        """
        Returns user entitlements. If required, you can specify group IDs to filter the
        results.
        """
        try:
            fields = self.get_fields(
                GET_ENTITLEMENTS, entitlement_fields, Version.DEFAULT
            )
            self.display.v("Calling list_entitlements function")
            entitlements = self.class_object.list_entitlements(group_ids=args.group_ids)
            self.display.show(entitlements, fields)
            success_msg = "Entitlements listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list entitlements")
