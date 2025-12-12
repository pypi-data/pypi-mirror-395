from secrets_safe_library import exceptions, request_sets, request_termination, requests
from secrets_safe_library.constants.endpoints import (
    GET_REQUEST_SETS,
    GET_REQUESTS,
    POST_REQUEST_SETS,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.request_sets import fields as request_sets_fields
from secrets_safe_library.mapping.requests import fields as requests_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Request(CLIController):
    """
    Works with Secrets Safe Requests - Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="requests",
            help="requests management commands",
        )

    _class_object_termination: request_termination.RequestTermination = None
    _class_object_sets: request_sets.RequestSets = None

    @property
    def class_object(self) -> requests.Request:
        if self._class_object is None and self.app is not None:
            self._class_object = requests.Request(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def class_object_termination(self) -> request_termination.RequestTermination:
        if self._class_object_termination is None and self.app is not None:
            self._class_object_termination = request_termination.RequestTermination(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object_termination

    @property
    def class_object_sets(self) -> request_sets.RequestSets:
        if self._class_object_sets is None and self.app is not None:
            self._class_object_sets = request_sets.RequestSets(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object_sets

    def _handle_request_creation_response(self, request_id, status_code):
        """
        Helper method to handle request creation response and status code validation.

        Args:
            request_id: The request id of the created or reused request.
            status_code: The HTTP status code returned
        """
        if status_code == 201:
            self.display.v("Request successful. Request ID in the response body.")
        else:
            self.display.v(
                "Existing request is being reused. "
                "Existing request ID in the response body."
            )
        self.display.show(f"RequestID: {request_id}")
        success_msg = f"Request processed successfully with ID: {request_id}"
        self.display.v(success_msg)

    @command
    @aliases("list")
    @option(
        "-s",
        "--status",
        help="The Request status. Options: all, pending, active",
        type=str,
        required=False,
        default="all",
    )
    @option(
        "-q",
        "--queue",
        help="The Request queue. Options: req, app",
        type=str,
        required=False,
        default="req",
    )
    def list_requests(self, args):
        """
        Returns a list of Requests to which the current user has access.
        """
        try:
            fields = self.get_fields(GET_REQUESTS, requests_fields, Version.DEFAULT)
            self.display.v("Calling list_requests function")
            requests_list = self.class_object.get_requests(
                status=args.status, queue=args.queue
            )
            self.display.show(requests_list, fields)
            success_msg = "Requests listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list requests")

    @command
    @aliases("create")
    @option(
        "-s-id",
        "--system-id",
        help="The Managed System id",
        type=int,
        required=True,
    )
    @option(
        "-a-id",
        "--account-id",
        help="The Managed Account id",
        type=int,
        required=True,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="The duration in minutes",
        type=int,
        required=True,
    )
    @option(
        "-app-id",
        "--application-id",
        help="The application id",
        type=int,
        required=False,
    )
    @option(
        "-r",
        "--reason",
        help="The reason for the request",
        type=str,
        required=False,
    )
    @option(
        "-a-type",
        "--access-type",
        help="The access type. Options: View, RDP, SSH, App",
        type=str,
        required=False,
    )
    @option(
        "-a-p-id",
        "--access-policy-schedule-id",
        help="The access policy schedule id",
        type=int,
        required=False,
    )
    @option(
        "-c-op",
        "--conflict-option",
        help="The conflict option",
        type=str,
        required=False,
    )
    @option(
        "-t-sys-id",
        "--ticket-system-id",
        help="The ticket system id",
        type=int,
        required=False,
    )
    @option(
        "-t-num",
        "--ticket-number",
        help="Ticket number associated with the request",
        type=str,
        required=False,
    )
    @option(
        "-r-o-c",
        "--rotate-on-checkin",
        help="Rotate on checkin",
        action="store_true",
    )
    def create_request(self, args):
        """
        Creates a new Request.
        """
        try:
            self.display.v("Calling create_request function")
            request, status_code = self.class_object.post_request(
                system_id=args.system_id,
                account_id=args.account_id,
                duration_minutes=args.duration_minutes,
                application_id=args.application_id,
                reason=args.reason,
                access_type=args.access_type,
                access_policy_schedule_id=args.access_policy_schedule_id,
                conflict_option=args.conflict_option,
                ticket_system_id=args.ticket_system_id,
                ticket_number=args.ticket_number,
                rotate_on_checkin=args.rotate_on_checkin,
            )
            self._handle_request_creation_response(request, status_code)
        except exceptions.CreationError as e:
            print_it("It was not possible to create request")
            print_it(f"Error: {e}")

    @command
    @aliases("create-by-alias")
    @option(
        "-a-id",
        "--alias-id",
        help="ID of the managed account alias.",
        type=int,
        required=True,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="The duration in minutes",
        type=int,
        required=True,
    )
    @option(
        "-a-type",
        "--access-type",
        help="The access type. Options: View, RDP, SSH, App",
        type=str,
        required=False,
    )
    @option(
        "-r",
        "--reason",
        help="The reason for the request",
        type=str,
        required=False,
    )
    @option(
        "-a-p-id",
        "--access-policy-schedule-id",
        help="The access policy schedule id",
        type=int,
        required=False,
    )
    @option(
        "-c-op",
        "--conflict-option",
        help="The conflict option",
        type=str,
        required=False,
    )
    @option(
        "-t-sys-id",
        "--ticket-system-id",
        help="The ticket system id",
        type=int,
        required=False,
    )
    @option(
        "-t-num",
        "--ticket-number",
        help="Ticket number associated with the request",
        type=str,
        required=False,
    )
    @option(
        "-r-o-c",
        "--rotate-on-checkin",
        help="Rotate on checkin",
        action="store_true",
    )
    def create_request_alias(self, args):
        """
        Creates a new release request using an alias.
        """
        try:
            self.display.v("Calling create_request function")
            request, status_code = self.class_object.post_request_alias(
                alias_id=args.alias_id,
                duration_minutes=args.duration_minutes,
                access_type=args.access_type,
                reason=args.reason,
                access_policy_schedule_id=args.access_policy_schedule_id,
                conflict_option=args.conflict_option,
                ticket_system_id=args.ticket_system_id,
                ticket_number=args.ticket_number,
                rotate_on_checkin=args.rotate_on_checkin,
            )
            self._handle_request_creation_response(request, status_code)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it("It was not possible to create request")
            print_it(f"Error: {e}")

    @command
    @aliases("checkin-request")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the check-in",
        type=str,
        required=False,
    )
    def put_request_checkin(self, args):
        """
        Check-in a Request.
        """
        try:
            self.display.v("Calling post_request_checkin function")
            self.class_object.put_request_checkin(
                request_id=args.request_id, reason=args.reason
            )
            success_msg = (
                f"Request with ID {args.request_id} was checked-in successfully"
            )
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to check-in request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")

    @command
    @aliases("approve-request")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the approval",
        type=str,
        required=False,
    )
    def put_request_approve(self, args):
        """
        Approve a Request.
        """
        try:
            self.display.v("Calling put_request_approve function")
            self.class_object.put_request_approve(
                request_id=args.request_id, reason=args.reason
            )
            success_msg = f"Request with ID {args.request_id} was approved successfully"
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.log.error(e)
            print_it("It was not possible to approve request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")

    @command
    @aliases("deny")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the denial",
        type=str,
        required=False,
    )
    def put_request_deny(self, args):
        """
        Deny a Request.
        """
        try:
            self.display.v("Calling put_request_deny function")
            self.class_object.put_request_deny(
                request_id=args.request_id, reason=args.reason
            )
            success_msg = f"Request with ID {args.request_id} was denied successfully"
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.log.error(e)
            print_it("It was not possible to deny request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")

    @command
    @aliases("rotate-on-checkin")
    @option(
        "-r-id",
        "--request-id",
        help="The Request id",
        type=int,
        required=True,
    )
    def request_rotate_on_checkin(self, args):
        """
        Updates a request to rotate the credentials on check-in/expiry.
        """
        try:
            self.display.v("Calling put_request_rotate_on_checkin function")
            self.class_object.put_request_rotate_on_checkin(request_id=args.request_id)
            success_msg = f"Request with ID {args.request_id} was rotated successfully"
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.log.error(e)
            print_it("It was not possible to rotate on check-in request")
            print_it(f"Error: {e}")
        except exceptions.LookupError as e:
            self.log.error(e)
            print_it(f"Request with ID {args.request_id} was not found")

    @command
    @aliases("termination-by-ma-id")
    @option(
        "-m-id",
        "--managed-account-id",
        help="The Managed Account id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the termination",
        type=str,
        required=False,
    )
    def termination_managed_account_id(self, args):
        """
        Terminates a Managed Account Request.
        """
        try:
            self.display.v(
                "Calling post_request_termination_managed_account_id " "function"
            )
            self.class_object_termination.post_request_termination_managed_account_id(
                managed_account_id=args.managed_account_id, reason=args.reason
            )
            success_msg = (
                f"Managed Account with ID {args.managed_account_id}"
                " was terminated successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it("It was not possible to terminate managed account")
            print_it(f"Error: {e}")

    @command
    @aliases("termination-by-ms-id")
    @option(
        "-s-id",
        "--managed-system-id",
        help="The Managed System id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the termination",
        type=str,
        required=False,
    )
    def termination_managed_system_id(self, args):
        """
        Terminates a Managed System Request.
        """
        try:
            self.display.v(
                "Calling post_request_termination_managed_system_id " "function"
            )
            self.class_object_termination.post_request_termination_managed_system_id(
                managed_system_id=args.managed_system_id, reason=args.reason
            )
            success_msg = (
                f"Managed System with ID {args.managed_system_id}"
                " was terminated successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to terminate managed system")
            print_it(f"Error: {e}")

    @command
    @aliases("termination-by-user")
    @option(
        "-u-id",
        "--user-id",
        help="The User id",
        type=int,
        required=True,
    )
    @option(
        "-re",
        "--reason",
        help="The reason for the termination",
        type=str,
        required=False,
    )
    def terminate_user_request(self, args):
        """
        Terminates a User Request.
        """
        try:
            self.display.v("Calling post_request_termination_user_id function")
            self.class_object_termination.post_request_termination_user_id(
                userid=args.user_id, reason=args.reason
            )
            success_msg = f"User with ID {args.user_id} was terminated successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it("It was not possible to terminate user")
            print_it(f"Error: {e}")

    @command
    @aliases("get-request-sets")
    @option(
        "-s",
        "--status",
        help="The Request status. Options: all, pending, active",
        type=str,
        required=False,
        default="all",
    )
    def get_request_set(self, args):
        """
        Returns a list of Requests to which the current user has access.
        """
        try:
            fields = self.get_fields(
                GET_REQUEST_SETS, request_sets_fields, Version.DEFAULT
            )
            self.display.v("Calling get_request_set function")
            request_set = self.class_object_sets.get_request_sets(status=args.status)
            self.display.show(request_set, fields)
            success_msg = "Request sets listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.log.error(e)
            print_it("It was not possible to get request set")
            print_it(f"Error: {e}")

    @command
    @aliases("create-request-sets")
    @option(
        "-a-types",
        "--access-types",
        help="The access types, at least two are required. "
        "Options: View, RDP, SSH, App",
        type=str,
        required=True,
        nargs="*",
    )
    @option(
        "-s-id",
        "--system-id",
        help="The Managed System id",
        type=int,
        required=True,
    )
    @option(
        "-a-id",
        "--account-id",
        help="The Managed Account id",
        type=int,
        required=True,
    )
    @option(
        "-d",
        "--duration-minutes",
        help="The duration in minutes",
        type=int,
        required=True,
    )
    @option(
        "-app-id",
        "--application-id",
        help="The application id",
        type=int,
        required=False,
    )
    @option(
        "-r",
        "--reason",
        help="The reason for the request",
        type=str,
        required=False,
    )
    @option(
        "-t-sys-id",
        "--ticket-system-id",
        help="The ticket system id",
        type=int,
        required=False,
    )
    @option(
        "-t-num",
        "--ticket-number",
        help="Ticket number associated with the request",
        type=str,
        required=False,
    )
    def create_request_set(self, args):
        """
        Creates a new Request Set.
        """
        try:
            fields = self.get_fields(
                POST_REQUEST_SETS, request_sets_fields, Version.DEFAULT
            )
            self.display.v("Calling create_request_set function")
            request_set = self.class_object_sets.post_request_sets(
                access_types=args.access_types,
                system_id=args.system_id,
                account_id=args.account_id,
                duration_minutes=args.duration_minutes,
                application_id=args.application_id,
                reason=args.reason,
                ticket_system_id=args.ticket_system_id,
                ticket_number=args.ticket_number,
            )
            self.display.show(request_set, fields)
            success_msg = "Request set created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it("It was not possible to create request set")
            print_it(f"Error: {e}")
