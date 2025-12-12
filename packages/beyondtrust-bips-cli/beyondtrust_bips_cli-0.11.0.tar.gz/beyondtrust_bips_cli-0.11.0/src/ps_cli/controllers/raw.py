import argparse
import json

from ps_cli.core.constants.formats import Format
from ps_cli.core.controllers import BaseCLIController
from ps_cli.core.decorators import command
from ps_cli.core.display import print_it


class RawRequest(BaseCLIController):
    """
    Run raw HTTP requests into the API.

    https://docs.beyondtrust.com/bips/docs/api

    Usage:
        ps-cli raw <HTTP_VERB> <ENDPOINT> [JSON_PAYLOAD]

    JSON response will be printed if available.
    """

    def __init__(self):
        super().__init__(name="raw", help="Send raw HTTP requests to the API.")

    def register_commands(self):
        self.register_subcommand(self.request)

    @command
    def request(self, args):
        """
        Send a raw HTTP request to the API endpoint.
        """
        self.display.v("Starting raw command")
        verb = args.verb.upper()
        endpoint = args.endpoint
        payload = args.payload
        headers = {"Content-Type": "application/json"}

        data = self._validate_payload(payload)
        if data is None and payload:
            return

        session = self._get_session()
        if session is None:
            return

        url = f"{self.app.authentication._api_url}/{endpoint}"
        self.log.info(f"Sending {verb} request to {url}")
        self.display.v(
            f"Sending {verb} request to {url} with payload: {data}", save_log=False
        )
        response = session.request(verb, url, json=data, headers=headers)
        self._handle_response(response)
        self.log.info("Raw command finished")

    def _validate_payload(self, payload):
        if not payload:
            return None
        try:
            return json.loads(payload)
        except json.JSONDecodeError as e:
            print_it(f"Invalid JSON payload: {e}")
            return None

    def _get_session(self):
        if not self.app or not self.app.authentication:
            print_it("Authentication is not initialized.")
            return None
        return self.app.authentication._req

    def _handle_response(self, response):
        if response.status_code in [200, 201, 204]:
            if response.content:
                try:
                    json_response = response.json()
                    self.display.show(json_response, format=Format.JSON.value)
                except json.JSONDecodeError:
                    print_it("Response is not valid JSON:")
                    print_it(response.text)
            else:
                print_it("Request ran successfully, but no content in response.")
        else:
            print_it(f"Status: {response.status_code}")
            print_it(f"Response: {response.text}")
            self.log.error(f"Error: {response.status_code} - {response.text}")

    def register_subparsers(self, subparsers: argparse._SubParsersAction) -> None:
        parser = subparsers.add_parser(
            self.name,
            help=self.help,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self.__doc__,
        )
        parser.add_argument(
            "verb",
            type=str,
            choices=["GET", "POST", "PUT", "DELETE"],
            help="HTTP verb to use (GET, POST, PUT, DELETE)",
        )
        parser.add_argument(
            "endpoint",
            type=str,
            help="API endpoint to call (e.g., Secrets-Safe/Folders/)",
        )
        parser.add_argument(
            "payload",
            type=str,
            nargs="?",
            default=None,
            help="""Optional JSON payload (e.g.: '{"key": "value"}')""",
        )
        parser.set_defaults(func=self.request)
