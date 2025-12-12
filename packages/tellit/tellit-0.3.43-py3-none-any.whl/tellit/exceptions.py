# Custom and Clear Exceptions for Tellit


class BaseTellitException(Exception):
    """Base Exception to be Inheritied"""


class UnsupportedPlatform(BaseTellitException):
    """Unsupported Platform, notify-py might not work as expected"""

    def __init__(self, platform):
        self.platform = platform

    def __repr__(self):
        return f"{self.platform} is not supported."

    def __str__(self):
        return f"{self.platform} is not supported."


class InvalidAudioPath(BaseTellitException):
    """Audio path provided is invalid."""

    def __repr__(self):
        return f"Unable to find audio path. Please check if it exists."

    def __str__(self):
        return f"Unable to find audio path. Please check if it exists."


class InvalidAudioFormat(BaseTellitException):
    """The custom audio provided is not a supported file"""

    def __repr__(self):
        return f"Only .wav files are supported."

    def __str__(self):
        return f"Only .wav files are supported."


class InvalidIconPath(BaseTellitException):
    """Icon Path Provided is Invalid"""

    def __repr__(self):
        return f"Unable to find icon path. Please check if it exists."

    def __str__(self):
        return f"Unable to find icon path. Please check if it exists."


class NotificationFailure(BaseTellitException):
    """Overall function failed"""

    pass


class BinaryNotFound(BaseTellitException):
    """ " A specified binary requirement was not found"""

    def __init__(self, binary):
        self.binary = binary

    def __repr__(self):
        return f"Unable find required {self.binary}. Please check if it's installed."

    def __str__(self):
        return f"Unable to find required {self.binary}. Please check if it's installed."


class InvalidMacOSNotificator(BaseTellitException):
    """The provided notificator is invalid."""

    def __str__(self):
        return f"The provided notificator is invalid. Please read the documentation for more information."

    def __repr__(self):
        return f"The provided notificator is invalid. Please read the documentation for more information."


class LinuxDbusException(Exception):
    """This error is raised when a connection with dbus is interrupted or is unable to be established"""

    pass
