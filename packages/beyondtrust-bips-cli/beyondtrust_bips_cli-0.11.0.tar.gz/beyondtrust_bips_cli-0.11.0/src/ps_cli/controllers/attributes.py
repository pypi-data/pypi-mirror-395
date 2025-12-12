from secrets_safe_library import attributes, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_ATTRIBUTE_ID,
    GET_ATTRIBUTES_ATTRIBUTE_TYPE_ID,
    GET_ATTRIBUTES_MANAGED_ACCOUNT_ID,
    GET_ATTRIBUTES_MANAGED_SYSTEM_ID,
    POST_ATTRIBUTE_ATTRIBUTE_TYPE_ID,
    POST_ATTRIBUTE_MANAGED_ACCOUNT_ID,
    POST_ATTRIBUTE_MANAGED_SYSTEM_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.attributes import fields as attribute_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Attributes(CLIController):
    """
    List, create, set and delete Attributes for Beyond Insight.
    Requires BeyondInsight/Password Safe Role Management (Read/Write).
    """

    def __init__(self):
        super().__init__(name="attributes", help="Manage attributes")

    @property
    def class_object(self) -> attributes.Attributes:
        if self._class_object is None and self.app is not None:
            self._class_object = attributes.Attributes(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("get-by-id")
    @option(
        "-id", "--attribute-id", type=int, help="ID of the attribute", required=True
    )
    def get_attribute_by_id(self, args):
        """
        Retrieves a specific attribute by ID.
        """
        try:
            fields = self.get_fields(
                GET_ATTRIBUTE_ID, attribute_fields, Version.DEFAULT
            )
            self.display.v("Calling get_attribute_by_id function")
            attribute = self.class_object.get_by_id(args.attribute_id)
            self.display.show(attribute, fields)
            success_msg = "Attribute retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the attribute")

    @command
    @aliases("get-by-type-id")
    @option(
        "-id-a-t",
        "--attribute-type-id",
        help="ID of the attribute type",
        type=int,
        required=True,
    )
    def get_attributes_by_type_id(self, args):
        """
        Retrieves all attributes for a specific attribute type ID.
        """
        try:
            fields = self.get_fields(
                GET_ATTRIBUTES_ATTRIBUTE_TYPE_ID, attribute_fields, Version.DEFAULT
            )
            self.display.v("Calling get_attributes_by_type_id function")
            attributes = self.class_object.get_attributes_by_attribute_type_id(
                attribute_type_id=args.attribute_type_id
            )
            self.display.show(attributes, fields)
            success_msg = "Attributes retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the attributes")

    @command
    @aliases("create-by-type-id")
    @option(
        "-id-a-t",
        "--attribute-type-id",
        type=int,
        help="ID of the attribute type",
        required=True,
    )
    @option(
        "-s-n",
        "--short-name",
        type=str,
        help="Short name of the attribute",
        required=True,
    )
    @option(
        "-l-n",
        "--long-name",
        type=str,
        help="Long name of the attribute",
        required=True,
    )
    @option(
        "-d",
        "--description",
        type=str,
        help="Description of the attribute",
        required=False,
    )
    @option(
        "-p-a-id",
        "--parent-attribute-id",
        type=int,
        help="ID of the parent attribute",
        required=False,
    )
    @option(
        "-v-i",
        "--value-int",
        type=int,
        help="Integer value of the attribute",
        required=False,
    )
    def post_attribute_by_type_id(self, args):
        """
        Creates a new attribute for a specific attribute type ID.
        """
        try:
            fields = self.get_fields(
                POST_ATTRIBUTE_ATTRIBUTE_TYPE_ID, attribute_fields, Version.DEFAULT
            )
            self.display.v("Calling post_attribute_by_type_id function")
            attribute = self.class_object.post_attribute_by_attribute_type_id(
                attribute_type_id=args.attribute_type_id,
                short_name=args.short_name,
                long_name=args.long_name,
                description=args.description,
                parent_attribute_id=args.parent_attribute_id,
                value_int=args.value_int,
            )
            self.display.show(attribute, fields)
            success_msg = "Attribute created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the attribute")

    @command
    @aliases("delete-by-id")
    @option(
        "-id", "--attribute-id", type=int, help="ID of the attribute", required=True
    )
    def delete_attribute_by_id(self, args):
        """
        Deletes a specific attribute by ID.
        """
        try:
            self.display.v("Calling delete_attribute_by_id function")
            self.class_object.delete_by_id(args.attribute_id, expected_status_code=200)
            success_msg = f"Attribute with ID {args.attribute_id} deleted successfully"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to delete the attribute")

    @command
    @aliases("get-by-managed-account-id")
    @option(
        "-id",
        "--managed-account-id",
        type=int,
        help="ID of the managed account",
        required=True,
    )
    def get_attributes_by_managed_account_id(self, args):
        """
        Retrieves all attributes for a specific managed account ID.
        """
        try:
            fields = self.get_fields(
                GET_ATTRIBUTES_MANAGED_ACCOUNT_ID, attribute_fields, Version.DEFAULT
            )
            self.display.v("Calling get_attributes_by_managed_account_id function")
            attributes = self.class_object.get_attributes_by_managed_account_id(
                managed_account_id=args.managed_account_id
            )
            self.display.show(attributes, fields)
            success_msg = "Attributes retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the attributes")

    @command
    @aliases("get-by-managed-system-id")
    @option(
        "-id",
        "--managed-system-id",
        type=int,
        help="ID of the managed system",
        required=True,
    )
    def get_attributes_by_managed_system_id(self, args):
        """
        Retrieves all attributes for a specific managed system ID.
        """
        try:
            fields = self.get_fields(
                GET_ATTRIBUTES_MANAGED_SYSTEM_ID, attribute_fields, Version.DEFAULT
            )
            self.display.v("Calling get_attributes_by_managed_system_id function")
            attributes = self.class_object.get_attributes_by_managed_system_id(
                managed_system_id=args.managed_system_id
            )
            self.display.show(attributes, fields)
            success_msg = "Attributes retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the attributes")

    @command
    @aliases("assign-by-managed-account-id")
    @option(
        "-id",
        "--managed-account-id",
        type=int,
        help="ID of the managed account",
        required=True,
    )
    @option(
        "-a-id", "--attribute-id", type=int, help="ID of the attribute", required=True
    )
    def post_attribute_by_managed_account_id(self, args):
        """
        Assign a new attribute for a specific managed account ID.
        """
        try:
            fields = self.get_fields(
                POST_ATTRIBUTE_MANAGED_ACCOUNT_ID, attribute_fields, Version.DEFAULT
            )
            self.display.v("Calling post_attribute_by_managed_account_id function")
            attribute = self.class_object.post_attribute_by_managed_account_id(
                managed_account_id=args.managed_account_id,
                attribute_id=args.attribute_id,
            )
            self.display.show(attribute, fields)
            success_msg = "Attribute assigned successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to assign the attribute to a managed account."
            )

    @command
    @aliases("assign-by-managed-system-id")
    @option(
        "-id",
        "--managed-system-id",
        type=int,
        help="ID of the managed system",
        required=True,
    )
    @option(
        "-a-id", "--attribute-id", type=int, help="ID of the attribute", required=True
    )
    def post_attribute_by_managed_system_id(self, args):
        """
        Assign a new attribute for a specific managed system ID.
        """
        try:
            fields = self.get_fields(
                POST_ATTRIBUTE_MANAGED_SYSTEM_ID, attribute_fields, Version.DEFAULT
            )
            self.display.v("Calling post_attribute_by_managed_system_id function")
            attribute = self.class_object.post_attribute_by_managed_system_id(
                managed_system_id=args.managed_system_id, attribute_id=args.attribute_id
            )
            self.display.show(attribute, fields)
            success_msg = "Attribute assigned successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to assign the attribute to a managed system.")

    @command
    @aliases("delete-by-managed-account-id")
    @option(
        "-id",
        "--managed-account-id",
        type=int,
        help="ID of the managed account",
        required=True,
    )
    def delete_attributes_by_managed_account_id(self, args):
        """
        Deletes all attributes for a specific managed account ID.
        """
        try:
            self.display.v("Calling delete_attributes_by_managed_account_id function")
            self.class_object.delete_attributes_by_managed_account_id(
                managed_account_id=args.managed_account_id
            )
            success_msg = "Attributes deleted successfully"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete the attributes from the managed account."
            )

    @command
    @aliases("delete-by-managed-account-id-attribute-id")
    @option(
        "-id",
        "--managed-account-id",
        type=int,
        help="ID of the managed account",
        required=True,
    )
    @option(
        "-a-id", "--attribute-id", type=int, help="ID of the attribute", required=True
    )
    def delete_attributes_by_managed_account_id_attribute_id(self, args):
        """
        Deletes a managed account attribute by managed account ID and attribute ID.
        """
        try:
            self.display.v(
                "Calling delete_attributes_by_managed_account_id_attribute_id function"
            )
            self.class_object.delete_attributes_by_managed_account_id_attribute_id(
                managed_account_id=args.managed_account_id,
                attribute_id=args.attribute_id,
            )
            success_msg = "Attribute deleted successfully"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete the attribute from the managed account."
            )

    @command
    @aliases("delete-by-managed-system-id")
    @option(
        "-id",
        "--managed-system-id",
        type=int,
        help="ID of the managed system",
        required=True,
    )
    def delete_attributes_by_managed_system_id(self, args):
        """
        Deletes all attributes for a specific managed system ID.
        """
        try:
            self.display.v("Calling delete_attributes_by_managed_system_id function")
            self.class_object.delete_attributes_by_managed_system_id(
                managed_system_id=args.managed_system_id
            )
            success_msg = "Attributes deleted successfully"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete the attributes from the managed system."
            )

    @command
    @aliases("delete-by-managed-system-id-attribute-id")
    @option(
        "-id",
        "--managed-system-id",
        type=int,
        help="ID of the managed system",
        required=True,
    )
    @option(
        "-a-id", "--attribute-id", type=int, help="ID of the attribute", required=True
    )
    def delete_attributes_by_managed_system_id_attribute_id(self, args):
        """
        Deletes a managed system attribute by managed system ID and attribute ID.
        """
        try:
            self.display.v(
                "Calling delete_attributes_by_managed_system_id_attribute_id function"
            )
            self.class_object.delete_attributes_by_managed_system_id_attribute_id(
                managed_system_id=args.managed_system_id, attribute_id=args.attribute_id
            )
            success_msg = "Attribute deleted successfully"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete the attribute from the managed system."
            )
