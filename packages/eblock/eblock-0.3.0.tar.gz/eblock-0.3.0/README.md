# EBlock (Easy Block Builder)

A flexible, schema-driven library for building dynamic, context-aware
content blocks with variable substitution, nested composition,
validation, and asynchronous rendering.

Designed for use in page builders, CMS backends, or dynamic UI
generation systems where content is defined as structured JSON, rendered
with context variables, and validated via Pydantic models.

------------------------------------------------------------------------

## Installation

``` shell
pip install eblock
```

or with `uv`:

``` shell
uv add eblock
```

------------------------------------------------------------------------

## Core Concepts

### `Context`

A container for variables and metadata used during block rendering.

-   Variables are **case-normalized to uppercase**.
-   Supports deep copying for safety.
-   Allows dynamic assignment via `ctx["key"] = value`.
-   Stores:
    -   `vars`: dictionary of scalar or structured values (strings,
        numbers, lists, dicts, etc.)
    -   `extra`: arbitrary metadata (not used in substitution)

### `BaseBlock`

Abstract base class for all content blocks.

Each block: - Accepts `properties` (dict) on initialization. -
Optionally validates input/output using Pydantic models. - Recursively
resolves `{{ variable }}` placeholders from `Context`. - Supports
nesting inside dicts, lists, tuples, and sets. - Exposes an async
`build()` method returning `(result_dict, output_schema)`. - Allows
custom output transformation via `prepare_output()`.

------------------------------------------------------------------------

## Block Registration Mechanism

EBlock uses an automatic class-based registration system powered by the
`BlockMeta` metaclass.

### How It Works

Every subclass of `BaseBlock` that defines a `_type` attribute is
**automatically registered** on import.

``` python
class TextBlock(BaseBlock):
    _type = "text"
```

When Python loads this class:

-   `BlockMeta.__new__` is triggered.
-   If `_type` is not `"base"` and not private (`_SomethingBlock`), the
    block is added to the global registry.
-   Duplicate `_type` values produce a warning and are ignored.

### Accessing Registered Blocks

You can list all registered block types:

``` python
from eblock import get_registered_block_types

print(get_registered_block_types())
# ["text", "score_card", ...]
```

### Creating Blocks Dynamically

Use the factory function:

``` python
from eblock import create_block

block = create_block("text", {"content": "Hello"})
```

### Building Blocks from JSON-like Config

The library supports nested block trees:

``` python
from eblock import create_blocks_from_config

blocks = create_blocks_from_config([
    {"type": "text", "properties": {"content": "Hi"}},
    {"type": "score_card", "properties": {"title": "Test", "score": 95}},
])
```

Nested blocks inside dicts/lists are resolved recursively.

### Why Use Automatic Registration?

-   No need for manual registries.
-   Blocks register themselves as soon as they are imported.
-   Decoupled plugins/modules can define their own block types.
-   Ensures consistency when building from JSON configs.

------------------------------------------------------------------------

## Features

✅ **Variable substitution**\
Placeholders like `{{ user_name }}` are replaced with values from
context.

✅ **Recursive structure support**\
Handles dicts, lists, tuples, sets, and nested `BaseBlock` instances.

✅ **Input/Output validation**\
Define `_input_schema` and `_output_schema` using Pydantic models.

✅ **Computed fields**\
Override `prepare_output()` to modify or add fields before output
validation.

✅ **Static dependency analysis**\
Use `.get_vars()` to extract all required variables, including in nested
blocks.

✅ **Async-first design**\
Full `async/await` support throughout the rendering pipeline.

✅ **Structured logging**\
Blocks and context instances log operations through hierarchical
loggers.

------------------------------------------------------------------------

## Usage Examples

### Basic Block

``` python
from eblock import BaseBlock, Context

class TextBlock(BaseBlock):
    _type = "text"

ctx = Context(vars={"name": "Alice"})
block = TextBlock({"content": "Hello, {{ name }}!"})
result, _ = await block.build(ctx)
# result == {"content": "Hello, Alice!"}
```

### Validated Block with Computed Output

``` python
from pydantic import BaseModel
from eblock import BaseBlock

class Input(BaseModel):
    title: str
    score: int

class Output(BaseModel):
    title: str
    score: int
    badge: str

class ScoreCard(BaseBlock):
    _type = "score_card"
    _input_schema = Input
    _output_schema = Output

    async def prepare_output(self, result, ctx):
        result["badge"] = "🏆" if result["score"] >= 90 else "📝"
        return result
```

### Nested Blocks

``` python
header = TextBlock({"text": "Welcome, {{ user }}!"})
page = PageBlock({"header": header, "theme": "{{ theme }}"})
# Both variables will be resolved from context
```

### Variable Inspection

``` python
block = TextBlock({"msg": "Hi {{ first }}, {{ last }}!"})
print(block.get_vars())  # {"FIRST", "LAST"}
```

------------------------------------------------------------------------

## API Reference

### `class Context`

-   `__init__(self, vars: dict | None = None, **extra)`
-   `__getitem__(key)`
-   `__setitem__(key, value)`
-   Properties:
    -   `vars` --- deep copy of stored variables\
    -   `extra` --- shallow copy of extra data

### `class BaseBlock`

-   `__init__(self, properties: dict)`
-   `async build(self, ctx: Context) -> tuple[dict, Type[BaseModel] | None]`
-   `async prepare_output(self, result: dict, ctx: Context) -> dict`
-   `get_vars(self) -> set[str]`
-   Property: `type` --- block identifier

### Define in subclasses

-   `_type: str` --- identifier (required)
-   `_input_schema: Type[BaseModel] | None`
-   `_output_schema: Type[BaseModel] | None`

### Registry Helpers

-   `create_block(type, properties)`
-   `create_blocks_from_config(config)`
-   `get_registered_block_types()`

------------------------------------------------------------------------

## Requirements

-   Python ≥ 3.10
-   Pydantic ≥ 2.0

------------------------------------------------------------------------

## Notes

-   Placeholders must use double curly braces: `{{ var_name }}`.
-   Whitespace is trimmed: `{{   user  }}` → `user`.
-   Missing variables resolve to empty string and produce a warning.
-   Blocks should be treated as stateless and recreated when reused.