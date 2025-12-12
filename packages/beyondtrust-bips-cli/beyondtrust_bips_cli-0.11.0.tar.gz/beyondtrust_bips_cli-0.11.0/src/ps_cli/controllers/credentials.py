from secrets_safe_library import credentials, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_CREDENTIALS_ALIASID,
    GET_CREDENTIALS_REQUESTID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.credentials import fields as credential_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Credential(CLIController):
    """
    Works with Secrets Safe Credentials - Get by Request ID or Alias ID

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="credentials",
            help="Credentials management commands",
        )

    @property
    def class_object(self) -> credentials.Credentials:
        if self._class_object is None and self.app is not None:
            self._class_object = credentials.Credentials(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("get-by-request-id")
    @option(
        "-r",
        "--request-id",
        help="The Request ID to get the credential",
        type=int,
        required=True,
    )
    @option(
        "-t",
        "--type",
        help="The type of credential to get. Options: 'password', 'ssh_key'",
        type=str,
        required=False,
    )
    def get_credential_by_request_id(self, args):
        """
        Returns a credential by Request ID.
        """
        try:
            fields = self.get_fields(
                GET_CREDENTIALS_REQUESTID, credential_fields, Version.DEFAULT
            )
            self.display.v("Calling get_credential_by_request_id function")
            credential = self.class_object.get_credentials_by_request_id(
                request_id=args.request_id,
                type=args.type,
            )
            self.display.show(credential, fields)
            success_msg = "Credential retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get a credential for "
                f"Request ID: {args.request_id}"
            )

    @command
    @aliases("get-by-alias-id")
    @option(
        "-a",
        "--alias-id",
        help="The Alias ID to get the credential",
        type=int,
        required=True,
    )
    @option(
        "-r",
        "--request-id",
        help="The Request ID to get the credential",
        type=int,
        required=True,
    )
    @option(
        "-t",
        "--type",
        help="The type of credential to get. Options: 'password', 'ssh_key'",
        type=str,
        required=False,
    )
    def get_credential_by_alias_id(self, args):
        """
        Returns a credential by Alias ID and Request ID.
        """
        try:
            fields = self.get_fields(
                GET_CREDENTIALS_ALIASID, credential_fields, Version.DEFAULT
            )
            self.display.v("Calling get_credential_by_alias_id function")
            credential = self.class_object.get_credentials_by_alias_id(
                alias_id=args.alias_id,
                request_id=args.request_id,
                type=args.type,
            )
            self.display.show(credential, fields)
            success_msg = "Credential retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get a credential for "
                f"Alias ID: {args.alias_id} and Request ID: {args.request_id}"
            )
