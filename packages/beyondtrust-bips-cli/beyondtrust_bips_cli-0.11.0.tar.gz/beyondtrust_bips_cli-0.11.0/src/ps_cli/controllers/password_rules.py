from secrets_safe_library import exceptions, password_rules
from secrets_safe_library.constants.endpoints import (
    GET_PASSWORD_RULES,
    GET_PASSWORD_RULES_ENABLED_PRODUCTS,
    GET_PASSWORD_RULES_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.password_rules import fields as rule_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class PasswordRule(CLIController):
    """
    Secret Safe Password Rules functionality.
    """

    def __init__(self):
        super().__init__(
            name="password-rules",
            help="Password rules management commands",
        )

    @property
    def class_object(self) -> password_rules.PasswordRule:
        if self._class_object is None and self.app is not None:
            self._class_object = password_rules.PasswordRule(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_password_rules(self, args):
        """
        Returns a list of password rules.
        """
        try:
            fields = self.get_fields(GET_PASSWORD_RULES, rule_fields, Version.DEFAULT)
            self.display.v("Calling list_password_rules function")
            rules = self.class_object.list()
            self.display.show(rules, fields)
            success_msg = "Password rules listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list password rules")

    @command
    @aliases("get")
    @option(
        "-id",
        "--rule-id",
        help="ID of the password rule",
        type=int,
        required=True,
    )
    def get_password_rule(self, args):
        """
        Returns a password rule by ID.
        """
        try:
            fields = self.get_fields(
                GET_PASSWORD_RULES_ID, rule_fields, Version.DEFAULT
            )
            self.display.v(f"Searching by ID {args.rule_id}")
            safe = self.class_object.get_by_id(args.rule_id)
            self.display.show(safe, fields)
            success_msg = f"Password rule with ID {args.rule_id} retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to get a safe for ID: {args.rule_id}")

    @command
    @aliases("list-ep")
    @option(
        "-n",
        "--product-name",
        help=(
            "The product name to select polices enabled for Password Safe or Secrets "
            "Safe"
        ),
        type=str,
        required=False,
        choices=["PasswordSafe", "SecretsSafe"],
    )
    def list_enabled_products(self, args):
        """
        Returns a list of password rules, with an optional parameter to return polices
        enabled for Password Safe or Secrets Safe.
        """
        try:
            if args.product_name is not None:
                self.display.v(
                    f"Searching for enabled password rules for {args.product_name}"
                )
                fields = self.get_fields(
                    GET_PASSWORD_RULES_ENABLED_PRODUCTS, rule_fields, Version.DEFAULT
                )
                products = self.class_object.list_by_key(
                    key="enabledproducts", value=args.product_name
                )
            else:
                fields = self.get_fields(
                    GET_PASSWORD_RULES, rule_fields, Version.DEFAULT
                )
                self.display.v("Listing all password rules")
                products = self.class_object.list()
            self.display.show(products, fields)
            success_msg = "Enabled products listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list enabled products")
