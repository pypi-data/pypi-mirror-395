from typing import Any, Dict, Optional
from logging import getLogger
from copy import copy, deepcopy


VARS_TYPE = Dict[str, Any]
"""Type for context variables dictionary (supports any JSON-serializable types)"""

EXTRA_TYPE = Dict[str, Any]
"""Type for extra context parameters (arbitrary objects)"""


class Context:
    """Runtime context for variable substitution and state management.

    Manages:
    - Variable storage with case-insensitive access
    - Extra parameters passed to blocks
    - Logging for variable access

    Variables are normalized to uppercase keys for case-insensitive access.
    """

    __slots__ = ("_vars", "_extra", "_logger")

    def __init__(self, vars: Optional[VARS_TYPE] = None, **extra: Any) -> None:
        """Initialize context with variables and extra parameters.

        Args:
            vars: Dictionary of initial variables (keys will be normalized to uppercase)
            **extra: Additional context parameters stored as-is
        """
        self._logger = getLogger(f"{__name__}.{self.__class__.__name__}")

        # Normalize variable keys to uppercase
        self._vars = {
            self._normalize_key(key): deepcopy(value)
            for key, value in (vars or {}).items()
        }
        self._extra = extra

        self._logger.debug(
            "Initialized context with variables: %s", list(self._vars.keys())
        )

    @property
    def vars(self) -> VARS_TYPE:
        """Get a deep copy of all stored variables (read-only view)."""
        return deepcopy(self._vars)

    @property
    def extra(self) -> EXTRA_TYPE:
        """Get a shallow copy of extra parameters."""
        return copy(self._extra)

    @staticmethod
    def _normalize_key(key: str) -> str:
        """Normalize variable key to uppercase for case-insensitive access."""
        return key.upper()

    def __setitem__(self, key: str, value: Any) -> None:
        """Store a variable with case-insensitive key.

        Args:
            key: Variable name (will be normalized to uppercase)
            value: Value to store (deep copied)
        """
        norm_key = self._normalize_key(key)
        self._vars[norm_key] = deepcopy(value)
        self._logger.debug(
            "Set context variable '%s' = %r (type: %s)",
            norm_key,
            value,
            type(value).__name__,
        )

    def __getitem__(self, key: str) -> Any:
        """Retrieve a variable with case-insensitive key.

        Args:
            key: Variable name to retrieve (case-insensitive)

        Returns:
            Variable value or None if not found
        """
        norm_key = self._normalize_key(key)
        value = self._vars.get(norm_key)
        self._logger.debug(
            "Accessed context variable '%s' = %r (type: %s)",
            norm_key,
            value,
            type(value).__name__ if value is not None else "None",
        )
        return value
