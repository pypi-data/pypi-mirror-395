from secrets_safe_library import dss_key_policies, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_DSS_KEY_RULES,
    GET_DSS_KEY_RULES_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.dss_key_policies import (
    fields as dss_key_policies_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class DSSKeyPolicies(CLIController):
    """
    Controller for managing DSS Key Policies.

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self) -> None:
        super().__init__(
            name="dss-key-policies",
            help="DSS Key Policies management commands",
        )

    @property
    def class_object(self) -> dss_key_policies.DSSKeyPolicies:
        if self._class_object is None and self.app is not None:
            self._class_object = dss_key_policies.DSSKeyPolicies(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_dss_key_policies(self, args):
        """
        Lists all DSS Key Policies.
        """
        try:
            fields = self.get_fields(
                GET_DSS_KEY_RULES, dss_key_policies_fields, Version.DEFAULT
            )
            self.display.v("Calling list_dss_key_policies function")
            policies = self.class_object.list()
            self.display.show(policies, fields)
            success_msg = "DSS Key Policies listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list DSS Key Policies")

    @command
    @aliases("get")
    @option(
        "-id",
        "--id_policy",
        help="ID of the DSS Key Policy to retrieve.",
        type=int,
        required=True,
    )
    def get_dss_key_policy_by_id(self, args):
        """
        Retrieves a DSS Key Policy by its ID.
        """
        try:
            fields = self.get_fields(
                GET_DSS_KEY_RULES_ID, dss_key_policies_fields, Version.DEFAULT
            )
            self.display.v("Calling get_dss_key_policy_by_id function")
            policy = self.class_object.get_by_id(object_id=args.id_policy)
            self.display.show(policy, fields)
            success_msg = (
                f"DSS Key Policy with ID {args.id_policy} retrieved successfully"
            )
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                f"It was not possible to get DSS Key Policy with ID {args.id_policy}"
            )
