3.0.0 (2024-03-12)
------------------

- Project renamed to ``flake8-commas-x`` to continue maintenance.
- Support dropped for Python <3.8.
- Support added for Python 3.12.
- Drop explicit ``noqa`` handling; this is handled by flake8 now.
- Remove use of ``pkg_resources`` in favour of ``importlib``.
- CI moved to GitHub Actions.


2.1.0 (2021-10-13)
------------------

- Remove upper bound on flake8.
  (`Issue #67 <https://github.com/PyCQA/flake8-commas/issues/67>`_)
- Note: this project is no longer maintained, and now black
  or https://github.com/asottile/add-trailing-comma is recommended instead.
  (`Issue #63 <https://github.com/PyCQA/flake8-commas/pull/63>`_)
  (`Issue #69 <https://github.com/PyCQA/flake8-commas/pull/69>`_)

2.0.0 (2018-03-19)
------------------

- Hide ._base from flake8 --version.
  (`Issue #45 <https://github.com/PyCQA/flake8-commas/issue/45>`_)
- Update URL to https://github.com/PyCQA/flake8-commas/.
  (`Issue #51 <https://github.com/PyCQA/flake8-commas/pull/51>`_)
- Add check for trailing commas on bare tuples - C818, thanks to
  `Chris AtLee <https://github.com/catlee>`_ and
  `Arkadiusz Adamski <https://github.com/ar4s/flake8_tuple>`_
  (`PR #52 <https://github.com/PyCQA/flake8-commas/pull/52>`_)


1.0.0 (2018-01-04)
------------------

- No changes from 0.5.1, just releasing the first major version.


0.5.1 (2018-01-02)
------------------

- Refactor single/multi tuple/subscript to simply count commas in all cases.
- Prohibit trailing commas in lambda parameter lists.
- Fix a missing trailing comma false positive in subcripts with slices.
- Fix a prohibited trailing comma false positve in subscripts with slices.
- All (`Issue #48 <https://github.com/flake8-commas/flake8-commas/pull/48>`_)


0.5.0 (2018-01-02)
------------------

- Remove EOL Python 3.3.
  (`Issue #47 <https://github.com/flake8-commas/flake8-commas/pull/47>`_)
- Prohibit trailing commas where there is no following new line
  (or forming a single element tuple).
  (`Issue #46 <https://github.com/flake8-commas/flake8-commas/pull/46>`_)


0.4.3 (2017-04-25)
------------------

- Enforce trailing commas in subscript tuples and slices again.
  Regression from 0.4.2
  (`Issue #42 <https://github.com/flake8-commas/flake8-commas/pull/42>`_)


0.4.2 (2017-04-18)
------------------

- Prevent lambda params in a parenth form enforcing a trailing comma.
  (`Issue #41 <https://github.com/flake8-commas/flake8-commas/pull/41>`_)
- Fix issue preventing execution on Python 2 with Flake8 3.
  (`Issue #35 <https://github.com/flake8-commas/flake8-commas/issues/35>`_)
- Allow bare wrapped subscript notation access.
  (`Issue #39 <https://github.com/flake8-commas/flake8-commas/pull/39>`_)
- Don't require comma in assert statement with parenth form.
  (`Issue #37 <https://github.com/flake8-commas/flake8-commas/pull/37>`_)


0.4.1 (2017-01-18)
------------------

- Add the framework flake8 trove classifier.


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
