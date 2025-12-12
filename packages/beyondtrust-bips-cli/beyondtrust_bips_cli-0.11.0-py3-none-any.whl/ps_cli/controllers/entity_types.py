from secrets_safe_library import entity_types, exceptions
from secrets_safe_library.constants.endpoints import GET_ENTITY_TYPES
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.entity_types import fields as entity_type_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command
from ps_cli.core.display import print_it


class EntityType(CLIController):
    """
    Password Safe Entity Types functionality.
    """

    def __init__(self):
        super().__init__(
            name="entity-types",
            help="Entity types management commands",
        )

    @property
    def class_object(self) -> entity_types.EntityType:
        if self._class_object is None and self.app is not None:
            self._class_object = entity_types.EntityType(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_entity_types(self, args):
        """
        Returns a list of entity types.
        """
        try:
            fields = self.get_fields(
                GET_ENTITY_TYPES, entity_type_fields, Version.DEFAULT
            )
            self.display.v("Calling list function")
            entitlements = self.class_object.list()
            self.display.show(entitlements, fields)
            success_msg = "Entity types listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list entity types")
