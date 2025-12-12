from logging import getLogger, Logger
from .ctx import Context
import re
from typing import Type
from pydantic import BaseModel, ValidationError


_VARS_PATTERN = re.compile(r"{{\s*(.*?)\s*}}")


class BaseBlock:
    _type: str = "base"
    _props: dict[str, object]
    _input_schema: Type[BaseModel] | None = None
    _output_schema: Type[BaseModel] | None = None

    _logger: Logger

    __slots__ = ("_props", "_logger")

    def __init__(self, properties: dict[str, object]) -> None:
        self._logger = getLogger(f"{__name__}.{self.__class__.__name__}")

        # Validate properties against input schema if defined
        if self._input_schema is not None:
            try:
                validated = self._input_schema(**properties)
                self._props = validated.model_dump()
                self._logger.debug(
                    f"Validated properties against schema {self._input_schema.__name__}"
                )
            except ValidationError as e:
                self._logger.error(f"Validation error for properties: {e}")
                raise
        else:
            self._props = properties

        self._logger.debug(
            f"Initialized block of type: {self._type} with properties: {self._props}"
        )

    async def build(
        self, ctx: Context
    ) -> tuple[dict[str, object], Type[BaseModel] | None]:
        """Build the block by replacing variables with their values from context.

        Args:
            ctx: Context object containing variables to substitute

        Returns:
            Tuple of (built properties dictionary, output schema if defined)
        """

        async def _build_value(val):
            """Recursively build values by replacing variables."""
            if isinstance(val, BaseBlock):
                built_data, _ = await val.build(ctx)
                return built_data
            elif isinstance(val, str):

                def replace_var(match):
                    var_name = match.group(1).strip()
                    value = ctx[var_name]
                    if value is None:
                        self._logger.warning(
                            f"Variable '{var_name}' not found in context: {ctx.vars}"
                        )
                    return str(value)

                return _VARS_PATTERN.sub(replace_var, val)
            elif isinstance(val, dict):
                return {k: await _build_value(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [await _build_value(item) for item in val]
            elif isinstance(val, tuple):
                return tuple(await _build_value(item) for item in val)
            elif isinstance(val, set):
                return {await _build_value(item) for item in val}
            else:
                return val

        result = {key: await _build_value(value) for key, value in self._props.items()}

        # Prepare output by adding computed fields and modifications
        result = await self.prepare_output(result, ctx)

        # Validate result against output schema if defined
        if self._output_schema is not None:
            try:
                validated = self._output_schema(**result)
                result = validated.model_dump()
                self._logger.debug(
                    f"Validated output against schema {self._output_schema.__name__}"
                )
            except ValidationError as e:
                self._logger.error(f"Output validation error: {e}")
                raise

        self._logger.debug(f"Built block of type {self._type}: {result}")
        return result, self._output_schema

    async def prepare_output(
        self, result: dict[str, object], ctx: Context
    ) -> dict[str, object]:
        """Prepare output by adding computed fields or modifying existing ones.

        This method is called after variable substitution but before output schema validation.
        Use it to add fields that exist in output schema but not in input schema, or to modify
        values based on context and other fields.

        Args:
            result: The built result dictionary
            ctx: The context object for accessing variables

        Returns:
            Modified result dictionary with computed fields added
        """
        self._logger.debug(f"Preparing output for block of type {self._type}")
        return result

    @property
    def type(self) -> str:
        return self._type

    def get_vars(self) -> set[str]:
        """Collect all variables used in this block and nested blocks."""
        vars_set = set()

        def _collect(val):
            if isinstance(val, BaseBlock):
                vars_set.update(val.get_vars())
            elif isinstance(val, str):
                for match in _VARS_PATTERN.findall(val):
                    if match.strip():
                        vars_set.add(match.strip())
            elif isinstance(val, dict):
                for v in val.values():
                    _collect(v)
            elif isinstance(val, (list, tuple, set)):
                for item in val:
                    _collect(item)

        for value in self._props.values():
            _collect(value)

        self._logger.debug(f"Collected variables: {vars_set}")
        return vars_set
