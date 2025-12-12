from secrets_safe_library import access_policies, exceptions, managed_account
from secrets_safe_library.constants.endpoints import (
    GET_ACCESS_POLICIES,
    POST_ACCESS_POLICIES_TEST,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.access_policies import fields as access_policy_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class AccessPolicy(CLIController):
    """
    List or set Access Policies for Password Safe.
    Requires Password Safe Role Management (Read).

    Use as the requestor. When testing directory accounts against a managed system,
    call the account by ID, not name.
    """

    def __init__(self):
        super().__init__(
            name="access-policies",
            help="Access policies commands",
        )

    _managed_account_object: managed_account.ManagedAccount | None = None

    @property
    def managed_account_object(self) -> managed_account.ManagedAccount:
        if self._managed_account_object is None and self.app is not None:
            self._managed_account_object = managed_account.ManagedAccount(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._managed_account_object

    @property
    def class_object(self) -> access_policies.AccessPolicy:
        if self._class_object is None and self.app is not None:
            self._class_object = access_policies.AccessPolicy(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_access_policies(self, args):
        """
        Returns a list of Password Safe access policies.
        """

        try:
            fields = self.get_fields(
                GET_ACCESS_POLICIES, access_policy_fields, Version.DEFAULT
            )
            self.display.v("Calling list_access_policies function")
            access_policies = self.class_object.list()
            self.display.show(access_policies, fields)
            success_msg = "Access policies listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list access policies")

    @command
    @aliases("test")
    @option(
        "-s-id",
        "--system-id",
        help="ID of the managed system",
        type=int,
        required=False,
    )
    @option(
        "-s-name",
        "--system-name",
        help="Name of the managed system",
        type=str,
        required=False,
    )
    @option(
        "-a-id",
        "--account-id",
        help="ID of the managed account",
        type=int,
        required=False,
    )
    @option(
        "-a-name",
        "--account-name",
        help="Name of the managed account",
        type=str,
        required=False,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="Duration in minutes",
        type=int,
        required=False,
        default=60,
    )
    def test_access_policy(self, args):
        """
        Tests an access policy against a managed system and account.

        Need to provide either managed system ID and account ID,
        or managed system name and account name.
        """
        try:
            if not (args.system_id and args.account_id) and not (
                args.system_name and args.account_name
            ):
                print_it(
                    "Please provide either system ID or name, and account ID or name"
                )
                return

            if args.system_name and args.account_name:
                self.display.v("Searching for managed system and account by name")
                managed_account = self.managed_account_object.get_managed_accounts(
                    account_name=args.account_name,
                    system_name=args.system_name,
                )

                if not isinstance(managed_account, dict):
                    print_it("More than one managed account found")
                    return
                else:
                    args.system_id = managed_account.get("SystemId", None)
                    args.account_id = managed_account.get("AccountId", None)

            self.display.v("Calling test_access_policy function")
            response_text, status_code = self.class_object.test_access_policy(
                system_id=args.system_id,
                account_id=args.account_id,
                duration_minutes=args.duration_minutes,
            )
            if status_code == 200:
                fields = self.get_fields(
                    POST_ACCESS_POLICIES_TEST, access_policy_fields, Version.DEFAULT
                )
                self.display.show(response_text, fields)
            else:
                self.display.v(response_text)
                print_it("Access policy test failed")
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it(f"It was not possible to test the access policy. {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to find the system or account")
