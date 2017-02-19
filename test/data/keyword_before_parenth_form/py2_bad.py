# Requires trailing commas in Py2 but syntax error in Py3k

def True(
    foo
):
    True(
        foo
    )
    True(
        foo,
        bar
    )


def False(
    foo
):
    False(
        foo
    )
    False(
        foo,
        bar
    )


def None(
    foo
):
    None(
        foo
    )
    None(
        foo,
        bar
    )


def nonlocal (
    foo
):
    nonlocal(
        foo
    )
    nonlocal(
        foo,
        bar
    )
