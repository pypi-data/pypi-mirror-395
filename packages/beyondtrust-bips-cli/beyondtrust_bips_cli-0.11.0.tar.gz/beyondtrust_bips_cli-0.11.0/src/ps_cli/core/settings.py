import os
from configparser import ConfigParser
from typing import Any, Optional

from ps_cli.core.display import print_it


class SettingsManager:
    def __init__(self, settings_path: Optional[str] = None) -> None:
        self.default_ini_file = "pscli-settings.ini"
        self.templates_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "templates"
        )

        self.settings_path = settings_path or self.get_settings_path()
        self.parser = ConfigParser()
        self._load_settings()

    def get_settings_path(self) -> str:
        env_path = os.environ.get("PSCLI_SETTINGS_PATH")
        if env_path:
            return env_path
        return os.path.join(os.path.expanduser("~"), self.default_ini_file)

    def _load_settings(self) -> None:
        if os.path.exists(self.settings_path):
            self.parser.read(self.settings_path)

    def get(self, section: str, option: str, default: Optional[Any] = None) -> Any:
        """
        Return a setting for the given section and option name.
        Validates the section and option exist before returning the setting value.
        """
        if self.parser.has_section(section) and self.parser.has_option(section, option):
            return self.parser.get(section, option)
        return default

    def initialize_settings(self, file_name: str = "") -> None:
        """
        Create a new settings file based on a template.

        This method creates a new settings file at the specified path
        (`self.settings_path`) using the contents of a template file
        (`pscli-settings.ini`). If the settings file already exists, it will print a
        message indicating that the file already exists.

        If the template file is not found, it will print a message indicating that the
        template file was not found.
        """
        file_name = file_name or self.default_ini_file
        template_path = os.path.join(self.templates_path, file_name)
        if not os.path.exists(self.settings_path):
            if os.path.exists(template_path):
                with open(template_path, "r") as f:
                    template_content = f.read()
                with open(self.settings_path, "w") as f:
                    f.write(template_content)
                print_it(f"Settings file created at {self.settings_path}")
            else:
                print_it(f"Template file not found {template_path}")
        else:
            print_it(f"Settings file already exists at {self.settings_path}")

    def refresh_settings_template(self) -> None:
        """
        Update the settings file with missing settings from a template.

        This method updates the existing settings file (`self.settings_path`) with any
        missing sections or options from a template file (`pscli-settings.ini`). It
        reads the template file, compares it with the existing settings file, and adds
        any missing sections or options to the settings file without modifying existing
        settings.

        If the template file is not found, it will print a message indicating that the
        template file was not found.
        """
        template_path = os.path.join(self.templates_path, self.default_ini_file)
        if os.path.exists(template_path):
            template_config = ConfigParser()
            template_config.read(template_path)

            for section in template_config.sections():
                if not self.parser.has_section(section):
                    print_it(f"Adding section {section}")
                    self.parser.add_section(section)

                for option in template_config.options(section):
                    if not self.parser.has_option(section, option):
                        print_it(f"Adding to {section} section: {option}")
                        self.parser.set(
                            section, option, template_config.get(section, option)
                        )

            with open(self.settings_path, "w") as f:
                self.parser.write(f)

            print_it(
                "Settings file updated with missing settings from "
                f"template at {self.settings_path}"
            )
        else:
            print_it(f"Template file not found {template_path}")

    def update_setting(self, section: str, option: str, value: str) -> None:
        """
        Update a single setting in the settings file.

        This method updates the value of a specific key in a given section of the
        settings file. If the section doesn't exist, it will be created. If the
        key doesn't exist in the section, it will be added with the provided value.

        Args:
            section (str): The name of the section where the key is located.
            option (str): The name of the key to update.
            value (str): The new value for the specified key.
        """
        if not self.parser.has_section(section):
            self.parser.add_section(section)

        self.parser.set(section, option, value)

        try:
            with open(self.settings_path, "w") as f:
                self.parser.write(f)
        except PermissionError as e:
            print_it(f"It was not possible to update settings: {e}")
        else:
            print_it(f"Setting '{option}' in section '{section}' updated to '{value}'")
