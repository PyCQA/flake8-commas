import tokenize

import pep8
import pkg_resources

COMMA_ERROR_CODE = 'C812'
COMMA_ERROR_MESSAGE = 'missing trailing comma'

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
                valid_comma_context.append(True)

            if token.string in ('for', 'and', 'or') and token.type == tokenize.NAME:
                valid_comma_context[-1] = False

            if (token.string in self.CLOSING_BRACKETS and
                    (idx - 1 > 0) and tokens[idx - 1].type == tokenize.NL and
                    (idx - 2 > 0) and tokens[idx - 2].string != ',' and
                    (idx - 3 > 0) and tokens[idx - 3].string != '**' and
                    valid_comma_context[-1]):

                end_row, end_col = tokens[idx - 2].end
                yield {
                    'message': '%s %s' % (COMMA_ERROR_CODE, COMMA_ERROR_MESSAGE),
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
