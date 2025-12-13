# example.py
import asyncio
from easy_block_builder import (
    Context,
    create_blocks_from_config,
    get_registered_block_types,
)
from blocks import *  # noqa: F403


async def main():
    print("Registered block types:", get_registered_block_types())

    config = [
        {
            "type": "section",
            "properties": {
                "title": "About us",
                "children": [
                    {
                        "type": "text",
                        "properties": {
                            "content": "We are a team {{ TEAM_NAME }}.",
                            "style": "intro",
                        },
                    },
                    {
                        "type": "image",
                        "properties": {
                            "src": "{{ CDN_URL }}/team.jpg",
                            "alt": "Our team",
                        },
                    },
                    {
                        "type": "section",
                        "properties": {
                            "title": "Contacts",
                            "children": [
                                {
                                    "type": "text",
                                    "properties": {
                                        "content": "Email: {{ CONTACT_EMAIL }}",
                                        "style": "small",
                                    },
                                }
                            ],
                        },
                    },
                ],
            },
        }
    ]

    blocks = create_blocks_from_config(config)

    ctx = Context(
        {
            "TEAM_NAME": "Easy Block Builder",
            "CDN_URL": "https://cdn.example.com",
            "CONTACT_EMAIL": "hello@example.com",
        }
    )

    results = []
    for block in blocks:
        data, _ = await block.build(ctx)
        results.append(data)

    import json

    print("\nThe final JSON result:\n")
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
