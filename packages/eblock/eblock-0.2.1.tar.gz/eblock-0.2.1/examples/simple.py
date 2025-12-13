from easy_block_builder import BaseBlock, Context


class TextBlock(BaseBlock):
    _type = "text"
    # без _input_schema и _output_schema — используем "сырые" свойства


# Пример использования
async def example_simple():
    ctx = Context(vars={"user_name": "Alice", "age": 30})
    block = TextBlock(
        {
            "title": "Hello, {{ user_name }}!",
            "description": "You are {{ age }} years old.",
        }
    )

    result, _ = await block.build(ctx)
    print(result)
    # {'title': 'Hello, Alice!', 'description': 'You are 30 years old.'}


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_simple())
