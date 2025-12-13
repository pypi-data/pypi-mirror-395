from easy_block_builder import BaseBlock, Context


class GreetingBlock(BaseBlock):
    _type = "greeting"


class UserProfileBlock(BaseBlock):
    _type = "user_profile"


# Использование
async def example_nested():
    ctx = Context(vars={"user": "Eve", "theme": "dark"})

    greeting = GreetingBlock(
        {"text": "Welcome, {{ user }}!", "style": "{{ theme }}-mode"}
    )

    profile = UserProfileBlock(
        {
            "avatar_url": "/avatar/{{ user }}.png",
            "header": greeting,  # ← вложенный блок!
        }
    )

    result, _ = await profile.build(ctx)
    print(result)

    # {
    #   'avatar_url': '/avatar/Eve.png',
    #   'header': {
    #       'text': 'Welcome, Eve!',
    #       'style': 'dark-mode'
    #   }
    # }


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_nested())
