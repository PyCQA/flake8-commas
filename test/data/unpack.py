def function(
    foo,
    bar,
    **kwargs
):
    pass

def function(
    foo,
    bar,
    *args
):
    pass

def function(
    foo,
    bar,
    *args,
    extra_kwarg,
    ):
    pass

result = function(
    foo,
    bar,
    **kwargs
)

result = function(
    foo,
    bar,
    **not_called_kwargs
)

def foo(
    ham,
    spam,
    *args,
    kwarg_only
    ):
    pass

# In python 3.5 if it's not a function def, commas are mandatory.

foo(
    **kwargs
)

{
    **kwargs
}

(
    *args
)

{
    *args
}

[
    *args
]

def foo(
    ham,
    spam,
    *args
    ):
    pass

def foo(
    ham,
    spam,
    **kwargs
    ):
    pass

def foo(
    ham,
    spam,
    *args,
    kwarg_only,
    ):
    pass

# In python 3.5 if it's not a function def, commas are mandatory.

foo(
    **kwargs,
)

{
    **kwargs,
}

(
    *args,
)

{
    *args,
}

[
    *args,
]
