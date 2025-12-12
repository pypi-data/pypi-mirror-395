import unittest
from markdown_extract import MarkdownExtractor

class TestTables(unittest.TestCase):
    def test_header_in_table_no_leading_pipe(self):
        # This is a valid markdown table where the third row starts with #
        markdown_content = """
        Col 1 | Col 2
        ---|---
        # Not a header | Val
        """
        extractor = MarkdownExtractor(markdown_content)
        
        # Check that it is NOT a section (child of root)
        # The title would be "Not a header | Val" if parsed as header
        with self.assertRaises(KeyError):
            _ = extractor["Not a header | Val"]
            
        # It should be in the __content__ list of the root
        root_content_list = extractor[""]._data["__content__"]
        self.assertTrue(any("# Not a header | Val" in line for line in root_content_list), 
                        "Line not found in root content list")

if __name__ == '__main__':
    unittest.main()
