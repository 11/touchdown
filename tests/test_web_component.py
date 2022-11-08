import unittest
from pprint import pprint
from pathlib import Path

from touchdown import to_ast, to_html


TESTCASE_DIR = './testcases/web-component'


class TestWebComponent(unittest.TestCase):
    def test_web_component_with_children_elements_markdown(self):
        pass

    def test_web_component_with_children_elements_html(self):
        pass

    def test_web_component_with_data_attribute_markdown(self):
        pass

    def test_web_component_with_data_attribute_html(self):
        pass

    def test_web_component_with_function_attribute_markdown(self):
        pass

    def test_web_component_with_function_attribute_html(self):
        pass

    def test_web_component_without_attributes_markdown(self):
        test_file = f'{TESTCASE_DIR}/test_web_component_without_attributes.md'
        expected_markdown = {}

        assert to_ast(test_file) == expected_markdown

    def test_web_component_no_attributes_html(self):
        pass

    def test_web_component_without_closing_tag_markdown(self):
        pass

    def test_web_component_without_closing_tag_html(self):
        pass
