# Run all tests
#     python -m unittest tests.py
#
# Run all tests and stop at first failure
#     python -m unittest -f tests.py
#     python -m unittest --failfast tests.py
#
# Run all tests, but if ^c is pressed, wait until current test is complete to kill process
#     python -m unittest -c tests.py
#     python -m unittest -catch tests.py


import unittest

from markdown import Markdown as MD


TESTCASE_DIR = '../testcases/'


class TestHeader(unittest.TestCase):
    def test_valid_headers(self):
        output = MD(TESTCASE_DIR + 'test_header.md').parse()
        expected_output = {
            'file': '../testcases/test_header.md',
            'content': [{
                'token': 'header',
                'tag': 'h1',
                'content': 'header 1'
            },
            {
                'token': 'header',
                'tag': 'h2',
                'content': 'header 2'
            },
            {
                'token': 'header',
                'tag': 'h3',
                'content': 'header 3'
            },
            {
                'token': 'header',
                'tag': 'h4',
                'content': 'header 4'
            },
            {
                'token': 'header',
                'tag': 'h5',
                'content': 'header 5'
            },
            {
                'token': 'header',
                'tag': 'h6',
                'content': 'header 6'
            }]
        }

        assert output == expected_output


# class TestOrderedList(unittest.TestCase):
#     pass
#
#
# class TestUnorderedList(unittest.TestCase):
#     pass
#
#
# class TestImage(unittest.TestCase):
#     pass
#
#
# class TestText(unittest.TestCase):
#     pass


if __name__ == '__main__':
    unittest.main()

