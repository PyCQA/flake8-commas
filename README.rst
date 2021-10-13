Flake8 Extension to enforce better comma placement.
===================================================

.. image:: http://unmaintained.tech/badge.svg
  :target: http://unmaintained.tech
  :alt: No Maintenance Intended

Usage
-----

If you are using flake8 it's as easy as:

.. code:: shell

    pip install flake8-commas

Now you can avoid those annoying merge conflicts on dictionary and list diffs.

Errors
------

Different versions of python require commas in different places. Ignore the
errors for languages you don't use in your flake8 config:

+------+-----------------------------------------+
| Code | message                                 |
+======+=========================================+
| C812 | missing trailing comma                  |
+------+-----------------------------------------+
| C813 | missing trailing comma in Python 3      |
+------+-----------------------------------------+
| C814 | missing trailing comma in Python 2      |
+------+-----------------------------------------+
| C815 | missing trailing comma in Python 3.5+   |
+------+-----------------------------------------+
| C816 | missing trailing comma in Python 3.6+   |
+------+-----------------------------------------+
| C818 | trailing comma on bare tuple prohibited |
+------+-----------------------------------------+
| C819 | trailing comma prohibited               |
+------+-----------------------------------------+

Examples
--------

.. code:: Python

    lookup_table = {
        'key1': 'value',
        'key2': 'something'  # <-- missing a trailing comma
    }

    json_data = json.dumps({
        "key": "value",
    }),                      # <-- incorrect trailing comma. json_data is now a tuple. Likely by accident.

