from typing import List
from pydantic import BaseModel, ConfigDict
from easy_block_builder import BaseBlock


class SectionBlockInput(BaseModel):
    title: str
    children: List[BaseBlock]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SectionBlockOutput(BaseModel):
    title: str
    items: List[dict]


class SectionBlock(BaseBlock):
    _type = "section"
    _input_schema = SectionBlockInput
    _output_schema = SectionBlockOutput

    async def prepare_output(self, result: dict, ctx) -> dict:
        # result already contains the allowed children as a list of dicts.
        return {"title": result["title"], "items": result["children"]}
