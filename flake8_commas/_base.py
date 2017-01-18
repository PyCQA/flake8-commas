import tokenize
import collections
import token as mod_token

try:
    import pycodestyle
except ImportError:
    import pep8 as pycodestyle
import pkg_resources

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


Context = collections.namedtuple('Context', ['comma', 'unpack'])


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
                return [Context(FUNCTION_DEF, False)]
            tk_string = previous_token.type
            if tk_string == PY2_ONLY_ERROR:
                return [Context(PY2_ONLY_ERROR, False)]
            if tk_string == PY3K_ONLY_ERROR:
                return [Context(PY3K_ONLY_ERROR, False)]
        else:
            return [Context(TUPLE_OR_PARENTH_FORM, False)]

    return [Context(True, False)]


def get_file_contents(filename):
    if filename == 'stdin':
        return pycodestyle.stdin_get_value().splitlines(True)
    else:
        return pycodestyle.readlines(filename)


def get_tokens(file_contents):
    file_contents_iter = iter(file_contents)

    def file_contents_next():
        return next(file_contents_iter)

    for t in tokenize.generate_tokens(file_contents_next):
        yield Token(t)


def no_qa_comment(token):
    return token.type == tokenize.COMMENT and token.string.endswith('noqa')


def get_noqa_lines(file_contents):
    tokens = get_tokens(file_contents)
    return [token.start_row for token in tokens if no_qa_comment(token)]


def get_comma_errors(file_contents):
    tokens = simple_tokens(get_tokens(file_contents))

    stack = [Context(False, False)]

    window = collections.deque([NONE, NONE], maxlen=3)

    for token in tokens:
        window.append(token)
        prev_2, prev_1, _ = window
        if token.type in OPENING:
            stack.extend(
                process_parentheses(token, prev_1, prev_2),
            )

        if token.type == FOR:
            stack[-1] = Context(False, False)

        comma_found = (
            stack[-1].comma == TUPLE_OR_PARENTH_FORM and
            token.type == COMMA
        )
        if comma_found:
            stack[-1] = stack[-1]._replace(comma=True)

        if token.type == COMMA:
            stack[-1] = stack[-1]._replace(unpack=False)

        if token.type == UNPACK:
            stack[-1] = stack[-1]._replace(unpack=True)

        comma_required = (
            token.type in CLOSING and
            stack[-1].comma and
            prev_1.type == NEW_LINE and
            prev_2.type != COMMA and
            prev_2.type not in OPENING and
            not (stack[-1].unpack and stack[-1].comma == FUNCTION_DEF)
        )
        if comma_required:
            end_row, end_col = prev_2.token.end
            if (stack[-1].unpack):
                errors = ERRORS['py35']
            else:
                errors = ERRORS[stack[-1].comma]
            yield {
                'message': '%s %s' % errors,
                'line': end_row,
                'col': end_col,
            }

        if token.type in CLOSING:
            stack.pop()


class CommaChecker(object):
    name = __name__
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        fn = 'stdin' if filename in ('stdin', '-', None) else filename
        self.filename = fn

    def run(self):
        file_contents = get_file_contents(self.filename)

        noqa_line_numbers = get_noqa_lines(file_contents)
        for error in get_comma_errors(file_contents):
            if error.get('line') not in noqa_line_numbers:
                yield (
                    error.get('line'),
                    error.get('col'),
                    error.get('message'),
                    type(self),
                )


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
