import re
import json
import logging
from pprint import pformat
from pathlib import Path

from .lib import readfile
from .lib import MARKDOWN_TOKENS as tks
from .errors import MarkdownSyntaxError


logger = logging.getLogger()


class Markdown:
    def __init__(self, file):
        self._filepath = Path(file)
        self._lineno = 0
        self._output = 'json'

        self._reader = None

    def __repr__(self):
        return f'File {self._filepath.name} - Lines processed {self._lineno}'

    def __str__(self):
        if self._output == 'html':
            # TODO: pprint HTML
            pass

        return pformat(self.parse())

    def __iter__(self):
        self._reader = readfile(self._filepath)
        return self

    def __next__(self):
        line = next(self._reader, None)
        if not line:
            raise StopIteration

        self._lineno += 1

        if re.match(tks['header'], line):
            return self._parse_header(line)
        elif re.match(tks['blockquote'], line):
            return self._parse_blockquote(line)
        elif re.match(tks['ordered_list'], line):
            return self._parse_ordered_list(self._reader)
        elif re.match(tks['unordered_list'], line):
            return self._parse_unordered_list(slef._reader)
        elif re.match(tks['image'], line):
            print('image')
        elif re.match(tks['codeblock'], self._reader):
            print('codeblock')
        else:
            print('paragraph')

    @property
    def filename(self):
        return self._filepath.name

    def parse(self, output='json', pretty=False):
        result = {
            'filename': self._filepath.name,
            'content': [token for token in self],
        }

        if output == 'json':
            if pretty:
                return json.dumps(result, indent=4, sort_keys=True)
            else:
                return json.dumps(result)
        else:
            # TODO: parse HTML output
            pass

    def _parse_header(self, line):
        match = re.findall(tks['header'], line)
        if len(match) != 1:
            raise MarkdownSyntaxError(self._file, self._lineno, '')

        header, content = match[0]
        return {
            'token': 'header',
            'tag': f'h{len(header)}',
            'content': content,
        }

    def _parse_blockquote(self, line):
        match = re.findall(tks['blockquote'], line)
        if len(match) != 1:
            raise MarkdownSyntaxError(self._file, self._lineno, '')

        blockquote, content = match[0]
        return {
            'token': 'blockquote',
            'tag': 'blockquote',
            'content': self._parse_text(content),
        }

    def _parse_image(self, line):
        pass

    def _parse_codeblock(self, line, reader):
        match = re.findall(tks['codeblock'], line)
        if len(match) != 1:
            raise MarkdownSyntaxError(self._file, self._lineno, '')

        codeblock, content = match[0]
        return {
            'token': 'codeblock',
            'tag': 'pre',
            'content': content,
            'languahe': None,
        }

    def _parse_list(self, reader, list_type, list_tag):
        reader.backstep() # reset the file generator back to the beginning of the ordered list

        output = {
            'element': list_type,
            'tag': list_tag,
            'content': [],
        }

        while (line := next(reader, None)):
            match = None
            if re.match(tks['ordered_list'], line):
                match = re.findall(tks['ordered_list'], line)
            else:
                reader.backstep()
                break

            if len(match) > 1 or len(match < 1):
                raise MarkdownSyntaxError(self._file, self._lineno, '')

            _, content = match[0]

            output['content'].append({
                'token': 'listitem',
                'tag': 'li',
                'content': self._parse_text(content),
            })

        return output

    def _parse_ordered_list(self, reader):
        return self._parse_list(reader, 'ordered_list', 'ol')

    def _parse_unordered_list(self, line):
        return self._parse_list(reader, 'unordered_list', 'ul')

    def _parse_link(self, line, seek=0):
        pass

    def _parse_decoration(self, line, seek=0):
        decors = set('*', '`', '/', '_', '~')
        decors_map = {
            '*': { 'token': 'bold',          'tag': 'b' },
            '`': { 'token': 'code',          'tag': 'span' },
            '/': { 'token': 'italic',        'tag': 'i' },
            '_': { 'token': 'underline',     'tag': 'u' },
            '~': { 'token': 'strikethrough', 'tag': 'strikethrough' },
        }

        stack = []
        idx = seek
        while idx < len(line):
            cur = line[idx]
            prev = line[idx-1] if idx > 0 else None

            if prev != '\\' and cur in decors:
                if len(stack) > 0 and stack[-1] == cur:
                    char, start_idx = stack.pop()
                    decor = decors_map[char].copy()
                    # decor['content'] =
                else:
                    stack.append((cur, idx))

            idx += 1

        return output

    def _parse_text(self, line):
        decors = set('*', '_', '~', '/', '`')
        output = {
            'element': 'paragraph',
            'tag': 'p',
            'content': [],
        }

        start = 0
        end = 0
        while end < len(line):
            cur = line[idx]
            prev = line[idx-1] if idx > 0 else None

            if prev != '\\' and cur in decors:
                # append plain text to output and reset sliding window
                text = { 'element': 'text', 'content': line[start:end] }
                output['content'].append(text)
                start = end

                # parse decorations
                decor = self._parse_decoration(self, line, idx);
                output['content'].append(decor)

            end += 1

        return output

