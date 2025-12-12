from secrets_safe_library import exceptions, smart_rules
from secrets_safe_library.constants.endpoints import GET_ASSETS_ID, GET_SMART_RULES
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.assets import fields as assets_fields
from secrets_safe_library.mapping.smart_rules import fields as smart_rule_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class SmartRule(CLIController):
    """
    Secret Safe Smart Rules functionality.
    """

    def __init__(self):
        super().__init__(
            name="smart-rules",
            help="Smart Rules management commands",
        )

    @property
    def class_object(self) -> smart_rules.SmartRule:
        if self._class_object is None and self.app is not None:
            self._class_object = smart_rules.SmartRule(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("create-with-attributes")
    @option(
        "-attr-ids",
        "--attribute-ids",
        help="A list of attribute IDs to add to the Smart Rule",
        type=int,
        nargs="+",
        required=True,
    )
    @option(
        "-t",
        "--title",
        help="The title of the Smart Rule",
        type=str,
        required=True,
    )
    @option(
        "-c",
        "--category",
        help="The category of the Smart Rule",
        type=str,
        default="Smart Rules",
    )
    @option(
        "-d",
        "--description",
        help="The description of the Smart Rule",
        type=str,
        default="",
    )
    @option(
        "--dont-process-immediately",
        help="Do not process the Smart Rule immediately",
        action="store_false",
        dest="process_immediately",
    )
    def create_rule_with_attributes(self, args):
        """
        Creates a new Smart Rule with the attributes referenced by ID.
        """
        try:
            fields = self.get_fields(
                GET_SMART_RULES, smart_rule_fields, Version.DEFAULT.value
            )
            self.display.v("Calling create_filter_asset_attribute function")
            smart_rule = self.class_object.create_filter_asset_attribute(
                attribute_ids=args.attribute_ids,
                title=args.title,
                category=args.category,
                description=args.description,
                process_immediately=args.process_immediately,
            )
            self.display.show(smart_rule, fields)
            success_msg = "Smart Rule created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it(f"It was not possible to create the Smart Rule: {e}")

    @command
    @aliases("list")
    def list_smart_rules(self, args):
        """
        Returns a list of Smart Rules to which the current user has at least Read
        access.
        """
        try:
            fields = self.get_fields(
                GET_SMART_RULES, smart_rule_fields, Version.DEFAULT
            )
            self.display.v("Calling list function")
            smart_rules = self.class_object.list()
            self.display.show(smart_rules, fields)
            success_msg = "Smart rules listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list smart rules")

    @command
    @aliases("get")
    @option(
        "-id",
        "--smart-rule-id",
        help="To get a smart rule by ID",
        type=int,
    )
    @option(
        "-t",
        "--title",
        help="To get a smart rule by Title",
        type=str,
    )
    def get_smart_rule(self, args):
        """
        Returns a smart rule by ID or Title.
        """
        try:
            fields = self.get_fields(
                GET_SMART_RULES, smart_rule_fields, Version.DEFAULT
            )
            if args.smart_rule_id:
                self.display.v(f"Searching by ID {args.smart_rule_id}")
                smart_rule = self.class_object.get_by_id(args.smart_rule_id)
            elif args.title:
                self.display.v(f"Searching by Title {args.title}")
                smart_rule = self.class_object.list_by_key("title", args.title)
            else:
                print_it("Please provide either an ID or a Title to search for.")
                return
            self.display.show(smart_rule, fields)
            success_msg = "Smart rule retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.smart_rule_id:
                print_it(
                    "It was not possible to get a smart rule for ID: "
                    f"{args.smart_rule_id}"
                )
            else:
                print_it(
                    f"It was not possible to get a smart rule for Title: {args.title}"
                )

    @command
    @aliases("list-assets")
    @option(
        "-id",
        "--smart-rule-id",
        help="Smart Rule ID to list assets for",
        type=int,
        required=True,
    )
    @option(
        "-l",
        "--limit",
        help="Limit the number of results",
        type=int,
        required=False,
    )
    @option(
        "-o",
        "--offset",
        help="Offset for pagination",
        type=int,
        required=False,
    )
    def list_assets_by_smart_rule(self, args):
        """
        Returns a list of assets associated with a Smart Rule.
        """
        try:
            self.display.v(f"Listing assets for Smart Rule ID {args.smart_rule_id}")
            assets = self.class_object.list_assets_by_smart_rule_id(
                smart_rule_id=args.smart_rule_id,
                limit=args.limit,
                offset=args.offset,
            )
            fields = self.get_fields(GET_ASSETS_ID, assets_fields, Version.DEFAULT)
            self.display.show(assets, fields)
            success_msg = "Assets listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to list assets for Smart Rule ID: "
                f"{args.smart_rule_id}"
            )

    @command
    @aliases("list-by-user-group")
    @option(
        "-ug-id",
        "--user-group-id",
        help="User Group ID to list smart rules for",
        type=int,
        required=True,
    )
    def list_smart_rules_by_user_group(self, args):
        """
        Returns a list of Smart Rules associated with a User Group.
        """
        try:
            fields = self.get_fields(
                GET_SMART_RULES, smart_rule_fields, Version.DEFAULT
            )
            self.display.v(
                f"Listing Smart Rules for User Group ID {args.user_group_id}"
            )
            smart_rules = self.class_object.list_smart_rules_by_user_group_id(
                user_group_id=args.user_group_id
            )
            self.display.show(smart_rules, fields)
            success_msg = "Smart rules listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to list smart rules for User Group ID: "
                f"{args.user_group_id}"
            )

    @command
    @aliases("run")
    @option(
        "-id",
        "--smart-rule-id",
        help="Smart Rule ID to run",
        type=int,
        required=True,
    )
    @option(
        "-q",
        "--queue",
        help="Queue the Smart Rule execution",
        action="store_true",
    )
    def run_smart_rule(self, args):
        """
        Processes a Smart Rule by ID.
        """
        try:
            fields = self.get_fields(
                GET_SMART_RULES, smart_rule_fields, Version.DEFAULT
            )
            self.display.v(f"Running Smart Rule ID {args.smart_rule_id}")
            result, status_code = self.class_object.run_smart_rule(
                smart_rule_id=args.smart_rule_id,
                queue=args.queue,
            )
            if status_code == 409:
                message = (
                    f"Smart Rule ID {args.smart_rule_id} is currently processing. "
                    "Please try again later."
                )
                print_it(message)
                self.log.info(message)
                return
            if result:
                self.display.show(result, fields)
            success_msg = "Smart Rule executed successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to run Smart Rule ID: {args.smart_rule_id}")
        except Exception as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"An error occurred while running Smart Rule ID: {args.smart_rule_id}"
            )

    @command
    @aliases("delete")
    @option(
        "-id",
        "--smart-rule-id",
        help="To delete a smart rule by ID",
        type=int,
    )
    @option(
        "-t",
        "--title",
        help="To delete a smart rule by Title",
        type=str,
    )
    def delete_smart_rule(self, args):
        """
        Deletes a Smart Rule by ID or Title.
        """
        try:
            success_msg = ""
            if args.smart_rule_id:
                self.display.v(f"Deleting smart rule by ID {args.smart_rule_id}")
                self.class_object.delete_by_id(args.smart_rule_id)
                success_msg = (
                    f"Smart Rule deleted successfully by ID {args.smart_rule_id}"
                )
            elif args.title:
                self.display.v(f"Deleting smart rule by Title {args.title}")
                self.class_object.delete_by_key("title", args.title)
                success_msg = f"Smart Rule deleted successfully by Title {args.title}"
            else:
                print_it("Please provide either an ID or Title")
                return
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            if args.smart_rule_id:
                print_it(
                    "It was not possible to delete a smart rule for ID: "
                    f"{args.smart_rule_id}"
                )
            else:
                print_it(
                    "It was not possible to delete a smart rule for Title: "
                    f"{args.title}"
                )
