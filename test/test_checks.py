import os
import sys
import tokenize

import pycodestyle
from flake8 import utils

from flake8_commas._base import Token, get_comma_errors

C813 = 'C813 missing trailing comma in Python 3'
C814 = 'C814 missing trailing comma in Python 2'
C815 = 'C815 missing trailing comma in Python 3.5+'
C816 = 'C816 missing trailing comma in Python 3.6+'
C818 = 'C818 trailing comma on bare tuple prohibited'


def get_tokens(filename):
    if filename == 'stdin':
        file_contents = utils.stdin_get_value().splitlines(True)
    else:
        file_contents = pycodestyle.readlines(filename)
    file_contents_iter = iter(file_contents)

    def file_contents_next():
        return next(file_contents_iter)

    for t in tokenize.generate_tokens(file_contents_next):
        yield Token(t)


def test_one_line_dict():
    filename = get_absolute_path('data/one_line_dict.py')
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_multiline_good_dict():
    filename = get_absolute_path('data/multiline_good_dict.py')
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_multiline_bad_dict():
    filename = get_absolute_path('data/multiline_bad_dict.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 14, 'line': 2, 'message': 'C812 missing trailing comma'},
    ]


def test_bad_list():
    filename = get_absolute_path('data/bad_list.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 5, 'line': 4, 'message': 'C812 missing trailing comma'},
        {'col': 5, 'line': 10, 'message': 'C812 missing trailing comma'},
        {'col': 5, 'line': 17, 'message': 'C812 missing trailing comma'},
    ]


def test_bad_function_call():
    filename = get_absolute_path('data/bad_function_call.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 17, 'line': 3, 'message': 'C812 missing trailing comma'},
    ]


def test_multiline_bad_function_def():
    fixture = 'data/multiline_bad_function_def.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 13, 'line': 9, 'message': 'C812 missing trailing comma'},
    ]


def test_bad_function_one_param():
    fixture = 'data/multiline_bad_function_one_param.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 13, 'line': 2, 'message': 'C812 missing trailing comma'},
        {'col': 9, 'line': 8, 'message': 'C812 missing trailing comma'},
    ]


def test_good_empty_comma_context():
    fixture = 'data/good_empty_comma_context.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_comma_good_dict():
    fixture = 'data/comment_good_dict.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_no_comma_required_list_comprehension():
    fixture = 'data/list_comprehension.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_no_comma_required_dict_comprehension():
    fixture = 'data/dict_comprehension.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_no_comma_required_multiline_if():
    fixture = 'data/multiline_if.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_no_comma_required_multiline_subscript():
    fixture = 'data/multiline_index_access.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 14, 'line': 27, 'message': 'C812 missing trailing comma'},
        {'col': 14, 'line': 34, 'message': 'C812 missing trailing comma'},
    ]


def test_comma_required_multiline_subscript_with_slice():
    fixture = 'data/multiline_subscript_slice.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 14, 'line': 5, 'message': 'C812 missing trailing comma'},
        {'col': 14, 'line': 33, 'message': 'C812 missing trailing comma'},
    ]


def test_comma_required_after_unpack_in_non_def_python_3_5():
    fixture = 'data/unpack.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 12, 'line': 4, 'message': C816},
        {'col': 9, 'line': 11, 'message': C816},
        {'col': 15, 'line': 19, 'message': C816},
        {'col': 12, 'line': 26, 'message': C815},
        {'col': 23, 'line': 32, 'message': C815},
        {'col': 14, 'line': 39, 'message': C816},
        {'col': 12, 'line': 46, 'message': C815},
        {'col': 12, 'line': 50, 'message': C815},
        {'col': 9, 'line': 58, 'message': C815},
        {'col': 9, 'line': 62, 'message': C815},
        {'col': 9, 'line': 68, 'message': C816},
        {'col': 12, 'line': 75, 'message': C816},
        {'col': 14, 'line': 83, 'message': C816},
        {'col': 19, 'line': 112, 'message': C815},
    ]


def test_no_comma_required_in_parenth_form():
    fixture = 'data/parenth_form.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_comma_required_in_argument_list():
    fixture = 'data/callable_before_parenth_form.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 7, 'line': 7, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 15, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 23, 'message': 'C812 missing trailing comma'},
    ]


