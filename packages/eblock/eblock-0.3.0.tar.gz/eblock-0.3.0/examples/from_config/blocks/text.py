from pydantic import BaseModel
from easy_block_builder import BaseBlock


class TextBlockInput(BaseModel):
    content: str
    style: str = "normal"


class TextBlockOutput(BaseModel):
    rendered: str


class TextBlock(BaseBlock):
    _type = "text"
    _input_schema = TextBlockInput
    _output_schema = TextBlockOutput

    async def prepare_output(self, result: dict, ctx) -> dict:
        content = result["content"]
        style = result["style"]
        rendered = f"<p class='{style}'>{content}</p>"
        return {"rendered": rendered}
