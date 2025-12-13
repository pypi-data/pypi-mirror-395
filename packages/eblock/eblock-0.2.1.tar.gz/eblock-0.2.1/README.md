# EBlock (Easy Block Builder)

A flexible, schema-driven library for building dynamic, context-aware content blocks with variable substitution, nested composition, validation, and asynchronous rendering.

Designed for use in page builders, CMS backends, or dynamic UI generation systems where content is defined as structured JSON, rendered with context variables, and validated via Pydantic models.

---

## Installation

```shell
pip install eblock
```

or with `uv`:

```shell
uv add eblock
```

---

## Core Concepts

### `Context`
A container for variables and metadata used during block rendering.

- Variables are **case-normalized to uppercase**.
- Supports deep copying for safety.
- Allows dynamic assignment via `ctx["key"] = value`.
- Stores:
  - `vars`: dictionary of scalar or structured values (strings, numbers, lists, dicts, etc.)
  - `extra`: arbitrary metadata (not used in substitution)

### `BaseBlock`
Abstract base class for all content blocks.

Each block:
- Accepts `properties` (dict) on initialization.
- Optionally validates input/output using Pydantic models.
- Recursively resolves `{{ variable }}` placeholders from `Context`.
- Supports nesting (blocks inside dicts, lists, etc.).
- Exposes a standardized async `build()` method.
- Allows custom output transformation via `prepare_output()`.

---

## Features

✅ **Variable substitution**  
Placeholders like `{{ user_name }}` are replaced with values from context.

✅ **Recursive structure support**  
Handles dicts, lists, tuples, sets, and nested `BaseBlock` instances.

✅ **Input/Output validation**  
Define `_input_schema` and `_output_schema` using Pydantic models.

✅ **Computed fields**  
Override `prepare_output()` to add or transform fields after substitution but before output validation.

✅ **Static dependency analysis**  
Use `.get_vars()` to extract all required variables from a block (including nested ones).

✅ **Async-first design**  
Full async/await support for future extensibility (e.g., async data fetching in `prepare_output`).

✅ **Structured logging**  
Each block and context instance logs actions with a unique hierarchical logger name.

---

## Usage Examples

### Basic Block
```python
from easy_block_builder import BaseBlock, Context

class TextBlock(BaseBlock):
    _type = "text"

ctx = Context(vars={"name": "Alice"})
block = TextBlock({"content": "Hello, {{ name }}!"})
result, _ = await block.build(ctx)
# result = {"content": "Hello, Alice!"}
```

### Validated Block with Computed Output
```python
from pydantic import BaseModel
from easy_block_builder import BaseBlock

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
```python
header = TextBlock({"text": "Welcome, {{ user }}!"})
page = PageBlock({"header": header, "theme": "{{ theme }}"})
# Both `user` and `theme` will be resolved from context
```

### Variable Inspection
```python
block = TextBlock({"msg": "Hi {{ first }}, {{ last }}!"})
print(block.get_vars())  # {"first", "last"}
```

---

## API Reference

### `class Context`
- `__init__(self, vars: dict | None = None, **extra)`
- `__getitem__(key)`, `__setitem__(key, value)`
- Properties: `vars` (deep copy), `extra` (shallow copy)

### `class BaseBlock`
- `__init__(self, properties: dict)`
- `async build(self, ctx: Context) -> tuple[dict, Type[BaseModel] | None]`
- `async prepare_output(self, result: dict, ctx: Context) -> dict` *(override to customize)*
- `get_vars(self) -> set[str]`
- Properties: `type` (read-only)

### Class-level attributes (define in subclass)
- `_type: str` — block identifier (e.g., `"image"`, `"form"`)
- `_input_schema: Type[BaseModel] | None`
- `_output_schema: Type[BaseModel] | None`

---

## Requirements

- Python ≥ 3.10
- Pydantic ≥ 2.0

---

## Notes

- All string placeholders must use double curly braces: `{{ var_name }}`.
- Whitespace inside placeholders is stripped: `{{  user_id  }}` → `user_id`.
- If a variable is missing in context, it resolves to `None` and logs a warning.
- Blocks are **not reusable** across different `build()` calls if they hold mutable state — design them as stateless.
