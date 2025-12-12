import argparse

from ps_cli.core.controllers import BaseCLIController
from ps_cli.core.decorators import command, option


class Settings(BaseCLIController):
    """
    CLI's settings management module.
    """

    def __init__(self):
        super().__init__("settings", "PS CLI settings management")

    @command
    def initialize_settings(self, args: argparse.Namespace):
        """
        Creates the default pscli-settings.ini file in the specified path
        (default to "~").

        Custom settings path can be set using PSCLI_SETTINGS_PATH environment
        variable.
        """
        self.app.settings.initialize_settings()

    @command
    def refresh_settings(self, args: argparse.Namespace):
        """
        Updates .ini file with latest structure, if some new setting has been added,
        then it would be included.
        """
        self.app.settings.refresh_settings_template()

    @command
    @option(
        "-s",
        "--section",
        help="Section name where the key is located",
        type=str,
        required=True,
    )
    @option("-k", "--key", help="Key to update", type=str, required=True)
    @option("-v", "--value", help="New value for the key", type=str, required=True)
    def update_setting(self, args: argparse.Namespace) -> None:
        """
        Update a single setting in the settings file.

        This command allows you to update the value of a specific key in a given section
        of the settings file. If the section doesn't exist, it will be created. If the
        key doesn't exist in the section, it will be added with the provided value.
        """
        self.app.settings.update_setting(args.section, args.key, args.value)
