"""User not found exception."""


class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""

    def __init__(
        self,
        message: str = "User not found.",
    ) -> None:
        super().__init__(message)
