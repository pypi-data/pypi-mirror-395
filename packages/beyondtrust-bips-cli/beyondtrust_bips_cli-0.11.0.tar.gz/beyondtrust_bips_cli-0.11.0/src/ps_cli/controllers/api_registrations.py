from secrets_safe_library import api_registrations, exceptions
from secrets_safe_library.constants.endpoints import (
    GET_API_REGISTRATIONS,
    GET_API_REGISTRATIONS_ID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.api_registrations import (
    fields as api_registration_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class APIRegistration(CLIController):
    """
    API Registration functionality.
    """

    def __init__(self):
        super().__init__(
            name="api-registrations",
            help="API Registrations management commands",
        )

    @property
    def class_object(self) -> api_registrations.APIRegistration:
        if self._class_object is None and self.app is not None:
            self._class_object = api_registrations.APIRegistration(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_api_registrations(self, args):
        """
        Returns a list of all API registrations.
        """
        try:
            fields = self.get_fields(
                GET_API_REGISTRATIONS, api_registration_fields, Version.DEFAULT
            )
            self.display.v("Calling list_api_registrations function")
            api_registrations = self.class_object.list()
            self.display.show(api_registrations, fields)
            success_msg = "API registrations listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list API registrations")

    @command
    @aliases("get")
    @option(
        "-id",
        "--api-registration-id",
        help="To get an API registration by ID",
        type=int,
        required=True,
    )
    def get_api_registration(self, args):
        """
        Returns an API registration by ID.
        """
        try:
            fields = self.get_fields(
                GET_API_REGISTRATIONS_ID, api_registration_fields, Version.DEFAULT
            )
            self.display.v(f"Searching by ID {args.api_registration_id}")
            api_registration = self.class_object.get_by_id(args.api_registration_id)
            self.display.show(api_registration, fields)
            success_msg = "API registration retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get an API registration for ID: "
                f"{args.api_registration_id}"
            )

    @command
    @aliases("get-key")
    @option(
        "-id",
        "--api-registration-id",
        help="To get an API key by API Registration ID",
        type=int,
        required=True,
    )
    def get_api_key(self, args):
        """
        Retrieves the API key for an API Key policy API Registration.
        """
        try:
            self.display.v(
                f"Searching API key by API Registration ID {args.api_registration_id}"
            )
            api_key = self.class_object.get_key_by_id(args.api_registration_id)
            print_it(api_key)
            self.display.v("API key retrieved successfully")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get an API key for API Registration ID: "
                f"{args.api_registration_id}"
            )

    @command
    @aliases("rotate-key")
    @option(
        "-id",
        "--api-registration-id",
        help="To rotate an API key by API Registration ID",
        type=int,
        required=True,
    )
    def rotate_api_key(self, args):
        """
        Rotates an API key by API Registration ID.
        """
        try:
            self.display.v(
                f"Rotating API key by API Registration ID {args.api_registration_id}"
            )
            api_key = self.class_object.rotate_api_key(args.api_registration_id)
            print_it(api_key)
            self.display.v("API key rotated successfully")
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to rotate an API key for ID: "
                f"{args.api_registration_id}"
            )

    @command
    @aliases("create")
    @option(
        "-n", "--name", help="The name of the API registration", type=str, required=True
    )
    @option(
        "-type",
        "--registration-type",
        help="The type of registration",
        type=str,
        required=True,
        choices=["apikeypolicy", "apiaccesspolicy"],
    )
    @option(
        "-token-dur",
        "--access-token-duration",
        help=(
            "The duration of the access token in minutes. Used with ApiAccessPolicy "
            "type"
        ),
        type=int,
        required=False,
        default=60,
    )
    @option(
        "-non-act",
        "--non-active",
        help="Indicates if the API Key policy should not be active by default.",
        action="store_false",
        dest="is_active",
        required=False,
    )
    @option(
        "-non-vis",
        "--non-visible",
        help="Indicates if the API Key policy should not be visible by default.",
        action="store_false",
        dest="is_visible",
        required=False,
    )
    @option(
        "-mfa",
        "--multi-factor-authentication",
        help="Enforce multi-factor authentication for the API Key policy.",
        action="store_true",
        required=False,
    )
    @option(
        "-cert",
        "--client-certificate",
        help="Require a client certificate for the API Key policy.",
        action="store_true",
        required=False,
    )
    @option(
        "-pass-req",
        "--user-password-required",
        help="Whether a user password is required.",
        action="store_true",
        required=False,
    )
    @option(
        "-verify-psrun",
        "--verify-psrun-signature",
        help="Whether to verify the PSRun signature for the API Key policy.",
        action="store_true",
        required=False,
    )
    @option(
        "-ip-rules",
        "--ip-authentication-rules",
        help="""IP authentication rules for the API policy.
        Format: "{'Type': str, 'Value': str, 'Description': str}" "..." """,
        type=str,
        nargs="+",
    )
    @option(
        "-psrun-rules",
        "--psrun-rules",
        help="""PSRun rules for the API policy.
        Format: "{'Id': int, 'IPAddress': str, 'MacAddress': str, 'SystemName': str,
        'FQDN': str, 'DomainName': str, 'UserId': str, 'RootVolumeId': str,
        'OSVersion': str}" "..." """,
        type=str,
        nargs="+",
    )
    @option(
        "-x-forwarded-for-rules",
        "--x-forwarded-for-authentication-rules",
        help="""X-Forwarded-For authentication rules for the API policy.
        Format: "{'Type': str, 'Value': str, 'Description': str}" "..." """,
        type=str,
        nargs="+",
    )
    def create_api_registration(self, args):
        """
        Creates a new API Registration.
        """
        try:
            fields = self.get_fields(
                GET_API_REGISTRATIONS_ID, api_registration_fields, Version.DEFAULT
            )

            self.display.v("Calling create_api_registration function")

            api_registration = self.class_object.create_api_registration(
                name=args.name,
                registration_type=args.registration_type,
                access_token_duration=args.access_token_duration,
                active=args.is_active,
                visible=args.is_visible,
                multi_factor_authentication_enforced=args.multi_factor_authentication,
                client_certificate_required=args.client_certificate,
                user_password_required=args.user_password_required,
                verify_psrun_signature=args.verify_psrun_signature,
                ip_authentication_rules=args.ip_authentication_rules,
                psrun_rules=args.psrun_rules,
                x_forwarded_for_authentication_rules=(
                    args.x_forwarded_for_authentication_rules
                ),
            )
            self.display.show(api_registration, fields)
            success_msg = "API registration created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.log.error(e)
            print_it(f"It was not possible to create the API Registration: {e}")

    def map_fields(self, data: list, fields: list) -> list:
        return [{field: record.get(field) for field in fields} for record in data]

    @command
    @aliases("update")
    @option(
        "-id",
        "--api-registration-id",
        help="The ID of the API registration to update",
        type=int,
        required=True,
    )
    @option(
        "-name",
        "--name",
        help="The name of the API registration",
        type=str,
        required=False,
    )
    @option(
        "-reg-type",
        "--registration-type",
        help="The type of the API registration",
        type=str,
        required=False,
    )
    @option(
        "-token-duration",
        "--access-token-duration",
        help="The duration of the access token",
        type=int,
        required=False,
    )
    @option(
        "--is-active",
        help="Whether the API registration is active",
        action="store_const",
        dest="is_active",
        const=True,
    )
    @option(
        "--is-not-active",
        help="Whether the API registration is not active",
        action="store_const",
        dest="is_active",
        const=False,
    )
    @option(
        "--is-visible",
        help="Whether the API registration is visible",
        action="store_const",
        dest="is_visible",
        const=True,
    )
    @option(
        "--is-not-visible",
        help="Whether the API registration is not visible",
        action="store_const",
        dest="is_visible",
        const=False,
    )
    @option(
        "--enable-mfa",
        help="Enforce multi-factor authentication for the API Key policy.",
        action="store_const",
        dest="multi_factor_authentication",
        const=True,
    )
    @option(
        "--disable-mfa",
        help="Do not enforce multi-factor authentication for the API Key policy.",
        action="store_const",
        dest="multi_factor_authentication",
        const=False,
    )
    @option(
        "--require-client-certificate",
        help="Require a client certificate for the API Key policy.",
        action="store_const",
        dest="client_certificate",
        const=True,
    )
    @option(
        "--no-client-certificate",
        help="Do not require a client certificate for the API Key policy.",
        action="store_const",
        dest="client_certificate",
        const=False,
    )
    @option(
        "--require-user-password",
        help="Require a user password.",
        action="store_const",
        dest="user_password_required",
        const=True,
    )
    @option(
        "--no-user-password",
        help="Do not require a user password.",
        action="store_const",
        dest="user_password_required",
        const=False,
    )
    @option(
        "-verify-psrun",
        "--verify-psrun-signature",
        help="Whether to verify the PSRun signature for the API Key policy.",
        action="store_true",
        required=False,
    )
    @option(
        "-ip-rules",
        "--ip-authentication-rules",
        help="""IP authentication rules for the API policy.
        Format: "{'Type': str, 'Value': str, 'Description': str}" "..." """,
        type=str,
        nargs="+",
    )
    @option(
        "-psrun-rules",
        "--psrun-rules",
        help="""PSRun rules for the API policy.
        Format: "{'Id': int, 'IPAddress': str, 'MacAddress': str, 'SystemName': str,
        'FQDN': str, 'DomainName': str, 'UserId': str, 'RootVolumeId': str,
        'OSVersion': str}" "..." """,
        type=str,
        nargs="+",
    )
    @option(
        "-x-forwarded-for-rules",
        "--x-forwarded-for-authentication-rules",
        help="""X-Forwarded-For authentication rules for the API policy.
        Format: "{'Type': str, 'Value': str, 'Description': str}" "..." """,
        type=str,
        nargs="+",
    )
    def update_api_registration(self, args):
        """
        Updates an existing API Registration.
        """
        try:
            if args.is_active is None:
                print_it(
                    "Should the API registration be active? "
                    "Use --is-active or --is-not-active accordingly"
                )
                return

            if args.is_visible is None:
                print_it(
                    "Should the API registration be visible? "
                    "Use --is-visible or --is-not-visible accordingly"
                )
                return

            if args.multi_factor_authentication is None:
                print_it(
                    "Should multi-factor authentication be enforced? "
                    "Use --enable-mfa or --disable-mfa accordingly"
                )
                return

            if args.client_certificate is None:
                print_it(
                    "Should a client certificate be required? Use "
                    "--require-client-certificate or --no-client-certificate "
                    "accordingly"
                )
                return

            if args.user_password_required is None:
                print_it(
                    "Should a user password be required? "
                    "Use --require-user-password or --no-user-password accordingly"
                )
                return

            fields = self.get_fields(
                GET_API_REGISTRATIONS_ID, api_registration_fields, Version.DEFAULT
            )

            self.display.v("Calling update_api_registration function")

            # Before updating, retrieve the existing API registration
            existing_registration = self.class_object.get_by_id(
                args.api_registration_id
            )

            rule_fields = ["Type", "Value", "Description"]
            psrun_rules_fields = [
                "Id",
                "IPAddress",
                "MacAddress",
                "SystemName",
                "FQDN",
                "DomainName",
                "UserId",
                "RootVolumeId",
                "OSVersion",
            ]

            ip_authentication_rules = args.ip_authentication_rules or self.map_fields(
                existing_registration.get("IPAuthenticationRules"), rule_fields
            )
            x_forwarded_for_authentication_rules = (
                args.x_forwarded_for_authentication_rules
                or self.map_fields(
                    existing_registration.get("XForwardedForAuthenticationRules"),
                    rule_fields,
                )
            )
            psrun_rules = args.psrun_rules or self.map_fields(
                existing_registration.get("PSRUNRules"), psrun_rules_fields
            )

            api_registration = self.class_object.update_api_registration(
                registration_id=args.api_registration_id,
                name=args.name or existing_registration.get("Name"),
                registration_type=args.registration_type
                or existing_registration.get("RegistrationType"),
                access_token_duration=args.access_token_duration
                or existing_registration.get("AccessTokenDuration"),
                active=args.is_active,
                visible=args.is_visible,
                multi_factor_authentication_enforced=args.multi_factor_authentication,
                client_certificate_required=args.client_certificate,
                user_password_required=args.user_password_required,
                verify_psrun_signature=args.verify_psrun_signature,
                ip_authentication_rules=ip_authentication_rules,
                psrun_rules=psrun_rules,
                x_forwarded_for_authentication_rules=(
                    x_forwarded_for_authentication_rules
                ),
            )
            self.display.show(api_registration, fields)
            success_msg = "API registration updated successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get an API registration for ID: "
                f"{args.api_registration_id}"
            )
        except exceptions.UpdateError as e:
            self.log.error(e)
            print_it(f"It was not possible to update the API Registration: {e}")

    @command
    @aliases("delete")
    @option(
        "-id",
        "--api-registration-id",
        help="To delete an API registration by ID",
        type=int,
        required=True,
    )
    def delete_api_registration(self, args):
        """
        Deletes an API registration by ID.
        """
        try:
            self.display.v(
                f"Deleting API registration by ID {args.api_registration_id}"
            )
            self.class_object.delete_by_id(
                args.api_registration_id, expected_status_code=200
            )
            success_msg = (
                f"API registration deleted successfully {args.api_registration_id}"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            print_it(
                "It was not possible to delete an API registration for ID: "
                f"{args.api_registration_id}"
            )
            print_it("Does API registration exist and provided ID is valid?")
            self.log.error(e)
