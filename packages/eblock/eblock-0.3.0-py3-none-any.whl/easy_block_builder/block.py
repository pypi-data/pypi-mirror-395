from logging import getLogger, Logger
from .ctx import Context

import re
from typing import Type, Any, Set, Tuple, Dict, Optional
from pydantic import BaseModel, ValidationError

_VARS_PATTERN = re.compile(r"{{\s*(.*?)\s*}}")
"""Regex pattern for detecting variables in double-curly-brace format (e.g., {{ var_name }})"""


class BlockMeta(type):
    """A metaclass for automatic block registration."""

    _registry: Dict[str, Type["BaseBlock"]] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        # Skipping the base class and inner classes
        if name == "BaseBlock" or name.startswith("_"):
            return cls

        # Checking that the class has the _type attribute.
        if hasattr(cls, "_type") and cls._type != "base":
            block_type = cls._type

            if block_type in mcs._registry:
                existing_cls = mcs._registry[block_type]
                getLogger(__name__).warning(
                    "Block type '%s' already registered to %s. Skipping registration of %s.",
                    block_type,
                    existing_cls.__name__,
                    cls.__name__,
                )
            else:
                mcs._registry[block_type] = cls
                getLogger(__name__).info(
                    "Auto-registered block type '%s' to class %s",
                    block_type,
                    cls.__name__,
                )

        return cls

    @classmethod
    def get_registry(mcs) -> Dict[str, Type["BaseBlock"]]:
        return mcs._registry


class BaseBlock(metaclass=BlockMeta):
    """Base class for all building blocks in the processing pipeline.

    Each block type should subclass this and implement:
    - `_type`: Unique identifier for the block type
    - Optional input/output schemas using Pydantic models
    - Optional `prepare_output()` for post-processing
    """

    _type: str = "base"
    """Unique identifier for the block type (must be overridden in subclasses)"""

    _props: Dict[str, Any]
    """Properties dictionary containing block configuration"""

    _input_schema: Optional[Type[BaseModel]] = None
    """Optional Pydantic schema for validating input properties"""

    _output_schema: Optional[Type[BaseModel]] = None
    """Optional Pydantic schema for validating final output"""

    _logger: Logger
    """Logger instance specific to this block type"""

    __slots__ = ("_props", "_logger")

    def __init__(self, properties: Dict[str, Any]) -> None:
        """Initialize the block with properties and validation.

        Args:
            properties: Configuration dictionary for the block

        Raises:
            ValidationError: If input schema exists and properties fail validation
        """
        self._logger = getLogger(f"{__name__}.{self.__class__.__name__}")

        # Validate properties against input schema if defined
        if self._input_schema is not None:
            try:
                validated = self._input_schema(**properties)
                self._props = validated.model_dump()
                self._logger.debug(
                    "Validated properties against schema %s",
                    self._input_schema.__name__,
                )
            except ValidationError as e:
                self._logger.error("Validation error for properties: %s", e)
                raise
        else:
            self._props = properties

        self._logger.debug(
            "Initialized %s block with properties: %s", self._type, self._props
        )

    async def build(
        self, ctx: Context
    ) -> Tuple[Dict[str, Any], Optional[Type[BaseModel]]]:
        """Build the block by resolving variables and nested blocks using context.

        Performs these operations:
        1. Recursively resolves variables in string values ({{ var }})
        2. Recursively builds nested BaseBlock objects
        3. Calls prepare_output() for custom post-processing
        4. Validates final output against output schema if defined

        Args:
            ctx: Context containing variables and runtime state

        Returns:
            Tuple containing:
            - Fully resolved properties dictionary
            - Output schema type (if defined) or None

        Raises:
            ValidationError: If output schema exists and built result fails validation
        """

        async def _build_value(val: Any) -> Any:
            """Recursively resolve values in properties.

            Handles:
            - Nested BaseBlock objects (builds them recursively)
            - Strings with variables (replaces {{ var }} patterns)
            - Collections (dicts, lists, tuples, sets)
            """
            if isinstance(val, BaseBlock):
                built_data, _ = await val.build(ctx)
                return built_data
            elif isinstance(val, str):

                def replace_var(match: re.Match) -> str:
                    """Replacement function for variable substitution."""
                    var_name = match.group(1).strip()
                    value = ctx[var_name]
                    if value is None:
                        self._logger.warning(
                            "Variable '%s' not found in context (available: %s)",
                            var_name,
                            list(ctx.vars.keys()),
                        )
                    return str(value) if value is not None else ""

                return _VARS_PATTERN.sub(replace_var, val)
            elif isinstance(val, dict):
                return {k: await _build_value(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [await _build_value(item) for item in val]
            elif isinstance(val, tuple):
                return tuple(await _build_value(item) for item in val)
            elif isinstance(val, set):
                return {await _build_value(item) for item in val}
            return val

        # Build all property values
        result = {key: await _build_value(value) for key, value in self._props.items()}

        # Custom post-processing hook
        result = await self.prepare_output(result, ctx)

        # Validate against output schema
        if self._output_schema is not None:
            try:
                validated = self._output_schema(**result)
                result = validated.model_dump()
                self._logger.debug(
                    "Validated output against schema %s", self._output_schema.__name__
                )
            except ValidationError as e:
                self._logger.error("Output validation error: %s", e)
                raise

        self._logger.debug("Built %s block: %s", self._type, result)
        return result, self._output_schema

    async def prepare_output(
        self, result: Dict[str, Any], ctx: Context
    ) -> Dict[str, Any]:
        """Customize output before schema validation (override in subclasses).

        This method is called after variable substitution but before output validation.
        Use cases include:
        - Adding computed fields not present in input
        - Modifying values based on context state
        - Transforming data structures for output schema compatibility

        Default implementation returns unmodified result.

        Args:
            result: Dictionary of built properties
            ctx: Current context object

        Returns:
            Modified properties dictionary
        """
        self._logger.debug("Preparing output for %s block", self._type)
        return result

    @property
    def type(self) -> str:
        """Get the block type identifier."""
        return self._type

    def get_vars(self) -> Set[str]:
        """Collect all variable references used in this block and nested blocks.

        Scans all string values for {{ var }} patterns and recursively collects
        variables from nested blocks.

        Returns:
            Set of normalized variable names (uppercase)
        """
        vars_set: Set[str] = set()

        def _collect(val: Any) -> None:
            """Recursive helper to collect variables from values."""
            if isinstance(val, BaseBlock):
                vars_set.update(val.get_vars())
            elif isinstance(val, str):
                for match in _VARS_PATTERN.findall(val):
                    normalized = match.strip().upper()
                    if normalized:
                        vars_set.add(normalized)
            elif isinstance(val, dict):
                for v in val.values():
                    _collect(v)
            elif isinstance(val, (list, tuple, set)):
                for item in val:
                    _collect(item)

        for value in self._props.values():
            _collect(value)

        self._logger.debug("Collected variables for %s block: %s", self._type, vars_set)
        return vars_set
