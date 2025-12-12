import unittest
from markdown_extract import MarkdownExtractor

class TestListFeature(unittest.TestCase):
    def setUp(self):
        self.markdown_content = """
# Title
## Heading 1
### Heading 2
## Heading 3
"""
        self.extractor = MarkdownExtractor(self.markdown_content)

    def test_extractor_list(self):
        # extractor.list() should return ["Title"]
        # Assuming extractor.list() behaves like extractor[""].list() or lists top-level keys
        # The user said: "if I use extractor.list() it will return ["Title"]"
        self.assertEqual(self.extractor.list(), ["Title"])

    def test_section_list(self):
        # extractor["Title"].list() should return ["Heading 1", "Heading 3"]
        self.assertEqual(self.extractor["Title"].list(), ["Heading 1", "Heading 3"])

    def test_nested_section_list(self):
        # extractor["Title"]["Heading 1"].list() should return ["Heading 2"]
        self.assertEqual(self.extractor["Title"]["Heading 1"].list(), ["Heading 2"])
        
    def test_leaf_section_list(self):
        # extractor["Title"]["Heading 1"]["Heading 2"].list() should return []
        self.assertEqual(self.extractor["Title"]["Heading 1"]["Heading 2"].list(), [])

if __name__ == '__main__':
    unittest.main()
