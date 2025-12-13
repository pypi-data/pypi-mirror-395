"""
AsciiDoc Table Parser Module

Parses AsciiDoc tables and extracts structured data. Designed to be reusable
for various table conversion tasks (not just callout explanations).

Handles:
- Two-column tables with callout numbers and explanations
- Conditional statements (ifdef, ifndef, endif) within table cells
- Multi-line table cells
- Table attributes and formatting
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TableCell:
    """Represents a single table cell with its content and any conditional blocks."""
    content: List[str]  # Lines of content in the cell
    conditionals: List[str]  # Any ifdef/ifndef/endif lines associated with this cell


@dataclass
class TableRow:
    """Represents a table row with cells."""
    cells: List[TableCell]
    conditionals_before: List[str]  # Conditional statements before this row
    conditionals_after: List[str]  # Conditional statements after this row


@dataclass
class AsciiDocTable:
    """Represents a complete AsciiDoc table."""
    start_line: int
    end_line: int
    attributes: str  # Table attributes like [cols="1,3"]
    rows: List[TableRow]
    title: str = ""  # Block title like ".Table description"


class TableParser:
    """Parses AsciiDoc tables and extracts structured data."""

    # Pattern for table start delimiter with optional attributes
    TABLE_START = re.compile(r'^\[.*?\]$')
    TABLE_DELIMITER = re.compile(r'^\|===\s*$')

    # Pattern for table cell separator (| or cell type specifier like a|, s|, etc.)
    CELL_SEPARATOR = re.compile(r'^(\||[ashdmev]\|)')

    # Pattern for conditional directives
    IFDEF_PATTERN = re.compile(r'^(ifdef::|ifndef::).+\[\]\s*$')
    ENDIF_PATTERN = re.compile(r'^endif::\[\]\s*$')

    # Pattern for callout number (used for callout table detection)
    CALLOUT_NUMBER = re.compile(r'^<(\d+)>\s*$')
    PLAIN_NUMBER = re.compile(r'^(\d+)\s*$')

    def _is_callout_or_number(self, text: str) -> tuple[bool, int]:
        """
        Check if text is a callout number (<1>) or plain number (1).
        Returns (is_match, number) or (False, 0) if no match.
        """
        text = text.strip()

        # Try callout format first: <1>
        match = self.CALLOUT_NUMBER.match(text)
        if match:
            return (True, int(match.group(1)))

        # Try plain number format: 1
        match = self.PLAIN_NUMBER.match(text)
        if match:
            return (True, int(match.group(1)))

        return (False, 0)

    def _finalize_row_if_complete(self, current_row_cells, conditionals_before_row,
                                   conditionals_after_row, expected_columns, rows):
        """
        Check if we have enough cells for a complete row, and if so, save it.

        Returns: (new_current_row_cells, new_conditionals_before, new_conditionals_after)
        """
        if expected_columns > 0 and len(current_row_cells) >= expected_columns:
            # Row is complete - save it
            rows.append(TableRow(
                cells=current_row_cells.copy(),
                conditionals_before=conditionals_before_row.copy(),
                conditionals_after=conditionals_after_row.copy()
            ))
            return [], [], []  # Reset for next row

        # Row not complete yet
        return current_row_cells, conditionals_before_row, conditionals_after_row

    def _parse_column_count(self, attributes: str) -> int:
        """
        Parse the cols attribute to determine number of columns.

        Example: '[cols="1,7a"]' returns 2
                 '[cols="1,2,3"]' returns 3
        """
        import re
        # Match cols="..." or cols='...'
        match = re.search(r'cols=["\']([^"\']+)["\']', attributes)
        if not match:
            return 0  # Unknown column count

        cols_spec = match.group(1)
        # Count comma-separated values
        # Handle formats like: "1,2", "1a,2a", "1,2,3", etc.
        columns = cols_spec.split(',')
        return len(columns)

    def find_tables(self, lines: List[str]) -> List[AsciiDocTable]:
        """Find all tables in the document."""
        tables = []
        i = 0

        while i < len(lines):
            # Look for table delimiter
            if self.TABLE_DELIMITER.match(lines[i]):
                # Check for attributes and title before the table
                attributes = ""
                title = ""
                start_line = i

                # Check line before delimiter for attributes [cols="..."]
                if i > 0 and self.TABLE_START.match(lines[i - 1]):
                    attributes = lines[i - 1]
                    start_line = i - 1

                    # Check line before attributes for title .Title
                    if i > 1 and lines[i - 2].strip().startswith('.') and not lines[i - 2].strip().startswith('..'):
                        title = lines[i - 2].strip()
                        start_line = i - 2
                elif i > 0 and lines[i - 1].strip().startswith('.') and not lines[i - 1].strip().startswith('..'):
                    # Title directly before delimiter (no attributes)
                    title = lines[i - 1].strip()
                    start_line = i - 1

                # Parse table content
                table = self._parse_table(lines, start_line, i, title)
                if table:
                    tables.append(table)
                    i = table.end_line + 1
                    continue
            i += 1

        return tables

    def _parse_table(self, lines: List[str], start_line: int, delimiter_line: int, title: str = "") -> Optional[AsciiDocTable]:
        """
        Parse a single table starting at the delimiter.

        AsciiDoc table format:
        .Optional title
        [optional attributes]
        |===
        |Cell1
        |Cell2
        (blank line separates rows)
        |Cell3
        |Cell4
        |===
        """
        # Get attributes and parse column count
        attributes = ""
        if start_line < delimiter_line:
            # Check if start line is title or attributes
            start_content = lines[start_line].strip()
            if start_content.startswith('.') and not start_content.startswith('..'):
                # Start line is title, attributes might be on next line
                if start_line + 1 < delimiter_line:
                    attributes = lines[start_line + 1]
            else:
                # Start line is attributes
                attributes = lines[start_line]

        expected_columns = self._parse_column_count(attributes)

        i = delimiter_line + 1
        rows = []
        current_row_cells = []
        current_cell_lines = []
        conditionals_before_row = []
        conditionals_after_row = []
        in_asciidoc_cell = False  # Track if we're in an a| (AsciiDoc) cell

        while i < len(lines):
            line = lines[i]

            # Check for table end
            if self.TABLE_DELIMITER.match(line):
                # Save any pending cell
                if current_cell_lines:
                    current_row_cells.append(TableCell(
                        content=current_cell_lines.copy(),
                        conditionals=[]
                    ))
                    current_cell_lines = []

                # Save any pending row
                if current_row_cells:
                    rows.append(TableRow(
                        cells=current_row_cells.copy(),
                        conditionals_before=conditionals_before_row.copy(),
                        conditionals_after=conditionals_after_row.copy()
                    ))

                # Get attributes if present (already extracted above)
                return AsciiDocTable(
                    start_line=start_line,
                    end_line=i,
                    attributes=attributes,
                    rows=rows,
                    title=title
                )

            # Check for conditional directives
            if self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line):
                # If we're building a cell (current_cell_lines is not empty) OR
                # we're in an AsciiDoc cell, add conditional to cell content
                if current_cell_lines or in_asciidoc_cell:
                    # Inside a cell - conditional is part of cell content
                    current_cell_lines.append(line)
                elif current_row_cells:
                    # Between cells in the same row
                    conditionals_after_row.append(line)
                else:
                    # Conditional before any cells in this row
                    conditionals_before_row.append(line)
                i += 1
                continue

            # Blank line handling
            if not line.strip():
                # In AsciiDoc cells (a|), blank lines are part of cell content
                if in_asciidoc_cell:
                    current_cell_lines.append(line)
                    i += 1
                    continue

                # Otherwise, blank line separates rows
                # Save pending cell if exists
                if current_cell_lines:
                    current_row_cells.append(TableCell(
                        content=current_cell_lines.copy(),
                        conditionals=[]
                    ))
                    current_cell_lines = []
                    in_asciidoc_cell = False

                # Save row if we have cells
                if current_row_cells:
                    rows.append(TableRow(
                        cells=current_row_cells.copy(),
                        conditionals_before=conditionals_before_row.copy(),
                        conditionals_after=conditionals_after_row.copy()
                    ))
                    current_row_cells = []
                    conditionals_before_row = []
                    conditionals_after_row = []

                i += 1
                continue

            # Check for cell separator (|) or cell type specifier (a|, s|, etc.)
            if self.CELL_SEPARATOR.match(line):
                # Determine if line starts with | or with a cell type specifier
                if line.startswith('|'):
                    # Standard cell separator
                    cell_content = line[1:]  # Remove leading |
                else:
                    # Cell type specifier without leading | (e.g., "a|text")
                    cell_content = line

                # Save previous cell if exists
                if current_cell_lines:
                    current_row_cells.append(TableCell(
                        content=current_cell_lines.copy(),
                        conditionals=[]
                    ))
                    current_cell_lines = []
                    in_asciidoc_cell = False  # Reset for next cell

                    # Check if row is complete (have enough cells based on cols attribute)
                    current_row_cells, conditionals_before_row, conditionals_after_row = \
                        self._finalize_row_if_complete(
                            current_row_cells, conditionals_before_row,
                            conditionals_after_row, expected_columns, rows
                        )

                # Check for cell type specifier (a|, s|, etc.)
                # Type specifiers are single characters followed by |
                if len(cell_content) > 1 and cell_content[0] in 'ashdmev' and cell_content[1] == '|':
                    # Track if this is an AsciiDoc cell (a|)
                    if cell_content[0] == 'a':
                        in_asciidoc_cell = True
                    cell_content = cell_content[2:]  # Remove type specifier and |

                cell_content = cell_content.strip()

                # Check if there are multiple cells on the same line (e.g., |Cell1 |Cell2 |Cell3)
                if '|' in cell_content:
                    # Split by | to get multiple cells
                    parts = cell_content.split('|')
                    for part in parts:
                        part = part.strip()
                        if part:  # Skip empty parts
                            current_row_cells.append(TableCell(
                                content=[part],
                                conditionals=[]
                            ))

                    # Multi-cell line completes a row - finalize it
                    if current_row_cells:
                        rows.append(TableRow(
                            cells=current_row_cells.copy(),
                            conditionals_before=conditionals_before_row.copy(),
                            conditionals_after=conditionals_after_row.copy()
                        ))
                        current_row_cells = []
                        conditionals_before_row = []
                        conditionals_after_row = []
                else:
                    # Single cell on this line
                    if cell_content:
                        current_cell_lines.append(cell_content)
                    # If empty, just start a new cell with no content yet

                i += 1
                continue

            # Check for cell type specifier on its own line (e.g., "a|", "s|", "h|")
            # This is actually a cell SEPARATOR with type specifier
            # Example:
            #   |<1>          ← Cell 1
            #   a|            ← Start cell 2 with type 'a' (AsciiDoc)
            #   content...    ← Cell 2 content
            stripped_line = line.strip()
            if (len(stripped_line) == 2 and
                stripped_line[0] in 'ashdmev' and
                stripped_line[1] == '|' and
                (current_cell_lines or current_row_cells)):
                # Save previous cell if we have one
                if current_cell_lines:
                    current_row_cells.append(TableCell(
                        content=current_cell_lines.copy(),
                        conditionals=[]
                    ))
                    current_cell_lines = []

                    # Check if row is complete
                    current_row_cells, conditionals_before_row, conditionals_after_row = \
                        self._finalize_row_if_complete(
                            current_row_cells, conditionals_before_row,
                            conditionals_after_row, expected_columns, rows
                        )

                # Set cell type for the NEW cell we're starting
                if stripped_line[0] == 'a':
                    in_asciidoc_cell = True
                # Start collecting content for the new cell (no content on this line)
                i += 1
                continue

            # Regular content line (continuation of current cell)
            if current_cell_lines or current_row_cells:
                current_cell_lines.append(line)

            i += 1

        # Return None if we didn't find a proper table end
        return None

    def is_callout_table(self, table: AsciiDocTable) -> bool:
        """
        Determine if a table is a callout explanation table.
        A callout table has two columns: callout number and explanation.
        Accepts both callout format (<1>) and plain numbers (1).
        Skips header rows if present.
        """
        if not table.rows:
            return False

        # Check if all rows have exactly 2 cells
        if not all(len(row.cells) == 2 for row in table.rows):
            return False

        # Determine if there's a header row and skip it
        has_header = self._has_header_row(table)
        data_rows = table.rows[1:] if has_header else table.rows

        if not data_rows:
            return False

        # Check if first cell of each data row is a callout number (either <1> or 1)
        for row in data_rows:
            first_cell = row.cells[0]
            if not first_cell.content:
                return False

            # First line of first cell should be a callout number or plain number
            first_line = first_cell.content[0].strip()
            is_match, _ = self._is_callout_or_number(first_line)
            if not is_match:
                return False

        return True

    def _has_header_row(self, table: AsciiDocTable) -> bool:
        """
        Check if table has a header row.
        Common header patterns: "Item", "Value", "Description", "Column", etc.

        A row is a header if:
        - It does NOT start with a callout number (<1> or 1)
        - It contains common header keywords in the cells
        """
        if not table.rows:
            return False

        first_row = table.rows[0]
        if not first_row.cells or len(first_row.cells) < 2:
            return False

        # If first cell is a callout number, this is NOT a header
        first_cell = first_row.cells[0]
        if first_cell.content:
            first_cell_text = first_cell.content[0].strip()
            is_callout, _ = self._is_callout_or_number(first_cell_text)
            if is_callout:
                return False

        # Collect text from all cells in first row
        header_text = ' '.join(
            cell.content[0] if cell.content else ''
            for cell in first_row.cells
        ).lower()

        # Check for common header keywords (as whole words)
        header_keywords = ['item', 'description', 'value', 'column', 'parameter', 'field', 'name']
        import re
        return any(re.search(r'\b' + re.escape(keyword) + r'\b', header_text) for keyword in header_keywords)

    def is_3column_callout_table(self, table: AsciiDocTable) -> bool:
        """
        Determine if a table is a 3-column callout explanation table.
        Format: Item (number) | Value | Description

        This format is used in some documentation (e.g., Debezium) where:
        - Column 1: Item number (1, 2, 3...) corresponding to callout numbers
        - Column 2: The value/code being explained
        - Column 3: Description/explanation text
        """
        if not table.rows:
            return False

        # Determine if there's a header row
        has_header = self._has_header_row(table)
        data_rows = table.rows[1:] if has_header else table.rows

        if not data_rows:
            return False

        # Check if all data rows have exactly 3 cells
        if not all(len(row.cells) == 3 for row in data_rows):
            return False

        # Check if first cell of each data row contains a callout or plain number (1, 2, 3... or <1>, <2>...)
        for row in data_rows:
            first_cell = row.cells[0]
            if not first_cell.content:
                return False

            # First line of first cell should be a callout number or plain number
            first_line = first_cell.content[0].strip()
            is_match, _ = self._is_callout_or_number(first_line)
            if not is_match:
                return False

        return True

    def get_table_callout_numbers(self, table: AsciiDocTable) -> List[int]:
        """
        Extract just the callout numbers from a table (in order, with duplicates).
        Used for validation and diagnostics.

        Returns:
            List of callout numbers in the order they appear in the table.
            Preserves duplicates to help identify table errors.
        """
        callout_numbers = []

        # Determine if there's a header row and skip it
        has_header = self._has_header_row(table)
        data_rows = table.rows[1:] if has_header else table.rows

        for row in data_rows:
            # Handle both 2-column and 3-column tables
            if len(row.cells) < 2:
                continue

            first_cell = row.cells[0]
            if not first_cell.content:
                continue

            # Extract callout number (supports both <1> and 1 formats)
            first_line = first_cell.content[0].strip()
            is_match, callout_num = self._is_callout_or_number(first_line)
            if is_match:
                callout_numbers.append(callout_num)

        return callout_numbers

    def extract_callout_explanations_from_table(self, table: AsciiDocTable) -> Dict[int, Tuple[List[str], List[str]]]:
        """
        Extract callout explanations from a table.
        Returns dict mapping callout number to tuple of (explanation_lines, conditionals).

        The conditionals list includes any ifdef/ifndef/endif statements that should
        be preserved when converting the table to other formats.

        Accepts both callout format (<1>) and plain numbers (1).
        Skips header rows if present.

        Note: If table contains duplicate callout numbers, the last one wins.
        Use get_table_callout_numbers() to detect duplicates.
        """
        explanations = {}

        # Determine if there's a header row and skip it
        has_header = self._has_header_row(table)
        data_rows = table.rows[1:] if has_header else table.rows

        for row in data_rows:
            if len(row.cells) != 2:
                continue

            callout_cell = row.cells[0]
            explanation_cell = row.cells[1]

            # Extract callout number (supports both <1> and 1 formats)
            first_line = callout_cell.content[0].strip()
            is_match, callout_num = self._is_callout_or_number(first_line)
            if not is_match:
                continue

            # Collect explanation lines, preserving blank lines and conditionals inline
            # Blank lines will need to become continuation markers (+) in definition lists
            explanation_lines = []
            for line in explanation_cell.content:
                # Preserve ALL lines including conditionals and blank lines
                # Empty lines will be marked as '' which signals need for continuation marker
                explanation_lines.append(line)

            # Collect conditionals that appear before/after the row
            row_conditionals = []
            row_conditionals.extend(row.conditionals_before)
            row_conditionals.extend(row.conditionals_after)

            explanations[callout_num] = (explanation_lines, row_conditionals)

        return explanations

    def extract_3column_callout_explanations(self, table: AsciiDocTable) -> Dict[int, Tuple[List[str], List[str], List[str]]]:
        """
        Extract callout explanations from a 3-column table.
        Returns dict mapping callout number to tuple of (value_lines, description_lines, conditionals).

        Format: Item | Value | Description
        - Item: Number (1, 2, 3...) or callout (<1>, <2>...) corresponding to callout number
        - Value: The code/value being explained
        - Description: Explanation text

        The conditionals list includes any ifdef/ifndef/endif statements that should
        be preserved when converting the table to other formats.

        Accepts both callout format (<1>) and plain numbers (1).
        """
        explanations = {}

        # Determine if there's a header row and skip it
        has_header = self._has_header_row(table)
        data_rows = table.rows[1:] if has_header else table.rows

        for row in data_rows:
            if len(row.cells) != 3:
                continue

            item_cell = row.cells[0]
            value_cell = row.cells[1]
            desc_cell = row.cells[2]

            # Extract item number (maps to callout number) - supports both <1> and 1 formats
            if not item_cell.content:
                continue

            item_num_str = item_cell.content[0].strip()
            is_match, callout_num = self._is_callout_or_number(item_num_str)
            if not is_match:
                continue

            # Collect value lines (column 2), preserving all content including conditionals
            value_lines = []
            for line in value_cell.content:
                value_lines.append(line)

            # Collect description lines (column 3), preserving all content including conditionals
            description_lines = []
            for line in desc_cell.content:
                description_lines.append(line)

            # Collect conditionals that appear before/after the row
            row_conditionals = []
            row_conditionals.extend(row.conditionals_before)
            row_conditionals.extend(row.conditionals_after)

            explanations[callout_num] = (value_lines, description_lines, row_conditionals)

        return explanations

    def find_callout_table_after_code_block(self, lines: List[str], code_block_end: int) -> Optional[AsciiDocTable]:
        """
        Find a callout explanation table that appears after a code block.

        Args:
            lines: All lines in the document
            code_block_end: Line number where the code block ends

        Returns:
            AsciiDocTable if a callout table is found, None otherwise
        """
        # Skip the closing delimiter of the code block (----, ...., etc.)
        i = code_block_end + 1
        if i < len(lines) and lines[i].strip() in ['----', '....', '====']:
            i += 1

        # Skip blank lines and continuation markers after code block
        while i < len(lines) and (not lines[i].strip() or lines[i].strip() == '+'):
            i += 1

        # Look for a table starting within the next few lines
        # (allowing for possible text between code block and table)
        search_limit = min(i + 10, len(lines))

        for j in range(i, search_limit):
            line = lines[j]

            # If we encounter a list-format callout explanation, stop
            # (list format takes precedence over table format further away)
            if self.CALLOUT_NUMBER.match(line.strip()):
                return None

            # If we encounter another code block start, stop
            if line.strip() in ['----', '....'] or line.strip().startswith('[source'):
                return None

            # Check for table delimiter
            if self.TABLE_DELIMITER.match(line):
                # Found a table, extract attributes and title
                attributes = ""
                title = ""
                start_line = j

                # Check line before delimiter for attributes [cols="..."]
                if j > 0 and self.TABLE_START.match(lines[j - 1]):
                    attributes = lines[j - 1]
                    start_line = j - 1

                    # Check line before attributes for title .Title
                    if j > 1 and lines[j - 2].strip().startswith('.') and not lines[j - 2].strip().startswith('..'):
                        title = lines[j - 2].strip()
                        start_line = j - 2
                elif j > 0 and lines[j - 1].strip().startswith('.') and not lines[j - 1].strip().startswith('..'):
                    # Title directly before delimiter (no attributes)
                    title = lines[j - 1].strip()
                    start_line = j - 1

                table = self._parse_table(lines, start_line, j, title)
                if table and (self.is_callout_table(table) or self.is_3column_callout_table(table)):
                    return table

                # If we found a table but it's not a callout table, stop searching
                break

        return None

    def convert_table_to_deflist(self, table: AsciiDocTable, preserve_conditionals: bool = True) -> List[str]:
        """
        Convert a two-column table to an AsciiDoc definition list.

        Args:
            table: The table to convert
            preserve_conditionals: Whether to preserve ifdef/ifndef/endif statements

        Returns:
            List of lines representing the definition list
        """
        output = []

        for row in table.rows:
            if len(row.cells) != 2:
                continue

            # Add conditionals before row
            if preserve_conditionals and row.conditionals_before:
                output.extend(row.conditionals_before)

            # First cell is the term
            term_lines = row.cells[0].content
            if term_lines:
                output.append(term_lines[0])

            # Second cell is the definition
            definition_lines = row.cells[1].content
            if definition_lines:
                # Filter out conditionals if needed
                if preserve_conditionals:
                    for line in definition_lines:
                        if self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line):
                            output.append(line)
                        else:
                            output.append(f"  {line}")
                else:
                    for line in definition_lines:
                        if not (self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line)):
                            output.append(f"  {line}")

            # Add conditionals after row
            if preserve_conditionals and row.conditionals_after:
                output.extend(row.conditionals_after)

            # Add blank line between entries
            output.append("")

        # Remove trailing blank line
        if output and not output[-1].strip():
            output.pop()

        return output

    def convert_table_to_bullets(self, table: AsciiDocTable, preserve_conditionals: bool = True) -> List[str]:
        """
        Convert a two-column table to a bulleted list.

        Args:
            table: The table to convert
            preserve_conditionals: Whether to preserve ifdef/ifndef/endif statements

        Returns:
            List of lines representing the bulleted list
        """
        output = []

        for row in table.rows:
            if len(row.cells) != 2:
                continue

            # Add conditionals before row
            if preserve_conditionals and row.conditionals_before:
                output.extend(row.conditionals_before)

            # Get the term (first cell)
            term_lines = row.cells[0].content
            term = term_lines[0] if term_lines else ""

            # Get the definition (second cell)
            definition_lines = row.cells[1].content

            # Filter conditionals from definition if needed
            filtered_def_lines = []
            inline_conditionals = []

            for line in definition_lines:
                if self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line):
                    if preserve_conditionals:
                        inline_conditionals.append(line)
                else:
                    filtered_def_lines.append(line)

            # Create bullet item
            if filtered_def_lines:
                first_line = filtered_def_lines[0]
                output.append(f"* *{term}*: {first_line}")

                # Add continuation lines with proper indentation
                for line in filtered_def_lines[1:]:
                    output.append(f"  {line}")

                # Add inline conditionals if present
                if preserve_conditionals and inline_conditionals:
                    output.extend(inline_conditionals)

            # Add conditionals after row
            if preserve_conditionals and row.conditionals_after:
                output.extend(row.conditionals_after)

        return output
