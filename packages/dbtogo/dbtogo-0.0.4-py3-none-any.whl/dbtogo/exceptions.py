class NoBindError(Exception):
    def __init__(self) -> None:
        super().__init__("You need to bind this model to a db before first use")


class UnboundDeleteError(Exception):
    def __init__(self) -> None:
        super().__init__("You cannot delete an object that is not in the db")


class DestructiveMigrationError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "This migration includes destructive actions,"
            "but wasnt executed with force=True"
        )


class InvalidMigrationError(Exception):
    def __init__(self) -> None:
        super().__init__("This migration is not valid")
