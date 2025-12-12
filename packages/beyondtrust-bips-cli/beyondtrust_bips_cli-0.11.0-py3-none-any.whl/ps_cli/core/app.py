import argparse
import os
from typing import List, Type

import requests
import urllib3
from retry_requests import retry
from secrets_safe_library import authentication, exceptions
from secrets_safe_library.constants.versions import Version

from ps_cli.core.constants import Delimiter, Format
from ps_cli.core.display import Display, print_it
from ps_cli.core.exceptions import InvalidAuthenticationException
from ps_cli.core.interfaces import AppInterface, ControllerInterface
from ps_cli.core.logger import LOG_LEVELS, Logger
from ps_cli.core.settings import SettingsManager
from ps_cli.core.version import get_api_version, get_cli_version

env = os.environ


class App(AppInterface):
    display: Display
    log: Logger
    api_version: str

    def __init__(self, controllers: List[Type[ControllerInterface]], args=None) -> None:
        """
        Initialize the App instance.

        Args:
            controllers (List[Type[ControllerInterface]]): List of controller classes.
            args (list, optional): Command-line arguments for testing. Defaults to None.
        """
        # Set available controllers
        self.controllers = controllers

        # Initialize main argument parser
        self.parser = self._create_parser()
        self.subparsers = self.parser.add_subparsers(dest="service", required=False)

        # Register each controller's subparsers
        self._register_controllers()

        # Parse args
        self.args = self.parser.parse_args(args)

        # Before instantiating any other attribute, we need settings to be available
        self._settings = SettingsManager()

        # API version
        self.api_version = self.args.api_version

        # Logging object
        log_level = "DEBUG" if self.args.verbose else self.args.log_level
        self.log = self._create_logger(log_level)

        # Display object, used for verbose output
        self.display = Display(
            self.args.verbose, self.log, self.args.format, self.args.delimiter
        )

        # Authentication object used to make calls to the API
        self.authentication = None

        if hasattr(self.args, "service") and self.args.service != "settings":
            # Settings doesn't need communication with API
            self._generate_authentication()

            # Only show version if authentication is successful, required because
            # it calls Configuration/Version endpoint.
            if self.args.version:
                print_it(f"ps-cli v{get_cli_version(self)}")
                print_it(f"API v{get_api_version(self)}")

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the main argument parser for the CLI.

        Returns:
            argparse.ArgumentParser: The main argument parser.
        """
        parser = argparse.ArgumentParser(
            prog="ps-cli",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Password Safe CLI",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Increase verbosity level (-v, -vv, -vvv, -vvvvv, -vvvvv)",
        )
        parser.add_argument(
            "-l",
            "--log-level",
            type=str,
            default=None,
            choices=[*LOG_LEVELS.keys()],
            help="Set log level (overrides log_level from settings.ini)",
        )
        parser.add_argument(
            "--format",
            type=str,
            default=Format.TSV.value,
            choices=[format.value for format in Format],
            help="Output format, TSV - tab separated value by default",
        )
        parser.add_argument(
            "--delimiter",
            type=str,
            default=Delimiter.COMMA.value,
            choices=[delimiter.value for delimiter in Delimiter],
            help="CSV delimiter",
        )
        parser.add_argument(
            "-av",
            "--api-version",
            type=str,
            default=Version.V3_0.value,
            choices=[
                version.value for version in Version if version != Version.DEFAULT
            ],
            help="PS API version to use",
        )
        parser.add_argument(
            "--version",
            action="store_true",
            help="Show CLI and API versions",
        )
        return parser

    @property
    def settings(self) -> SettingsManager:
        return self._settings

    def _generate_authentication(self):
        self.display.v("Generating authentication")

        if self.settings:
            api_url = env.get("PSCLI_API_URL", self.settings.get("general", "api_url"))
            api_version = self.api_version or env.get(
                "PSCLI_API_VERSION", self.settings.get("general", "api_version")
            )
            retries = env.get(
                "PSCLI_AUTH_RETRIES",
                self.settings.get("authentication", "request_retries", 3),
            )
            timeout_connection = env.get(
                "PSCLI_TIMEOUT_CONNECTION",
                self.settings.get("authentication", "timeout_connection", 30),
            )
            timeout_request = env.get(
                "PSCLI_TIMEOUT_REQUEST",
                self.settings.get("authentication", "timeout_request", 30),
            )

            client_id = env.get(
                "PSCLI_CLIENT_ID", self.settings.get("authentication", "client_id")
            )
            client_secret = env.get(
                "PSCLI_CLIENT_SECRET",
                self.settings.get("authentication", "client_secret"),
            )
            client_verify_ca = env.get(
                "PSCLI_VERIFY_CA",
                self.settings.get("authentication", "verify_ca", "true"),
            )

            if not api_url:
                print_it(
                    "Can't authenticate with API since api_url is not set yet "
                    "missing setting: [general] api_url"
                )
            if not client_id:
                print_it(
                    "Can't authenticate with API since client_id is not set yet "
                    "missing setting: [authentication] client_id"
                )
            if not client_secret:
                print_it(
                    "Can't authenticate with API since client_secret is not set yet "
                    "missing setting: [authentication] client_secret"
                )

            if all([api_url, client_id, client_secret]):
                if client_verify_ca.lower() == "false":
                    urllib3.disable_warnings(
                        category=urllib3.exceptions.InsecureRequestWarning
                    )
                    self.display.v(
                        "WARNING: Certificate Authority verification is disabled"
                    )
                with requests.Session() as session:
                    req = retry(
                        session,
                        retries=int(retries),
                        backoff_factor=0.2,
                        status_to_retry=(408, 500, 502, 503, 504),
                    )

                    logger = self.log.logger if self.log else None

                    auth_config = {
                        "req": req,
                        "timeout_connection": int(timeout_connection),
                        "timeout_request": int(timeout_request),
                        "api_url": api_url,
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "logger": logger,
                        "api_version": api_version,
                        "verify_ca": client_verify_ca.lower() == "true",
                    }

                    self.authentication = authentication.Authentication(**auth_config)

                    get_api_access_response = self.authentication.get_api_access()
                    self.display.v("API access request completed")

                    if get_api_access_response.status_code != 200:
                        if self.log:
                            err_msg = (
                                "get_api_access.status_code: "
                                f"{get_api_access_response.status_code}: "
                                f"{get_api_access_response.text}"
                            )
                            self.display.v(err_msg)

                        raise InvalidAuthenticationException("Unable to authenticate")
            else:
                print_it(
                    "Please complete required settings in: "
                    f"{self.settings.settings_path}"
                )

        else:
            self.display.v(
                "Settings are not set yet, run: ps-cli settings initialize-settings"
            )

    def _create_logger(self, default_level=None) -> Logger | None:
        """
        Create a new Logger instance with the provided settings.
        """
        if self.settings:
            log_file = self.settings.get("logger", "log_file")
            max_bytes = self.settings.get("logger", "max_bytes", 10485760)
            backup_count = self.settings.get("logger", "backup_count", 5)
            log_level = self.settings.get("logger", "log_level", "WARNING")

            # Override log_level based on default_level
            log_level = default_level or log_level

            logger = Logger(log_file, int(max_bytes), int(backup_count), log_level)
            if self.args.verbose:
                print_it("Logger initialized")
            return logger
        return None

    def _register_controllers(self) -> None:
        """
        Register all provided controllers with the App.

        This method iterates over the list of controller classes provided in the
        `__init__` method, instantiates each controller, and registers its subparsers
        with the main parser.
        """
        for controller_class in self.controllers:
            controller = controller_class()
            controller.register_subparsers(self.subparsers)
            controller.setup(self)

    def run(self) -> None:
        """
        Run the CLI application.

        This method executes the corresponding command function with the parsed
        arguments.
        """
        try:
            if not self.args.service:
                return
            self.args.func(self.args)
        except exceptions.OptionsError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"Options error: {e}")
