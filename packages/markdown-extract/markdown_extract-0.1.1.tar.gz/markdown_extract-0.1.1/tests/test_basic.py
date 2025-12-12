import unittest
from markdown_extract import MarkdownExtractor

class TestMarkdownExtractor(unittest.TestCase):
    def setUp(self):
        self.sample_markdown = """# Header 1
        Content under H1.

        ## Header 2
        Content under H2.

        ### Header 3
        Content under H3.

        ## Header 2b
        Content under H2b.
        """
        self.extractor = MarkdownExtractor(self.sample_markdown)

    def test_layer_1(self):
        # Should return everything under Header 1, including H2 and H3
        content = self.extractor.get_section("Header 1")
        self.assertIn("Content under H1.", content)
        self.assertIn("## Header 2", content)
        self.assertIn("Content under H2.", content)
        self.assertIn("### Header 3", content)
        self.assertIn("## Header 2b", content)
        
    def test_layer_2(self):
        # Should return content under Header 2
        content = self.extractor.get_section("Header 1", "Header 2")
        self.assertIn("Content under H2.", content)
        self.assertIn("### Header 3", content)
        # Should NOT contain Header 2b
        self.assertNotIn("## Header 2b", content)
        
    def test_layer_3(self):
        content = self.extractor.get_section("Header 1", "Header 2", "Header 3")
        self.assertIn("Content under H3.", content)
        
    def test_missing_section(self):
        content = self.extractor.get_section("Header 1", "NonExistent")
        self.assertIsNone(content)

    def test_bracket_access(self):
        # Test accessing sections via brackets
        section = self.extractor["Header 1"]
        content = str(section)
        self.assertIn("Content under H1.", content)
        self.assertIn("## Header 2", content)
        
        # Test nested access
        sub_section = self.extractor["Header 1"]["Header 2"]
        content_sub = str(sub_section)
        self.assertIn("Content under H2.", content_sub)
        self.assertNotIn("## Header 2b", content_sub)
        
        # Test deep nested access
        deep_section = self.extractor["Header 1"]["Header 2"]["Header 3"]
        self.assertIn("Content under H3.", str(deep_section))

    def test_bracket_missing(self):
        with self.assertRaises(KeyError):
            _ = self.extractor["NonExistent"]
            
        with self.assertRaises(KeyError):
            _ = self.extractor["Header 1"]["NonExistent"]

if __name__ == '__main__':
    unittest.main()
