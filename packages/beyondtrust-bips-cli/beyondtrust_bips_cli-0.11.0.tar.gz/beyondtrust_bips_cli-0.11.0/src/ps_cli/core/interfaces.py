import argparse
from abc import ABC, abstractmethod
from typing import Any, Callable

from ps_cli.core.display import Display
from ps_cli.core.logger import Logger
from ps_cli.core.settings import SettingsManager


class AppInterface(ABC):
    """
    Abstract base class defining the interface for the CLI App.
    """

    @property
    @abstractmethod
    def settings(self) -> SettingsManager:
        pass

    @abstractmethod
    def _register_controllers(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass


class ControllerInterface(ABC):
    """
    Abstract base class defining the interface for a Controller.

    This interface defines the methods that a Controller implementation must provide,
    including registering commands, subcommands, and subparsers.
    """

    @property
    @abstractmethod
    def log(self) -> Logger:
        pass

    @property
    @abstractmethod
    def display(self) -> Display:
        pass

    @abstractmethod
    def register_commands(self) -> None:
        pass

    @abstractmethod
    def register_subcommand(self, func: Callable) -> None:
        pass

    @abstractmethod
    def register_subparsers(self, subparsers: argparse._SubParsersAction) -> None:
        pass

    @abstractmethod
    def setup(self, app: AppInterface) -> None:
        pass


class ClassObjectInterface(ABC):
    """
    Abstract base class that includes a class_object property.

    This enforces a lazy loading behavior to avoid loading the CLI app with class
    instances that are not required.

    Example of implementation:
    The class_object property should return an object from corresponding Python Library
    class.
    >>> @property
    >>> def class_object(self) -> secrets_safe.SecretsSafe:
    >>>     if self._class_object is None and self.app is not None:
    >>>         self._class_object = secrets_safe.SecretsSafe(
    >>>             authentication=self.app.authentication
    >>>         )
    >>>     return self._class_object
    """

    @property
    @abstractmethod
    def class_object(self) -> Any | None:
        pass
