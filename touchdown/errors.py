class MarkdownSyntaxError(Exception):
    def __init__(self, file, lineno, message=''):
        self._file = file
        self._lineno = lineno
        self._message = message
        super().__init__(message)

    def __str__(self):
        return f'MarkdownSyntaxError\n  "File {self._file}": line {self._lineno}\n    {self._message}'
