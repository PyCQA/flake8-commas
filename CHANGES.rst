0.4.0 (2017-01-18)
------------------

- Support flake8 3.x.x.
  (`Issue #20 <https://github.com/flake8-commas/flake8-commas/issue/20>`_)
- No trailing comma after any function def with unpack.
- support Python 3.6 `issue9232 <https://bugs.python.org/issue9232>`_
  trailing commas.
  (`Issue #33 <https://github.com/flake8-commas/flake8-commas/pull/33>`_)


0.3.1 (2017-01-18)
------------------

- Also parse unpacks with literals.
  (`Issue #30 <https://github.com/flake8-commas/flake8-commas/issue/30>`_)


0.3.0 (2017-01-16)
------------------

- If there is a comment after the last item, do not report an error.
  (`Issue #18 <https://github.com/flake8-commas/flake8-commas/issue/18>`_)
- If there is an empty, tuple, list, dict, or function, do not report an error.
  (`Issue #17 <https://github.com/flake8-commas/flake8-commas/issue/17>`_)
- Support PEP 3132 Python 3.5+ extended unpacking.
  (`Issue #26 <https://github.com/flake8-commas/flake8-commas/issue/26>`_)
- `*args` should not require a trailing comma.
  (`Issue #27 <https://github.com/flake8-commas/flake8-commas/issue/27>`_)


0.2.0 (2017-01-13)
------------------

- First version of flake8-commas with changelog
- Fix HTML readme render on PyPI.
- Support various parenth_form edge cases.
- Merge from flake8-trailing-commas
