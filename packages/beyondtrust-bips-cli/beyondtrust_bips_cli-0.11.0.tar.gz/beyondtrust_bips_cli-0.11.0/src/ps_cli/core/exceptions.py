class InvalidSettingsPathException(Exception):
    """
    Raised when provided settings path doesn't exist.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidAuthenticationException(Exception):
    """
    Raised when an error happened when trying to authenticate to the API.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidLogLevelException(Exception):
    """
    Raised when trying to initialize Logger using an invalid log level.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidFormatException(Exception):
    """
    Raised when trying to print/display some data with an invalid format.
    Valid formats are present in Format class.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
