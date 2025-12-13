from pydantic import BaseModel
from easy_block_builder import BaseBlock


class ImageBlockInput(BaseModel):
    src: str
    alt: str = ""


class ImageBlockOutput(BaseModel):
    url: str
    caption: str


class ImageBlock(BaseBlock):
    _type = "image"
    _input_schema = ImageBlockInput
    _output_schema = ImageBlockOutput

    async def prepare_output(self, result: dict, ctx) -> dict:
        return {"url": result["src"], "caption": result["alt"]}
