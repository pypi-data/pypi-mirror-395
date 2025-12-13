from pydantic import BaseModel, Field
from typing import Optional
from easy_block_builder import BaseBlock, Context


class UserInput(BaseModel):
    name: str
    age: int = Field(ge=0)
    city: Optional[str] = None


class UserOutput(BaseModel):
    display_name: str
    profile_summary: str
    is_adult: bool


class UserCardBlock(BaseBlock):
    _type = "user_card"
    _input_schema = UserInput
    _output_schema = UserOutput

    async def prepare_output(self, result: dict, ctx: Context) -> dict:
        # Добавляем вычисляемые поля
        name = result["name"]
        age = result["age"]
        city = result.get("city") or "Unknown"

        result["display_name"] = f"👤 {name}"
        result["profile_summary"] = f"{name}, {age} y.o., from {city}"
        result["is_adult"] = age >= 18

        return result


# Пример использования
async def example_with_schema():
    ctx = Context(vars={"default_city": "Berlin"})

    # Входные данные содержат переменную
    block = UserCardBlock(
        {"name": "{{ visitor_name }}", "age": 25, "city": "{{ default_city }}"}
    )

    ctx["visitor_name"] = "Bob"  # Можно задавать и после создания контекста

    result, _ = await block.build(ctx)
    print(result)
    # {
    #   'name': 'Bob',
    #   'age': 25,
    #   'city': 'Berlin',
    #   'display_name': '👤 Bob',
    #   'profile_summary': 'Bob, 25 y.o., from Berlin',
    #   'is_adult': True
    # }


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_with_schema())
