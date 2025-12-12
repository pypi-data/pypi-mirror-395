from secrets_safe_library import exceptions, managed_account, quick_rules
from secrets_safe_library.constants.endpoints import GET_QUICK_RULES, GET_QUICK_RULES_ID
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.quick_rules import fields as quick_rule_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class QuickRule(CLIController):
    """
    Secret Safe Quick Rules functionality.
    """

    def __init__(self):
        super().__init__(
            name="quick-rules",
            help="Quick Rules management commands",
        )

    _managed_account_object: managed_account.ManagedAccount | None = None

    @property
    def class_object(self) -> quick_rules.QuickRule:
        if self._class_object is None and self.app is not None:
            self._class_object = quick_rules.QuickRule(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def managed_account_object(self) -> managed_account.ManagedAccount:
        if self._managed_account_object is None and self.app is not None:
            self._managed_account_object = managed_account.ManagedAccount(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._managed_account_object

    @command
    @aliases("create")
    @option(
        "-ids",
        help="A list of IDs to add to the Quick Rule",
        type=int,
        nargs="+",
    )
    @option(
        "-t",
        "--title",
        help="The title of the Quick Rule",
        type=str,
        required=True,
    )
    @option(
        "-c",
        "--category",
        help="The category of the Quick Rule",
        type=str,
        default="Quick Rules",
    )
    @option(
        "-d",
        "--description",
        help="The description of the Quick Rule",
        type=str,
        default="",
    )
    @option(
        "-rt",
        "--rule-type",
        help="The type of the Quick Rule",
        type=str,
        choices=["ManagedAccount", "ManagedSystem"],
        default="ManagedAccount",
    )
    def create_quick_rule(self, args):
        """
        Creates a new Quick Rule.
        """
        try:
            fields = self.get_fields(
                GET_QUICK_RULES, quick_rule_fields, Version.DEFAULT.value
            )
            self.display.v("Calling create_quick_rule function")
            quick_rule = self.class_object.create_quick_rule(
                ids=args.ids,
                title=args.title,
                category=args.category,
                description=args.description,
                rule_type=args.rule_type,
            )
            self.display.show(quick_rule, fields)
            success_msg = "Quick Rule created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it(f"It was not possible to create the Quick Rule: {e}")

    @command
    @aliases("list")
    def list_quick_rules(self, args):
        """
        Returns a list of Quick Rules to which the current user has at least Read
        access.
        """
        try:
            fields = self.get_fields(
                GET_QUICK_RULES, quick_rule_fields, Version.DEFAULT
            )
            self.display.v("Calling list function")
            quick_rules = self.class_object.list()
            self.display.show(quick_rules, fields)
            success_msg = "Quick Rules listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list quick rules")

    @command
    @aliases("get")
    @option(
        "-id",
        "--quick-rule-id",
        help="To get a quick rule by ID",
        type=int,
        required=False,
    )
    @option(
        "-t",
        "--title",
        help="To get a quick rule by Title",
        type=str,
        required=False,
    )
    def get_quick_rule(self, args):
        """
        Returns a quick rule by ID or Title.
        """
        try:
            fields = self.get_fields(
                GET_QUICK_RULES_ID, quick_rule_fields, Version.DEFAULT
            )
            if args.quick_rule_id:
                self.display.v(f"Searching by ID {args.quick_rule_id}")
                quick_rule = self.class_object.get_by_id(args.quick_rule_id)
            elif args.title:
                self.display.v(f"Searching by Title {args.title}")
                quick_rule = self.class_object.list_by_key("title", args.title)
            else:
                print_it("Please provide either an ID or a Title to search for.")
                return
            self.display.show(quick_rule, fields)
            success_msg = "Quick Rule retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.quick_rule_id:
                print_it(
                    "It was not possible to get a quick rule for ID: "
                    f"{args.quick_rule_id}"
                )
            else:
                print_it(
                    f"It was not possible to get a quick rule for Title: {args.title}"
                )

    @command
    @aliases("get-by-org")
    @option(
        "-o-id",
        "--organization-id",
        help="To get a quick rule by Organization ID",
        type=int,
        required=True,
    )
    @option(
        "-t",
        "--title",
        help="To get a quick rule by Title",
        type=str,
        required=True,
    )
    def get_quick_rule_by_org(self, args):
        """
        Returns a Quick Rule by organization ID and title.
        """
        try:
            fields = self.get_fields(
                GET_QUICK_RULES_ID, quick_rule_fields, Version.DEFAULT
            )
            self.display.v(
                f"Searching by Organization ID {args.organization_id} and Title "
                f"{args.title}"
            )
            quick_rule = self.class_object.get_by_org_and_title(
                organization_id=args.organization_id, title=args.title
            )
            self.display.show(quick_rule, fields)
            success_msg = "Quick Rule retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get a quick rule for Organization ID: "
                f"{args.organization_id} and Title: {args.title}"
            )

    @command
    @aliases("delete")
    @option(
        "-id",
        "--quick-rule-id",
        help="To delete a quick rule by ID",
        type=int,
        required=False,
    )
    @option(
        "-t",
        "--title",
        help="To delete a quick rule by Title",
        type=str,
        required=False,
    )
    def delete_quick_rule(self, args):
        """
        Deletes a Quick Rule by ID or Title.
        """
        try:
            success_msg = ""
            if args.quick_rule_id:
                self.display.v(f"Deleting quick rule by ID {args.quick_rule_id}")
                self.class_object.delete_by_id(args.quick_rule_id)
            elif args.title:
                self.display.v(f"Deleting quick rule by Title {args.title}")
                self.class_object.delete_by_key("title", args.title)
            else:
                print_it("Please provide either an ID or a Title to delete.")
                return
            if args.quick_rule_id:
                success_msg = (
                    f"Quick Rule deleted successfully by ID {args.quick_rule_id}"
                )
            elif args.title:
                success_msg = f"Quick Rule deleted successfully by Title {args.title}"
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            if args.quick_rule_id:
                print_it(
                    "It was not possible to delete a quick rule for ID: "
                    f"{args.quick_rule_id}"
                )
            else:
                print_it(
                    "It was not possible to delete a quick rule for Title: "
                    f"{args.title}"
                )
            print_it("Does quick rule exist and provided ID is valid?")
            self.log.error(e)

    @command
    @aliases("delete-by-org")
    @option(
        "-o-id",
        "--organization-id",
        help="To delete a quick rule by Organization ID",
        type=int,
        required=True,
    )
    @option(
        "-t",
        "--title",
        help="To delete a quick rule by Title",
        type=str,
        required=True,
    )
    def delete_quick_rule_by_org(self, args):
        """
        Deletes a Quick Rule by organization ID and title.
        """
        try:
            self.display.v(
                f"Deleting quick rule by Organization ID {args.organization_id} and "
                f"Title {args.title}"
            )
            self.class_object.delete_by_org_and_title(
                organization_id=args.organization_id, title=args.title
            )
            success_msg = "Quick Rule deleted successfully."
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(
                f"It was not possible to delete a quick rule for Organization ID: "
                f"{args.organization_id} and Title: {args.title}"
            )
            self.log.error(e)
            print_it("Does quick rule exist and provided ID is valid?")

    @command
    @aliases("add-accounts")
    @option(
        "-id",
        "--quick-rule-id",
        help="The ID of the Quick Rule to which accounts will be added",
        type=int,
        required=True,
    )
    @option(
        "-a",
        "--account-ids",
        help="A list of account IDs to add to the Quick Rule",
        type=int,
        nargs="+",
        required=True,
    )
    @option(
        "-r",
        "--remove-previous",
        help="Remove previous accounts before adding new ones",
        action="store_true",
    )
    def add_accounts_to_quick_rule(self, args):
        """
        Adds accounts to a Quick Rule.
        """
        try:
            accounts = []

            if not args.remove_previous:
                self.display.v(
                    "Not removing previous accounts, adding new accounts with existing "
                    "ones."
                )
                prev_accounts = self.managed_account_object.list_by_quick_rule_id(
                    quick_rule_id=args.quick_rule_id
                )
                accounts.extend(
                    account.get("ManagedAccountID") for account in prev_accounts
                )

            accounts.extend(args.account_ids)

            self.display.v(
                f"Adding accounts {accounts} to Quick Rule ID {args.quick_rule_id}"
            )
            result = self.class_object.add_accounts_to_quick_rule(
                quick_rule_id=args.quick_rule_id,
                account_ids=accounts,
            )
            self.display.show(result, {})
            success_msg = (
                f"Accounts added successfully to Quick Rule ID: {args.quick_rule_id}"
            )
            self.display.v(success_msg)
        except exceptions.AdditionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to add accounts to Quick Rule ID: "
                f"{args.quick_rule_id}"
            )
