from x import (
    y
)

assert(
    SyntaxWarning,
    ThrownHere,
    Anyway
)

# async await is fine outside an async def

def await(
    foo
):
    async(
        foo
    )

def async(
    foo
):
    await(
        foo
    )
