import os

from flake8_commas._base import (
    get_file_contents, get_noqa_lines, get_comma_errors,
)

C813 = 'C813 missing trailing comma in Python 3'
C814 = 'C814 missing trailing comma in Python 2'
C815 = 'C815 missing trailing comma in Python 3.5+'


def test_get_noqa_lines():
    filename = get_absolute_path('data/no_qa.py')
    assert get_noqa_lines(get_file_contents(filename)) == [2]


def test_one_line_dict():
    filename = get_absolute_path('data/one_line_dict.py')
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_multiline_good_dict():
    filename = get_absolute_path('data/multiline_good_dict.py')
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_multiline_bad_dict():
    filename = get_absolute_path('data/multiline_bad_dict.py')
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 14, 'line': 2, 'message': 'C812 missing trailing comma'},
    ]


def test_bad_list():
    filename = get_absolute_path('data/bad_list.py')
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 5, 'line': 4, 'message': 'C812 missing trailing comma'},
        {'col': 5, 'line': 10, 'message': 'C812 missing trailing comma'},
        {'col': 5, 'line': 17, 'message': 'C812 missing trailing comma'},
    ]


def test_bad_function_call():
    filename = get_absolute_path('data/bad_function_call.py')
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 17, 'line': 3, 'message': 'C812 missing trailing comma'},
    ]


def test_multiline_bad_function_def():
    fixture = 'data/multiline_bad_function_def.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 13, 'line': 9, 'message': 'C812 missing trailing comma'},
    ]


def test_bad_function_one_param():
    fixture = 'data/multiline_bad_function_one_param.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 13, 'line': 2, 'message': 'C812 missing trailing comma'},
        {'col': 9, 'line': 8, 'message': 'C812 missing trailing comma'},
    ]


def test_good_empty_comma_context():
    fixture = 'data/good_empty_comma_context.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_comma_good_dict():
    fixture = 'data/comment_good_dict.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_no_comma_required_list_comprehension():
    fixture = 'data/list_comprehension.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_no_comma_required_dict_comprehension():
    fixture = 'data/dict_comprehension.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_no_comma_required_multiline_if():
    fixture = 'data/multiline_if.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_comma_required_after_unpack_in_non_def_python_3_5():
    fixture = 'data/unpack.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 12, 'line': 26, 'message': C815},
        {'col': 23, 'line': 32, 'message': C815},
        {'col': 14, 'line': 39, 'message': 'C812 missing trailing comma'},
        {'col': 12, 'line': 46, 'message': C815},
        {'col': 12, 'line': 50, 'message': C815},
        {'col': 9, 'line': 58, 'message': C815},
        {'col': 9, 'line': 62, 'message': C815},
        {'col': 19, 'line': 112, 'message': C815},
    ]


def test_no_comma_required_in_parenth_form():
    fixture = 'data/parenth_form.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_comma_required_in_argument_list():
    fixture = 'data/callable_before_parenth_form.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 7, 'line': 7, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 15, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 23, 'message': 'C812 missing trailing comma'},
    ]


def test_comma_required_even_if_you_use_or():
    fixture = 'data/multiline_bad_or_dict.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 14, 'line': 3, 'message': 'C812 missing trailing comma'},
    ]


def test_comma_not_required_even_if_you_use_dict_for():
    fixture = 'data/multiline_good_single_keyed_for_dict.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_comma_not_required_in_parenth_form_string_splits():
    fixture = 'data/multiline_string.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_comma_not_required_in_comment_lines():
    fixture = 'data/good_list.py'
    filename = get_absolute_path(fixture)
    assert list(get_comma_errors(get_file_contents(filename))) == []


base = 'data/keyword_before_parenth_form/'


def test_base():
    filename = get_absolute_path(base + 'base.py')
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_base_bad():
    filename = get_absolute_path(base + 'base_bad.py')
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 5, 'line': 2, 'message': 'C812 missing trailing comma'},
        {'col': 10, 'line': 8, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 14, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 17, 'message': 'C812 missing trailing comma'},
        {'col': 7, 'line': 21, 'message': 'C812 missing trailing comma'},
        {'col': 11, 'line': 24, 'message': 'C812 missing trailing comma'},
    ]


def test_py2():
    filename = get_absolute_path(base + 'py2.py')
    assert list(get_comma_errors(get_file_contents(filename))) == []


def test_py2_bad():
    filename = get_absolute_path(base + 'py2_bad.py')
    assert list(get_comma_errors(get_file_contents(filename))) == [
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
    assert list(get_comma_errors(get_file_contents(filename))) == [
        {'col': 9, 'line': 4, 'message': C813},
        {'col': 9, 'line': 8, 'message': C813},
    ]


def test_py3():
    filename = get_absolute_path(base + 'py3.py')
    assert list(get_comma_errors(get_file_contents(filename))) == []


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
