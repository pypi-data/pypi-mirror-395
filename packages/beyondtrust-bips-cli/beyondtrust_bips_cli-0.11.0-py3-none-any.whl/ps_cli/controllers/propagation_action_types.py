from secrets_safe_library import exceptions, propagation_action_types
from secrets_safe_library.constants.endpoints import GET_PROPAGATION_ACTION_TYPES
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.propagation_action_types import (
    fields as propagation_action_types_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command
from ps_cli.core.display import print_it


class PropagationActionTypes(CLIController):
    """
    Controller for managing Propagation Action Types.

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self) -> None:
        super().__init__(
            name="propagation-action-types",
            help="Propagation Action Types management commands",
        )

    @property
    def class_object(self) -> propagation_action_types.PropagationActionTypes:
        if self._class_object is None and self.app is not None:
            self._class_object = propagation_action_types.PropagationActionTypes(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_propagation_action_types(self, args):
        """
        Lists all Propagation Action Types.
        """
        try:
            fields = self.get_fields(
                GET_PROPAGATION_ACTION_TYPES,
                propagation_action_types_fields,
                Version.DEFAULT,
            )
            self.display.v("Calling list_propagation_action_types function")
            action_types = self.class_object.list()
            self.display.show(action_types, fields)
            success_msg = "Propagation Action Types listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list Propagation Action Types")
