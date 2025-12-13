from pydantic import BaseModel
from easy_block_builder import BaseBlock, Context


class ProductInput(BaseModel):
    name: str
    price_usd: float


class ProductOutput(BaseModel):
    name: str
    price_usd: float
    price_rub: float
    formatted_price: str


class ProductBlock(BaseBlock):
    _type = "product"
    _input_schema = ProductInput
    _output_schema = ProductOutput

    async def prepare_output(self, result: dict, ctx: Context) -> dict:
        usd = result["price_usd"]
        rate = ctx["USD_TO_RUB"] or 90.0  # fallback
        rub = round(usd * rate, 2)
        result["price_rub"] = rub
        result["formatted_price"] = f"{rub:,.2f} ₽"
        return result


async def example_product():
    ctx = Context(vars={"USD_TO_RUB": 88.5})
    block = ProductBlock({"name": "Wireless Headphones", "price_usd": 99.99})
    res, _ = await block.build(ctx)
    print(res["formatted_price"])  # "8,849.12 ₽"


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_product())
