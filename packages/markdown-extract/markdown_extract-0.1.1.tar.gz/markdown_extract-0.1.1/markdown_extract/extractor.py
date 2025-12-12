from .parser import parse_markdown


class Section:
    """
    Helper class to represent a section of the markdown file.
    Allows recursive access via brackets and string conversion.
    """
    def __init__(self, data_node, title=None):
        self._data = data_node
        self._title = title

    def __getitem__(self, key):
        if key in self._data:
            return Section(self._data[key], title=key)
        raise KeyError(f"Section '{key}' not found.")

    def __str__(self):
        return self._reconstruct_node(self._data, is_root=True)

    def __repr__(self):
        return self.__str__()
        
    def list(self) -> list:
        """
        Returns a list of child header names.
        """
        return [k for k in self._data.keys() if k not in ["__content__", "__header_line__"]]

    def _reconstruct_node(self, node, is_root=False) -> str:
        output = []

        if not is_root and "__header_line__" in node:
            output.append(node["__header_line__"])

        if "__content__" in node:
            output.extend(node["__content__"])

        # Iterate over children
        for key, value in node.items():
            if key not in ["__content__", "__header_line__"]:
                # It's a child node
                output.append(self._reconstruct_node(value, is_root=False))

        return "\n".join(output)


class MarkdownExtractor:
    """
    Main class to extract data from markdown content.
    """
    def __init__(self, file_content: str):
        self.data = parse_markdown(file_content)

    def list(self) -> list:
        """
        Returns a list of top-level header names.
        """
        return Section(self.data).list()

    def get_section(self, *headers) -> str:
        """
        Retrieves the content of a specific section defined by the hierarchy
        of headers.

        Args:
            *headers: Variable length argument list of header names (strings).
                      e.g. get_section("Header 1", "Header 2")

        Returns:
            The raw string content of the section, including sub-headers and
            their content. Returns None if not found.
        """
        current_node = self.data

        for header in headers:
            if header in current_node:
                current_node = current_node[header]
            else:
                return None

        # Reuse Section class for reconstruction
        return str(Section(current_node))

    def __getitem__(self, key):
        if key == "":
            return Section(self.data)
        if key in self.data:
            return Section(self.data[key], title=key)
        raise KeyError(f"Section '{key}' not found.")
