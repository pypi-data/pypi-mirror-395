import unittest
from markdown_extract import MarkdownExtractor

class TestEdgeCases(unittest.TestCase):
    def test_code_block_with_comments(self):
        markdown_content = """
        # Section 1
        Some text.

        ```python
        # This is a comment, not a header
        def foo():
            pass
        ```

        ## Section 2
        More text.
        """
        extractor = MarkdownExtractor(markdown_content)
        
        # "Section 1" should contain the code block
        section_1 = str(extractor["Section 1"])
        self.assertIn("```python", section_1)
        self.assertIn("# This is a comment, not a header", section_1)
        
        # "Section 1" should NOT have a child called "This is a comment, not a header"
        with self.assertRaises(KeyError):
            _ = extractor["This is a comment, not a header"]
            
        # Section 2 should exist as a child of Section 1
        self.assertIn("Section 2", extractor["Section 1"]._data)

    def test_root_access(self):
        markdown_content = """Pre-header content.
        # Section 1
        Content.
        """
        extractor = MarkdownExtractor(markdown_content)
        
        # Test accessing root via empty string (simulating "empty bracket" intent)
        root_content = str(extractor[""])
        self.assertIn("Pre-header content.", root_content)
        self.assertIn("# Section 1", root_content)
        self.assertIn("Content.", root_content)

        self.assertIn("Content.", root_content)

    def test_math_block(self):
        markdown_content = """
        $$
        # Math Header
        x = y^2
        $$
        # Real Header
        """
        extractor = MarkdownExtractor(markdown_content)
        # Should NOT be parsed as a header
        with self.assertRaises(KeyError):
            _ = extractor["Math Header"]
            
        self.assertIn("Real Header", extractor.data)

    def test_front_matter(self):
        markdown_content = """
        ---
        title: My Title
        # Front Matter Header
        date: 2023-01-01
        ---
        # Real Header
        """
        extractor = MarkdownExtractor(markdown_content)
        # Should NOT be parsed as a header
        with self.assertRaises(KeyError):
            _ = extractor["Front Matter Header"]
            
        self.assertIn("Real Header", extractor.data)

if __name__ == '__main__':
    unittest.main()
