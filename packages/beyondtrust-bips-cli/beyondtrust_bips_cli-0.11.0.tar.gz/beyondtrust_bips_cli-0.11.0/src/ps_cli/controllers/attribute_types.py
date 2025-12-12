from secrets_safe_library import attribute_types, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_ATTRIBUTE_TYPES,
    GET_ATTRIBUTE_TYPES_ID,
    POST_ATTRIBUTE_TYPES,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.attribute_types import (
    fields as attribute_types_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class AttributeTypes(CLIController):
    """
    List or set Attribute Types for Beyond Insight.
    Requires Beyond Insight Role Management (Read/Write).
    """

    def __init__(self):
        super().__init__(
            name="attribute-types",
            help="Attribute types commands",
        )

    @property
    def class_object(self) -> attribute_types.AttributeType:
        if self._class_object is None and self.app is not None:
            self._class_object = attribute_types.AttributeType(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_attribute_types(self, args):
        """
        Returns a list of Password Safe attribute types.
        """
        try:
            fields = self.get_fields(
                GET_ATTRIBUTE_TYPES, attribute_types_fields, Version.DEFAULT
            )
            self.display.v("Calling list_attribute_types function")
            attribute_types_list = self.class_object.list()
            self.display.show(attribute_types_list, fields)
            success_msg = "Attribute types listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list attribute types")

    @command
    @aliases("get-id")
    @option(
        "-id",
        "--attribute-type-id",
        help="The ID of the attribute type to retrieve",
        type=int,
        required=True,
    )
    def get_attribute_type_by_id(self, args):
        """
        Retrieves a specific attribute type by ID.
        """
        try:
            fields = self.get_fields(
                GET_ATTRIBUTE_TYPES_ID, attribute_types_fields, Version.DEFAULT
            )
            self.display.v("Calling get_attribute_type function")
            attribute_type = self.class_object.get_by_id(args.attribute_type_id)
            self.display.show(attribute_type, fields)
            success_msg = "Attribute type retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the attribute type")

    @command
    @aliases("create")
    @option(
        "-n",
        "--name",
        help="The name of the attribute type to create",
        type=str,
        required=True,
    )
    def create_attribute_type(self, args):
        """
        Creates a new attribute type.
        """
        try:
            fields = self.get_fields(
                POST_ATTRIBUTE_TYPES, attribute_types_fields, Version.DEFAULT
            )
            self.display.v("Calling create_attribute_type function")
            new_attribute_type = self.class_object.create_attribute_type(args.name)
            self.display.show(new_attribute_type, fields)
            success_msg = "Attribute type created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the attribute type")

    @command
    @aliases("delete")
    @option(
        "-id",
        "--attribute-type-id",
        help="The ID of the attribute type to delete",
        type=int,
        required=True,
    )
    def delete_attribute_type_by_id(self, args):
        """
        Deletes a specific attribute type by ID.
        """
        try:
            self.display.v("Calling delete_attribute_type function")
            self.class_object.delete_by_id(
                object_id=args.attribute_type_id, expected_status_code=200
            )
            success_msg = "Attribute type deleted successfully"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to delete the attribute type")
