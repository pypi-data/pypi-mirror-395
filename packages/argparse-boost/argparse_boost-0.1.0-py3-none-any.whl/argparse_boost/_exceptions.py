class CliSetupError(Exception):
    """Error during CLI setup."""


class FieldNameConflictError(CliSetupError):
    """Raised when flattened dataclass field names collide."""


class UnsupportedFieldTypeError(CliSetupError):
    """Raised when dataclass fields use unsupported types."""
