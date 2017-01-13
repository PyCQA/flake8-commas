import tokenize
import token as mod_token

import pep8
import pkg_resources

# A parenthesized expression list yields whatever that expression list
# yields: if the list contains at least one comma, it yields a tuple;
# otherwise, it yields the single expression that makes up the expression
# list.

PYTHON_2_KWDS = {
    'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
    'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if',
    'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise',
    'return', 'try', 'while', 'with', 'yield',
}

PYTHON_3_KWDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class',
    'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for',
    'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
    'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
}

KWD_LIKE_FUNCTION = {'import', 'assert'}

ALL_KWDS = (PYTHON_2_KWDS & PYTHON_3_KWDS) - KWD_LIKE_FUNCTION
NOT_PYTHON_2_KWDS = (PYTHON_3_KWDS - PYTHON_2_KWDS) - KWD_LIKE_FUNCTION
NOT_PYTHON_3_KWDS = (PYTHON_2_KWDS - PYTHON_3_KWDS) - KWD_LIKE_FUNCTION


class TupleOrParenthForm(object):
    def __bool__(self):
        return False

    __nonzero__ = __bool__

TUPLE_OR_PARENTH_FORM = TupleOrParenthForm()
PY3K_ONLY_ERROR = object()
PY2_ONLY_ERROR = object()

CLOSE_ATOM_STRINGS = {
    '}',
    ']',
    ')',
    '`',
}

ERRORS = {
    True: ('C812', 'missing trailing comma'),
    PY3K_ONLY_ERROR: ('C813', 'missing trailing comma in Python 3'),
    PY2_ONLY_ERROR: ('C814', 'missing trailing comma in Python 2'),
}


def process_parentheses(token, previous_token):
    if token.string == '(':
        is_function = (
            previous_token and
            (
                (previous_token.string in CLOSE_ATOM_STRINGS) or
                (
                    previous_token.type == mod_token.NAME and
                    previous_token.string not in ALL_KWDS
                )
            )
        )
        if is_function:
            tk_string = previous_token.string
            if tk_string in NOT_PYTHON_2_KWDS:
                return [PY2_ONLY_ERROR]
            if tk_string in NOT_PYTHON_3_KWDS:
                return [PY3K_ONLY_ERROR]
        else:
            return [TUPLE_OR_PARENTH_FORM]

    return [True]

try:
    dist = pkg_resources.get_distribution('flake8-trailing-commas')
    __version__ = dist.version
except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'


class CommaChecker(object):
    name = __name__
    version = __version__

    OPENING_BRACKETS = [
        '[',
        '{',
        '(',
    ]

    CLOSING_BRACKETS = [
        ']',
        '}',
        ')',
    ]

    def __init__(self, tree, filename='(none)', builtins=None):
        self.filename = filename

    def get_file_contents(self):
        if self.filename in ('stdin', '-', None):
            self.filename = 'stdin'
            return pep8.stdin_get_value().splitlines(True)
        else:
            return pep8.readlines(self.filename)

    def run(self):
        file_contents = self.get_file_contents()

        noqa_line_numbers = self.get_noqa_lines(file_contents)
        errors = self.get_comma_errors(file_contents)

        for error in errors:
            if error.get('line') not in noqa_line_numbers:
                yield (error.get('line'), error.get('col'), error.get('message'), type(self))

    def get_noqa_lines(self, file_contents):
        tokens = [Token(t) for t in tokenize.generate_tokens(lambda L=iter(file_contents): next(L))]
        return [token.start_row
                for token in tokens
                if token.type == tokenize.COMMENT and token.string.endswith('noqa')]

    def get_comma_errors(self, file_contents):
        tokens = [Token(t) for t in tokenize.generate_tokens(lambda L=iter(file_contents): next(L))]
        tokens = [t for t in tokens if t.type != tokenize.COMMENT]

        valid_comma_context = [False]

        for idx, token in enumerate(tokens):
            if token.string in self.OPENING_BRACKETS:
                previous_token = (
                    tokens[idx - 1] if (idx - 1 > 0) else None
                )
                valid_comma_context.extend(
                    process_parentheses(token, previous_token),
                )

            if token.string == 'for' and token.type == tokenize.NAME:
                valid_comma_context[-1] = False

            if (valid_comma_context[-1] == TUPLE_OR_PARENTH_FORM and
                    token.string == ','):
                valid_comma_context[-1] = True

            if (token.string in self.CLOSING_BRACKETS and
                    (idx - 1 > 0) and tokens[idx - 1].type == tokenize.NL and
                    (idx - 2 > 0) and tokens[idx - 2].string != ',' and
                    (idx - 3 > 0) and tokens[idx - 3].string != '**' and
                    valid_comma_context[-1]):

                end_row, end_col = tokens[idx - 2].end
                yield {
                    'message': '%s %s' % ERRORS[valid_comma_context[-1]],
                    'line': end_row,
                    'col': end_col,
                }

            if token.string in self.CLOSING_BRACKETS:
                valid_comma_context.pop()


class Token:
    '''Python 2 and 3 compatible token'''
    def __init__(self, token):
        self.token = token

    @property
    def type(self):
        return self.token[0]

    @property
    def string(self):
        return self.token[1]

    @property
    def start(self):
        return self.token[2]

    @property
    def start_row(self):
        return self.start[0]

    @property
    def start_col(self):
        return self.start[1]

    @property
    def end(self):
        return self.token[3]

    @property
    def end_row(self):
        return self.end[0]

    @property
    def end_col(self):
        return self.end[1]
