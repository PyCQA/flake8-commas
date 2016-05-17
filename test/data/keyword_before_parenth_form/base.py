from x import (
    y,
)

assert(
    SyntaxWarning,
    ThrownHere,
    Anyway,
)

if(
    foo and
    bar
):
    pass
elif(
    foo and
    bar
):
    pass

for x in(
    [1,2,3]
):
    print(x)


(x for x in (
    [1, 2, 3]
))

(
    'foo'
) is (
    'foo'
)

if (
    foo and
    bar
) or not (
    foo
) or (
    spam
):
    pass

def xyz():
    raise(
        Exception()
    )

def abc():
    return(
        3
    )

while(
    False
):
    pass

with(
    loop
):
    pass

def foo():
    yield (
        "foo"
    )

# async await is fine outside an async def

def await(
    foo,
):
    async(
        foo,
    )

def async(
    foo,
):
    await(
        foo,
    )
