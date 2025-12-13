from typing import Dict, Any, List, Union
from .block import BaseBlock, BlockMeta
from logging import getLogger

_logger = getLogger(__name__)


def create_block(block_type: str, properties: Dict[str, Any]) -> BaseBlock:
    registry = BlockMeta.get_registry()
    if block_type not in registry:
        available = ", ".join(registry.keys())
        raise ValueError(
            f"Unknown block type: '{block_type}'. Available types: {available}"
        )

    block_class = registry[block_type]
    _logger.debug(
        "Creating block of type '%s' with class %s", block_type, block_class.__name__
    )
    return block_class(properties)


def create_blocks_from_config(
    config: Union[List[Dict[str, Any]], Dict[str, Any]],
) -> List[BaseBlock]:
    blocks = []

    if isinstance(config, dict) and "type" in config:
        config = [config]

    for block_config in config:
        block_type = block_config.get("type")
        if not block_type:
            raise ValueError("Block configuration must contain 'type' field")

        properties = block_config.get("properties", {})

        # Рекурсивная обработка вложенных блоков
        for prop_name, prop_value in properties.items():
            if isinstance(prop_value, list) and all(
                isinstance(item, dict) and "type" in item for item in prop_value
            ):
                nested_blocks = create_blocks_from_config(prop_value)
                properties[prop_name] = nested_blocks
            elif isinstance(prop_value, dict) and "type" in prop_value:
                nested_block = create_blocks_from_config(prop_value)[0]
                properties[prop_name] = nested_block

        block = create_block(block_type, properties)
        blocks.append(block)

    return blocks


def get_registered_block_types() -> List[str]:
    return list(BlockMeta.get_registry().keys())
