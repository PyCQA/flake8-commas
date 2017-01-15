import tokenize
import collections
import token as mod_token

try:
    import pycodestyle
except ImportError:
    import pep8 as pycodestyle
import pkg_resources

__all__ = ['CommaChecker']

try:
    dist = pkg_resources.get_distribution('flake8-commas')
    __version__ = dist.version
except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'

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


class SimpleToken(object):
    def __init__(self, token, type):
        self.token = token
        self.type = type

NEW_LINE = 'new-line'
COMMA = ','
OPENING_BRACKET = '('
SOME_CLOSING = 'some-closing'
SOME_OPENING = 'some-opening'
OPENING = {SOME_OPENING,  OPENING_BRACKET}
CLOSING = {SOME_CLOSING}
BACK_TICK = '`'
CLOSE_ATOM = CLOSING | {BACK_TICK}
FOR = 'for'
NAMED = 'named'
PY2_ONLY_ERROR = 'py2-only-error'
PY3K_ONLY_ERROR = 'py3-only-error'
DEF = 'def'
FUNCTION_DEF = 'function-def'
FUNCTION = {NAMED, PY2_ONLY_ERROR, PY3K_ONLY_ERROR, FUNCTION_DEF}
UNPACK = '* or **'
NONE = SimpleToken(token=None, type=None)


def get_type(token):
    type = token.type
    if type == tokenize.NL:
        return NEW_LINE

    string = token.string
    if type == tokenize.NAME and string == 'for':
        return FOR
    if type == tokenize.NAME and string == 'def':
        return DEF
    if type == mod_token.NAME and string not in ALL_KWDS:
        if string in NOT_PYTHON_2_KWDS:
            return PY2_ONLY_ERROR
        if string in NOT_PYTHON_3_KWDS:
            return PY3K_ONLY_ERROR
        return NAMED
    if string in {'**', '*'}:
        return UNPACK
    if string == ',':
        return COMMA
    if string == '(':
        return OPENING_BRACKET
    if string in {'[', '{'}:
        return SOME_OPENING
    if string in {']', ')', '}'}:
        return SOME_CLOSING
    if string == '`':
        return BACK_TICK
    return


def simple_tokens(tokens):
    tokens = (Token(t) for t in tokens)
    tokens = (t for t in tokens if t.type != tokenize.COMMENT)

    token = next(tokens)
    previous_token = SimpleToken(token=token, type=get_type(token))
    for token in tokens:
        next_token = SimpleToken(token=token, type=get_type(token))
        if previous_token.type == NEW_LINE and next_token.type == NEW_LINE:
            continue
        yield previous_token
        previous_token = next_token

ERRORS = {
    True: ('C812', 'missing trailing comma'),
    FUNCTION_DEF: ('C812', 'missing trailing comma'),
    PY3K_ONLY_ERROR: ('C813', 'missing trailing comma in Python 3'),
    PY2_ONLY_ERROR: ('C814', 'missing trailing comma in Python 2'),
    'py35': ('C815', 'missing trailing comma in Python 3.5+'),
}


def process_parentheses(token, prev_1, prev_2):
    previous_token = prev_1

    if token.type == OPENING_BRACKET:
        is_function = (
            previous_token and
            (
                (previous_token.type in CLOSE_ATOM) or
                (
                    previous_token.type in FUNCTION
                )
            )
        )
        if is_function:
            if prev_2.type == DEF:
                return [FUNCTION_DEF]
            tk_string = previous_token.type
            if tk_string == PY2_ONLY_ERROR:
                return [PY2_ONLY_ERROR]
            if tk_string == PY3K_ONLY_ERROR:
                return [PY3K_ONLY_ERROR]
        else:
            return [TUPLE_OR_PARENTH_FORM]

    return [True]


class CommaChecker(object):
    name = __name__
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        self.filename = filename

    def get_file_contents(self):
        if self.filename in ('stdin', '-', None):
            self.filename = 'stdin'
            return pycodestyle.stdin_get_value().splitlines(True)
        else:
            return pycodestyle.readlines(self.filename)

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
        tokens = simple_tokens(tokenize.generate_tokens(lambda L=iter(file_contents): next(L)))

        valid_comma_context = [False]

        window = collections.deque([NONE, NONE, NONE], maxlen=4)

        for token in tokens:
            window.append(token)
            prev_3, prev_2, prev_1, _ = window
            if token.type in OPENING:
                valid_comma_context.extend(
                    process_parentheses(token, prev_1, prev_2),
                )

            if token.type == FOR:
                valid_comma_context[-1] = False

            if (valid_comma_context[-1] == TUPLE_OR_PARENTH_FORM and token.type == COMMA):
                valid_comma_context[-1] = True

            comma_required = (
                token.type in CLOSING and
                valid_comma_context[-1] and
                prev_1.type == NEW_LINE and
                prev_2.type != COMMA and
                prev_2.type not in OPENING and
                (
                    prev_3.type != UNPACK or
                    (prev_3.type == UNPACK and valid_comma_context[-1] != FUNCTION_DEF)
                )
            )
            if comma_required:
                end_row, end_col = prev_2.token.end
                if (prev_3.type == UNPACK):
                    errors = ERRORS['py35']
                else:
                    errors = ERRORS[valid_comma_context[-1]]
                yield {
                    'message': '%s %s' % errors,
                    'line': end_row,
                    'col': end_col,
                }

            if token.type in CLOSING:
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
