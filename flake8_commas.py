from sys import stdin
import tokenize


__version__ = '0.1.0'

COMMA_ERROR_CODE = 'C812'
COMMA_ERROR_MESSAGE = 'missing trailing comma'


class CommaChecker(object):
    name = __name__
    version = __version__

    CLOSING_BRACKETS = [
        ']',
        '}',
        ')',
    ]

    def __init__(self, tree, filename='(none)', builtins=None):
        self.file = (filename == 'stdin' and stdin) or filename

    def get_file_contents(self):
        with open(self.file, 'r') as file_to_check:
            return file_to_check.readlines()

    def run(self):
        if self.file == stdin:
            file_contents = self.file
        else:
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
        for token in tokens:
            if (token.string in self.CLOSING_BRACKETS and
                    last_token and last_token.type == tokenize.NL and
                    last_last_token and last_last_token.string != ','):

                end_row, end_col = last_last_token.end
                yield {
                    'message': '%s %s' % (COMMA_ERROR_CODE, COMMA_ERROR_MESSAGE),
                    'line': end_row,
                    'col': end_col,
                }

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
