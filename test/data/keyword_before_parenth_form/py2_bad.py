# Requires trailing commas in Py2 but syntax error in Py3k

def True(
    foo
):
    True(
        foo
    )


def False(
    foo
):
    False(
        foo
    )


def None(
    foo
):
    None(
        foo
    )


def nonlocal (
    foo
):
    nonlocal(
        foo
    )
