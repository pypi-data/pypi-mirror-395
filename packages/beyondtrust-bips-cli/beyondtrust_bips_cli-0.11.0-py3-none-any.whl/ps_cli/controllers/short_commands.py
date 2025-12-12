from secrets_safe_library import (
    credentials,
    exceptions,
    isa_requests,
    managed_account,
    requests,
)

from ps_cli.core.controllers import ShortCommandController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class ShortCommand(ShortCommandController):
    """
    Short Commands functionality.
    """

    def __init__(self):
        super().__init__(
            name="short-commands",
            help=(
                "Short Commands simplify API workflows by reducing command-line input"
                " and chaining successive calls in a single command, instead of calling"
                " each endpoint directly."
            ),
        )

    _managed_account_object: managed_account.ManagedAccount | None = None
    _request_object: requests.Request | None = None
    _credential_object: credentials.Credentials | None = None
    _isa_request_object: isa_requests.ISARequest | None = None

    @property
    def managed_account_object(self) -> managed_account.ManagedAccount | None:
        if self._managed_account_object is None and self.app is not None:
            self._managed_account_object = managed_account.ManagedAccount(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._managed_account_object

    @property
    def request_object(self) -> requests.Request | None:
        if self._request_object is None and self.app is not None:
            self._request_object = requests.Request(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._request_object

    @property
    def credential_object(self) -> credentials.Credentials | None:
        if self._credential_object is None and self.app is not None:
            self._credential_object = credentials.Credentials(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._credential_object

    @property
    def isa_request_object(self) -> isa_requests.ISARequest | None:
        if self._isa_request_object is None and self.app is not None:
            self._isa_request_object = isa_requests.ISARequest(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._isa_request_object

    @command
    @aliases("retrieve-password-by-name")
    @option(
        "-sn",
        "--system-name",
        help="The managed system name. Use DatabaseName/InstanceName for databases",
        type=str,
        required=True,
    )
    @option(
        "-an",
        "--account-name",
        help="The managed account name",
        type=str,
        required=True,
    )
    @option(
        "-r",
        "--reason",
        help="The reason to retrieve a password",
        type=str,
        required=True,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="The request duration. Default request duration is 10 minutes",
        type=int,
        required=False,
        default=10,
    )
    @option(
        "-t",
        "--credential-type",
        help="The type of credentials to retrieve",
        type=str,
        required=False,
        default="password",
        choices=["password", "dsskey"],
    )
    @option(
        "-k",
        "--keep-request",
        help="Do not release created request (regular requests only)",
        action="store_true",
    )
    @option(
        "--use-isa",
        help="Use ISA-based access instead of regular requests",
        action="store_true",
    )
    def retrieve_password(self, args):
        """
        Finds an account by name, creates a request or ISA request, then retrieves
        credentials.
        For regular requests, the request is automatically released after credential
        retrieval (unless --keep-request is specified). ISA requests do not require
        manual release.
        """
        try:
            # Find the managed account
            account_data = self._find_managed_account(args)
            if not account_data:
                return

            # Retrieve password using appropriate method
            if args.use_isa:
                self._retrieve_via_isa_request(args, account_data)
            else:
                self._retrieve_via_regular_request(args, account_data)

        except exceptions.LookupError as e:
            self._handle_lookup_error(e)
        except exceptions.CreationError as e:
            self._handle_creation_error(e, args)
        except exceptions.UpdateError as e:
            self._handle_update_error(e)

    def _find_managed_account(self, args):
        """Find managed account by name and system name."""
        self.display.v(
            f"Searching for managed account '{args.account_name}' "
            f"on system '{args.system_name}'"
        )

        managed_accounts = self.managed_account_object.get_managed_accounts(
            account_name=args.account_name,
            system_name=args.system_name,
        )

        if not managed_accounts:
            print_it(
                f"No managed account found with name '{args.account_name}' "
                f"on system '{args.system_name}'"
            )
            return None

        # Get the first matching account
        managed_account_data = (
            managed_accounts[0]
            if isinstance(managed_accounts, list)
            else managed_accounts
        )
        account_id = managed_account_data.get("AccountId")
        system_id = managed_account_data.get("SystemId")

        if not account_id or not system_id:
            print_it(
                "Unable to retrieve account ID or system ID "
                "from managed account data"
            )
            return None

        self.display.v(
            f"Found managed account ID: {account_id}, system ID: {system_id}"
        )

        return {
            "account_id": account_id,
            "system_id": system_id,
            "data": managed_account_data,
        }

    def _retrieve_via_isa_request(self, args, account_data):
        """Retrieve password using ISA request."""
        self.display.v("Creating ISA request for credential retrieval")
        isa_request = self.isa_request_object.create_isa_request(
            system_id=account_data["system_id"],
            account_id=account_data["account_id"],
            duration_minutes=args.duration_minutes,
            reason=args.reason,
            type=args.credential_type,
        )

        # Display the credentials
        self.display.show(isa_request)
        self.display.v("Password retrieved successfully via ISA request")

    def _retrieve_via_regular_request(self, args, account_data):
        """Retrieve password using regular request flow."""
        request_id = None
        try:
            # Create request
            self.display.v(
                f"Creating request for account ID {account_data['account_id']}"
            )
            request_id, _ = self.request_object.post_request(
                system_id=account_data["system_id"],
                account_id=account_data["account_id"],
                duration_minutes=args.duration_minutes,
                reason=args.reason,
            )

            self.display.v(f"Request created successfully with ID: {request_id}")

            # Get credentials
            self._get_and_display_credentials(request_id, args.credential_type)

            # Release request if needed
            self._handle_request_cleanup(request_id, args.keep_request)

        except (
            exceptions.CreationError,
            exceptions.LookupError,
            exceptions.UpdateError,
        ):
            # Re-raise specific exceptions to be handled by main exception handlers
            if request_id and not args.keep_request:
                try:
                    self._cleanup_request(request_id)
                except Exception as cleanup_error:
                    self.log.error(
                        "Failed to cleanup request during error handling: "
                        f"{cleanup_error}"
                    )
            raise
        except Exception as e:
            # Only catch truly unexpected exceptions
            if request_id and not args.keep_request:
                try:
                    self._cleanup_request(request_id)
                except Exception as cleanup_error:
                    self.log.error(
                        "Failed to cleanup request during error handling: "
                        f"{cleanup_error}"
                    )
            self.log.error(f"Error during password retrieval: {e}")

    def _get_and_display_credentials(self, request_id, credential_type):
        """Get credentials and display them."""
        self.display.v(f"Retrieving credentials for request ID {request_id}")
        credential = self.credential_object.get_credentials_by_request_id(
            request_id=request_id,
            type=credential_type,
        )

        # Display the credentials
        self.display.show(credential)
        self.display.v("Password retrieved successfully")

    def _handle_request_cleanup(self, request_id, keep_request):
        """Handle request cleanup/release."""
        if keep_request:
            self.display.v(
                f"Request {request_id} not released due to --keep-request parameter"
            )
        else:
            self.display.v(f"Releasing request ID {request_id}")
            self.request_object.put_request_checkin(
                request_id=request_id,
                reason="Automatic release after password retrieval",
            )
            self.display.v(f"Request {request_id} released successfully")

    def _cleanup_request(self, request_id):
        """Clean up request on error."""
        self.request_object.put_request_checkin(
            request_id=request_id, reason="Error occurred - cleaning up"
        )
        self.display.v(f"Request {request_id} released due to error")

    def _handle_lookup_error(self, error):
        """Handle lookup errors."""
        self.display.v(error, save_log=False)
        self.log.error(error)
        print_it("Unable to find the specified managed account or retrieve credentials")

    def _handle_creation_error(self, error, args):
        """Handle creation errors."""
        self.display.v(error, save_log=False)
        self.log.error(error)
        if args.use_isa:
            print_it("It was not possible to create the ISA request")
        else:
            print_it("It was not possible to create the request")

    def _handle_update_error(self, error):
        """Handle update errors."""
        self.display.v(error, save_log=False)
        self.log.error(error)
        print_it("It was not possible to release the request")
