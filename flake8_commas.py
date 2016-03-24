import tokenize

import pep8


__version__ = '0.1.1'

COMMA_ERROR_CODE = 'C812'
COMMA_ERROR_MESSAGE = 'missing trailing comma'


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

        last_last_token = None
        last_token = None
        is_comprehension = [False]
        for token in tokens:
            if token.type == tokenize.COMMENT:
                continue

            if token.string in self.OPENING_BRACKETS:
                is_comprehension.append(False)

            if token.string == 'for' and token.type == tokenize.NAME:
                is_comprehension[-1] = True

            if (token.string in self.CLOSING_BRACKETS and
                    last_token and last_token.type == tokenize.NL and
                    last_last_token and last_last_token.string != ',' and
                    not is_comprehension[-1]):

                end_row, end_col = last_last_token.end
                yield {
                    'message': '%s %s' % (COMMA_ERROR_CODE, COMMA_ERROR_MESSAGE),
                    'line': end_row,
                    'col': end_col,
                }

            if token.string in self.CLOSING_BRACKETS:
                is_comprehension.pop()

            last_last_token = last_token
            last_token = token


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
