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


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
