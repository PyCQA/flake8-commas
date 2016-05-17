from flake8_commas import CommaChecker
import os
from unittest import TestCase


class TestChecks(TestCase):
    def test_get_noqa_lines(self):
        checker = CommaChecker(None, filename=get_absolute_path('data/no_qa.py'))
        self.assertEqual(checker.get_noqa_lines(checker.get_file_contents()), [2])


class CommaTestChecks(TestCase):
    def test_one_line_dict(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/one_line_dict.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_multiline_good_dict(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/multiline_good_dict.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_multiline_bad_dict(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/multiline_bad_dict.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 14, 'line': 2, 'message': 'C812 missing trailing comma'},
        ])

    def test_bad_list(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/bad_list.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 5, 'line': 4, 'message': 'C812 missing trailing comma'},
        ])

    def test_bad_function_call(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/bad_function_call.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 17, 'line': 3, 'message': 'C812 missing trailing comma'},
        ])

    def test_multiline_bad_function_def(self):
        fixture = 'data/multiline_bad_function_def.py'
        comma_checker = CommaChecker(None, filename=get_absolute_path(fixture))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 13, 'line': 9, 'message': 'C812 missing trailing comma'},
        ])

    def test_bad_function_one_param(self):
        fixture = 'data/multiline_bad_function_one_param.py'
        comma_checker = CommaChecker(None, filename=get_absolute_path(fixture))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 13, 'line': 2, 'message': 'C812 missing trailing comma'},
            {'col': 9, 'line': 8, 'message': 'C812 missing trailing comma'},
        ])

    def test_comma_good_dict(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/comment_good_dict.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_no_comma_required_list_comprehension(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/list_comprehension.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_no_comma_required_dict_comprehension(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/dict_comprehension.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_no_comma_required_multiline_if(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/multiline_if.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_no_comma_required_after_kwargs(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/kwargs.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_no_comma_required_in_parenth_form(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path('data/parenth_form.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_comma_required_in_argument_list(self):
        fixture = 'data/callable_before_parenth_form.py'
        comma_checker = CommaChecker(None, filename=get_absolute_path(fixture))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 7, 'line': 7, 'message': 'C812 missing trailing comma'},
            {'col': 7, 'line': 15, 'message': 'C812 missing trailing comma'},
            {'col': 7, 'line': 23, 'message': 'C812 missing trailing comma'},
        ])

    def test_comma_required_even_if_you_use_or(self):
        fixture = 'data/multiline_bad_or_dict.py'
        comma_checker = CommaChecker(None, filename=get_absolute_path(fixture))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 14, 'line': 3, 'message': 'C812 missing trailing comma'},
        ])

    def test_comma_not_required_even_if_you_use_dict_for(self):
        fixture = 'data/multiline_good_single_keyed_for_dict.py'
        comma_checker = CommaChecker(None, filename=get_absolute_path(fixture))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])


class ParenthFormChecks(TestCase):
    base = 'data/keyword_before_parenth_form/'

    def test_base(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path(self.base + 'base.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_base_bad(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path(self.base + 'base_bad.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 5, 'line': 2, 'message': 'C812 missing trailing comma'},
            {'col': 10, 'line': 8, 'message': 'C812 missing trailing comma'},
            {'col': 7, 'line': 14, 'message': 'C812 missing trailing comma'},
            {'col': 11, 'line': 17, 'message': 'C812 missing trailing comma'},
            {'col': 7, 'line': 21, 'message': 'C812 missing trailing comma'},
            {'col': 11, 'line': 24, 'message': 'C812 missing trailing comma'},
        ])

    def test_py2(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path(self.base + 'py2.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])

    def test_py2_bad(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path(self.base + 'py2_bad.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 7, 'line': 4, 'message': 'C814 missing trailing comma in Python 2'},
            {'col': 11, 'line': 7, 'message': 'C814 missing trailing comma in Python 2'},
            {'col': 7, 'line': 12, 'message': 'C814 missing trailing comma in Python 2'},
            {'col': 11, 'line': 15, 'message': 'C814 missing trailing comma in Python 2'},
            {'col': 7, 'line': 20, 'message': 'C814 missing trailing comma in Python 2'},
            {'col': 11, 'line': 23, 'message': 'C814 missing trailing comma in Python 2'},
            {'col': 7, 'line': 28, 'message': 'C814 missing trailing comma in Python 2'},
            {'col': 11, 'line': 31, 'message': 'C814 missing trailing comma in Python 2'},
        ])

    def test_py2_3(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path(self.base + 'py2_3.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [
            {'col': 9, 'line': 4, 'message': 'C813 missing trailing comma in Python 3'},
            {'col': 9, 'line': 8, 'message': 'C813 missing trailing comma in Python 3'},
        ])

    def test_py3(self):
        comma_checker = CommaChecker(None, filename=get_absolute_path(self.base + 'py3.py'))
        self.assertEqual(list(comma_checker.get_comma_errors(comma_checker.get_file_contents())), [])


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
