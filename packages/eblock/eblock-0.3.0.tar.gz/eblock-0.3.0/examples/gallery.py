from easy_block_builder import BaseBlock, Context


class ImageBlock(BaseBlock):
    _type = "image"


class GalleryBlock(BaseBlock):
    _type = "gallery"

    async def prepare_output(self, result: dict, ctx: Context) -> dict:
        # Ничего не делаем — всё уже обработано рекурсивно
        return result


async def example_gallery():
    ctx = Context(vars={"user_id": "789"})

    images = [
        ImageBlock({"src": "/img/{{ user_id }}/1.jpg", "alt": "Photo 1"}),
        ImageBlock({"src": "/img/{{ user_id }}/2.jpg", "alt": "Photo 2"}),
    ]

    gallery = GalleryBlock({"items": images, "title": "Your Photos"})

    result, _ = await gallery.build(ctx)
    print(result)  # "/img/789/1.jpg"


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_gallery())