def test_comma_required_even_if_you_use_or():
    fixture = 'data/multiline_bad_or_dict.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 14, 'line': 3, 'message': 'C812 missing trailing comma'},
    ]


def test_comma_not_required_in_multiline_case():
    fixture = 'data/multiline_case.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_comma_required_in_multiline_case_nested():
    fixture = 'data/multiline_case_bad.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 20, 'line': 5, 'message': 'C812 missing trailing comma'},
    ]


def test_comma_required_in_f_string_call():
    fixture = 'data/f_strings.py'
    filename = get_absolute_path(fixture)

    expected = (
        [
            {
                'col': 12,
                'line': 7,
                'message': 'C819 trailing comma prohibited',
            },
            {
                'col': 6,
                'line': 11,
                'message': 'C812 missing trailing comma',
            },
        ]
        if sys.version_info >= (3, 12)
        else []
    )

    assert list(get_comma_errors(get_tokens(filename))) == expected


def test_comma_not_required_even_if_you_use_dict_for():
    fixture = 'data/multiline_good_single_keyed_for_dict.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_comma_not_required_in_parenth_form_string_splits():
    fixture = 'data/multiline_string.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_comma_not_required_in_comment_lines():
    fixture = 'data/good_list.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_tokens(filename))) == []


base = 'data/keyword_before_parenth_form/'


def test_base():
    filename = get_absolute_path(base + 'base.py')
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_base_bad():
    filename = get_absolute_path(base + 'base_bad.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 5, 'line': 2, 'message': 'C812 missing trailing comma'},
        {'col': 10, 'line': 8, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 14, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 17, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 21, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 24, 'message': 'C812 missing trailing comma'},
    ]


def test_py2():
    filename = get_absolute_path(base + 'py2.py')
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_py2_bad():
    filename = get_absolute_path(base + 'py2_bad.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 7, 'line': 4, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 7, 'message': C814},
        {'col': 7, 'line': 12, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 15, 'message': C814},
        {'col': 7, 'line': 20, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 23, 'message': C814},
        {'col': 7, 'line': 28, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 31, 'message': C814},
    ]


def test_py2_3():
    filename = get_absolute_path(base + 'py2_3.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
        {'col': 9, 'line': 4, 'message': C813},
        {'col': 9, 'line': 8, 'message': C813},
    ]


def test_py3():
    filename = get_absolute_path(base + 'py3.py')
    assert list(get_comma_errors(get_tokens(filename))) == []


def test_prohibited():
    filename = get_absolute_path('data/prohibited.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
       {'col': 21, 'line': 1, 'message': 'C819 trailing comma prohibited'},
       {'col': 13, 'line': 3, 'message': 'C819 trailing comma prohibited'},
       {'col': 18, 'line': 5, 'message': 'C819 trailing comma prohibited'},
       {'col': 6, 'line': 10, 'message': 'C819 trailing comma prohibited'},
       {'col': 21, 'line': 12, 'message': 'C819 trailing comma prohibited'},
       {'col': 13, 'line': 14, 'message': 'C819 trailing comma prohibited'},
       {'col': 18, 'line': 16, 'message': 'C819 trailing comma prohibited'},
       {'col': 6, 'line': 21, 'message': 'C819 trailing comma prohibited'},
       {'col': 10, 'line': 27, 'message': 'C819 trailing comma prohibited'},
       {'col': 9, 'line': 29, 'message': 'C819 trailing comma prohibited'},
    ]


def test_bare():
    # Tests inspired by flake8_tuple https://git.io/vxstN
    filename = get_absolute_path('data/bare.py')
    assert list(get_comma_errors(get_tokens(filename))) == [
       {'col': 8, 'line': 7, 'message': C818},
       {'col': 19, 'line': 9, 'message': C818},
       {'col': 8, 'line': 16, 'message': C818},
       {'col': 10, 'line': 20, 'message': C818},
       {'col': 32, 'line': 27, 'message': C818},
       {'col': 26, 'line': 29, 'message': C818},
       {'col': 17, 'line': 32, 'message': C818},
    ]


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
