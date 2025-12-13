# trellis/exceptions.py


class TrellisError(Exception):
    """Base exception for all trellis-related errors."""


class ProcessNotFound(TrellisError):
    """Raised when a process cannot be found for a given key."""


class StepNotFound(TrellisError):
    """Raised when a step name is not defined for a process."""
