import re


def parse_markdown(file_content: str) -> dict:
    """
    Parses markdown content into a nested dictionary based on headers.

    Args:
        file_content: The string content of the markdown file.

    Returns:
        A dictionary representing the structure of the markdown file.
        Keys are header names, values are either dictionaries (sub-sections)
        or strings (content).
    """
    lines = file_content.split('\n')
    return _parse_lines(lines)


def _parse_lines(lines):
    """
    Helper function to parse lines into the dictionary structure.
    """
    root = {"__content__": []}
    stack = [(0, root)]  # (level, current_dict)

    in_code_block = False
    in_table = False
    in_math_block = False
    in_front_matter = False
    
    # Front matter must be at the very beginning (ignoring blank lines)
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip():
            start_index = i
            break
            
    if start_index < len(lines) and lines[start_index].strip() == '---':
        in_front_matter = True
        
    for i, line in enumerate(lines):
        if i < start_index:
            continue
            
        stripped_line = line.strip()
        
        # Check for code block toggle
        if stripped_line.startswith('```'):
            in_code_block = not in_code_block
            
        # Check for math block toggle
        if stripped_line == '$$':
            in_math_block = not in_math_block
            
        # Check for front matter toggle
        if stripped_line == '---':
            if i == start_index:
                in_front_matter = True
            elif in_front_matter:
                in_front_matter = False
                # If we just closed front matter, this line is not a header
                
        # Check for table delimiter (only if not in code/math/front matter)
        if not in_code_block and not in_math_block and not in_front_matter:
            # Check for blank line to end table
            if not stripped_line:
                in_table = False
            elif "|" in stripped_line and "-" in stripped_line:
                if re.match(r'^[\s|:-]+$', stripped_line):
                    in_table = True

        header_match = re.match(r'^(#+)\s+(.*)', stripped_line)
        if header_match and not in_code_block and not in_table and not in_math_block and not in_front_matter:
            level = len(header_match.group(1))
            title = header_match.group(2).strip()

            # Pop stack
            while stack and stack[-1][0] >= level:
                stack.pop()

            parent_node = stack[-1][1]

            new_node = {"__content__": []}
            new_node["__header_line__"] = line  # Store the original header line
            parent_node[title] = new_node
            stack.append((level, new_node))
        else:
            # Append line to current node's content
            stack[-1][1]["__content__"].append(line)

    return root

