from secrets_safe_library import exceptions, functional_accounts
from secrets_safe_library.constants.endpoints import (
    GET_FUNCTIONAL_ACCOUNTS,
    GET_FUNCTIONAL_ACCOUNTS_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.data_classes import SSHConfig
from secrets_safe_library.mapping.functional_accounts import (
    fields as functional_account_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class FunctionalAccount(CLIController):
    """
    Secret Safe Functional Accounts functionality.
    """

    def __init__(self):
        super().__init__(
            name="functional-accounts",
            help="Functional Accounts management commands",
        )

    @property
    def class_object(self) -> functional_accounts.FunctionalAccount:
        if self._class_object is None and self.app is not None:
            self._class_object = functional_accounts.FunctionalAccount(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_functional_accounts(self, args):
        """
        Returns a list of functional accounts.
        """
        try:
            fields = self.get_fields(
                GET_FUNCTIONAL_ACCOUNTS, functional_account_fields, Version.DEFAULT
            )
            self.display.v("Calling list_functional_accounts function")
            functional_accts = self.class_object.list()
            self.display.show(functional_accts, fields)
            success_msg = "Functional accounts listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list functional accounts")

    @command
    @aliases("get")
    @option(
        "-id",
        "--functional-account-id",
        help="To get a functional account by ID",
        type=int,
        required=False,
        enforce_uuid=False,
    )
    @option(
        "-n",
        "--name",
        help="To get a functional account by Name",
        type=str,
        required=False,
    )
    def get_functional_account(self, args):
        """
        Returns a functional account by ID or Name.
        """
        try:
            fields = self.get_fields(
                GET_FUNCTIONAL_ACCOUNTS_ID, functional_account_fields, Version.DEFAULT
            )

            if args.functional_account_id is not None:
                self.display.v(f"Searching by ID {args.functional_account_id}")
                functional_account = self.class_object.get_by_id(
                    args.functional_account_id
                )
            elif args.name is not None:
                self.display.v(f"Searching by name {args.name}")
                accounts = self.class_object.list()

                functional_account = next(
                    (
                        account
                        for account in accounts
                        if account["AccountName"] == args.name
                    ),
                    None,
                )

                if functional_account is None:
                    print_it(f"No functional account was found with name {args.name}")
                    return
            else:
                print_it("Either ID or Name is required")
                return

            self.display.show(functional_account, fields)
            success_msg = "Functional account retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            if args.functional_account_id is not None:
                print_it(
                    "It was not possible to get a functional account for ID: "
                    f"{args.functional_account_id}"
                )
            elif args.name is not None:
                print_it(
                    "It was not possible to get a functional account for name: "
                    f"{args.name}"
                )

    @command
    @aliases("create")
    @option(
        "-p",
        "--platform-id",
        help="ID of the platform to which the account belongs",
        type=int,
        required=True,
    )
    @option(
        "-n",
        "--account-name",
        help="Name of the functional account",
        type=str,
        required=True,
    )
    @option(
        "-d",
        "--display-name",
        help="Display name of the functional account",
        type=str,
        required=False,
    )
    @option(
        "-desc",
        "--description",
        help="Description of the functional account",
        type=str,
        required=False,
    )
    @option(
        "-dom",
        "--domain-name",
        help="Domain name of the functional account",
        type=str,
        required=False,
    )
    @option(
        "-pwd",
        "--password",
        help="Password for the functional account",
        type=str,
        required=False,
    )
    @option(
        "-pk",
        "--private-key",
        help="Private key for the functional account",
        type=str,
        required=False,
    )
    @option(
        "-pp",
        "--passphrase",
        help="Passphrase for the private key",
        type=str,
        required=False,
    )
    @option(
        "-ec",
        "--elevation-command",
        help="Elevation command for the functional account",
        type=str,
        required=False,
    )
    @option(
        "-tid",
        "--tenant-id",
        help="Tenant ID for the functional account",
        type=str,
        required=False,
    )
    @option(
        "-oid",
        "--object-id",
        help="Object ID for the functional account",
        type=str,
        required=False,
    )
    @option(
        "-s",
        "--secret",
        help="Secret for the functional account",
        type=str,
        required=False,
    )
    @option(
        "-sae",
        "--service-account-email",
        help="Service account email for the functional account",
        type=str,
        required=False,
    )
    @option(
        "-ai",
        "--azure-instance",
        help="Azure instance for the functional account (default: AzurePublic)",
        type=str,
        required=False,
        default="AzurePublic",
    )
    def create_functional_account(self, args):
        """
        Creates a functional account in the specified platform.
        """
        try:
            fields = self.get_fields(
                GET_FUNCTIONAL_ACCOUNTS_ID, functional_account_fields, Version.DEFAULT
            )
            self.display.v("Creating functional account with provided details")
            ssh_config = SSHConfig(
                private_key=args.private_key,
                passphrase=args.passphrase,
                elevation_command=args.elevation_command,
            )
            functional_account, _ = self.class_object.create_functional_account(
                platform_id=args.platform_id,
                account_name=args.account_name,
                display_name=args.display_name,
                description=args.description,
                domain_name=args.domain_name,
                password=args.password,
                ssh_config=ssh_config,
                tenant_id=args.tenant_id,
                object_id=args.object_id,
                secret=args.secret,
                service_account_email=args.service_account_email,
                azure_instance=args.azure_instance,
            )
            self.display.show(functional_account, fields)
            success_msg = "Functional account created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            print_it("It was not possible to create the functional account")
            self.log.error(e)

    @command
    @aliases("delete")
    @option(
        "-id",
        "--functional-account-id",
        help="To delete a functional account by ID",
        type=str,
        required=True,
        enforce_uuid=False,
    )
    def delete_functional_account(self, args):
        """
        Deletes a functional account by ID.
        """
        try:
            self.display.v(
                f"Deleting functional account by ID {args.functional_account_id}"
            )
            self.class_object.delete_by_id(
                args.functional_account_id, expected_status_code=200
            )
            success_msg = (
                f"Functional account deleted successfully {args.functional_account_id}"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(
                "It was not possible to delete a functional account for ID: "
                f"{args.functional_account_id}"
            )
            print_it("Does functional account exist and provided ID is valid?")
            self.log.error(e)
