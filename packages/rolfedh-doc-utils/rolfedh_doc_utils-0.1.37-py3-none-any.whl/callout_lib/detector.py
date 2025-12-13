"""
Callout Detection Module

Detects code blocks with callouts and extracts callout information from AsciiDoc files.
Supports both list-format and table-format callout explanations.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from .table_parser import TableParser


@dataclass
class Callout:
    """Represents a callout with its number and explanation text."""
    number: int
    lines: List[str]  # List of lines to preserve formatting
    is_optional: bool = False


@dataclass
class CalloutGroup:
    """Represents one or more callouts that share the same code line."""
    code_line: str  # The actual code line (without callouts)
    callout_numbers: List[int]  # List of callout numbers on this line


@dataclass
class CodeBlock:
    """Represents a code block with its content and metadata."""
    start_line: int
    end_line: int
    delimiter: str
    content: List[str]
    language: Optional[str] = None


class CalloutDetector:
    """Detects and extracts callout information from AsciiDoc code blocks."""

    # Pattern for code block start: [source,language] or [source] with optional attributes
    CODE_BLOCK_START = re.compile(r'^\[source(?:,\s*(\w+))?(?:[,\s]+[^\]]+)?\]')

    # Pattern for callout number in code block (can appear multiple times per line)
    CALLOUT_IN_CODE = re.compile(r'<(\d+)>')

    # Pattern for callout with optional preceding comment syntax
    # Matches common comment styles: //, #, --, followed by optional whitespace and <number>
    # Note: Semicolon (;) removed because it's a statement terminator in Java/C/C++/JavaScript
    # and causes false positives (e.g., "name; <1>" would incorrectly remove the semicolon)
    CALLOUT_WITH_COMMENT = re.compile(r'\s*(?://|#|--)\s*<\d+>|\s*<\d+>')

    # Pattern for callout explanation line: <1> Explanation text
    CALLOUT_EXPLANATION = re.compile(r'^<(\d+)>\s+(.+)$')

    # Pattern to detect user-replaceable values in angle brackets
    # Excludes heredoc syntax (<<) and comparison operators
    USER_VALUE_PATTERN = re.compile(r'(?<!<)<([a-zA-Z][^>]*)>')

    def __init__(self):
        """Initialize detector with table parser."""
        self.table_parser = TableParser()
        self.last_table_title = ""  # Track title from most recent table extraction
        self.last_table = None  # Track last table found for validation diagnostics

    def find_code_blocks(self, lines: List[str]) -> List[CodeBlock]:
        """Find all code blocks in the document."""
        blocks = []
        i = 0

        while i < len(lines):
            # Check for [source] prefix first
            match = self.CODE_BLOCK_START.match(lines[i])
            if match:
                language = match.group(1)
                start = i
                i += 1

                # Find the delimiter line (---- or ....)
                if i < len(lines) and lines[i].strip() in ['----', '....']:
                    delimiter = lines[i].strip()
                    i += 1
                    content_start = i

                    # Find the closing delimiter
                    while i < len(lines):
                        if lines[i].strip() == delimiter:
                            content = lines[content_start:i]
                            blocks.append(CodeBlock(
                                start_line=start,
                                end_line=i,
                                delimiter=delimiter,
                                content=content,
                                language=language
                            ))
                            break
                        i += 1
            # Check for plain delimited blocks without [source] prefix
            elif lines[i].strip() in ['----', '....']:
                delimiter = lines[i].strip()
                start = i
                i += 1
                content_start = i

                # Find the closing delimiter
                while i < len(lines):
                    if lines[i].strip() == delimiter:
                        content = lines[content_start:i]
                        # Only add if block contains callouts
                        if any(self.CALLOUT_IN_CODE.search(line) for line in content):
                            blocks.append(CodeBlock(
                                start_line=start,
                                end_line=i,
                                delimiter=delimiter,
                                content=content,
                                language=None
                            ))
                        break
                    i += 1
            i += 1

        return blocks

    def extract_callouts_from_code(self, content: List[str]) -> List[CalloutGroup]:
        """
        Extract callout numbers from code block content.
        Returns list of CalloutGroups, where each group contains:
        - The code line (with user-replaceable value if found, or full line)
        - List of callout numbers on that line

        Multiple callouts on the same line are grouped together to be merged
        in the definition list.
        """
        groups = []

        for line in content:
            # Look for all callout numbers on this line
            callout_matches = list(self.CALLOUT_IN_CODE.finditer(line))
            if callout_matches:
                # Remove callouts AND preceding comment syntax from the line
                # Use CALLOUT_WITH_COMMENT to remove both comment syntax and callout
                line_without_callouts = self.CALLOUT_WITH_COMMENT.sub('', line).rstrip()

                # COMMENTED OUT: User-replaceable value detection causes false positives
                # with Java generics (e.g., <MyEntity, Integer>) and other valid syntax
                # that uses angle brackets. Always use the full code line.
                #
                # # Find all angle-bracket enclosed values
                # user_values = self.USER_VALUE_PATTERN.findall(line_without_callouts)
                #
                # # Determine what to use as the code line term
                # if user_values:
                #     # Use the rightmost (closest to the callout) user value
                #     code_line = user_values[-1]
                # else:
                #     # No angle-bracket value found - use the actual code line
                #     code_line = line_without_callouts

                # Always use the full code line
                code_line = line_without_callouts

                # Collect all callout numbers on this line
                callout_nums = [int(m.group(1)) for m in callout_matches]

                groups.append(CalloutGroup(
                    code_line=code_line,
                    callout_numbers=callout_nums
                ))

        return groups

    def extract_callout_explanations(self, lines: List[str], start_line: int) -> Tuple[Dict[int, Callout], int]:
        """
        Extract callout explanations following a code block.
        Supports list-format (<1> text), 2-column table, and 3-column table formats.
        Returns dict of callouts and the line number where explanations end.
        """
        # First, try to find a table-format callout explanation
        table = self.table_parser.find_callout_table_after_code_block(lines, start_line)
        if table:
            # Check if it's a 3-column table (Item | Value | Description)
            if self.table_parser.is_3column_callout_table(table):
                return self._extract_from_3column_table(table)
            # Check if it's a 2-column table (<callout> | explanation)
            elif self.table_parser.is_callout_table(table):
                return self._extract_from_table(table)

        # Fall back to list-format extraction
        return self._extract_from_list(lines, start_line)

    def _extract_from_table(self, table) -> Tuple[Dict[int, Callout], int]:
        """Extract callout explanations from a table format."""
        # Store table for use by converters and validation
        self.last_table = table
        self.last_table_title = table.title if hasattr(table, 'title') else ""

        explanations = {}
        table_data = self.table_parser.extract_callout_explanations_from_table(table)

        for callout_num, (explanation_lines, row_conditionals) in table_data.items():
            # explanation_lines now includes blank lines and conditionals inline
            # row_conditionals are before/after the entire row (rarely used)
            all_lines = []

            # Add any row-level conditionals before
            if row_conditionals:
                all_lines.extend(row_conditionals)

            # Add explanation lines (already includes inline conditionals and blank lines)
            all_lines.extend(explanation_lines)

            # Check if marked as optional
            is_optional = False
            if all_lines and (all_lines[0].lower().startswith('optional.') or
                             all_lines[0].lower().startswith('optional:')):
                is_optional = True
                all_lines[0] = all_lines[0][9:].strip()
            elif all_lines and ('(Optional)' in all_lines[0] or '(optional)' in all_lines[0]):
                is_optional = True
                all_lines[0] = re.sub(r'\s*\(optional\)\s*', ' ', all_lines[0], flags=re.IGNORECASE).strip()

            explanations[callout_num] = Callout(callout_num, all_lines, is_optional)

        return explanations, table.end_line

    def _extract_from_3column_table(self, table) -> Tuple[Dict[int, Callout], int]:
        """
        Extract callout explanations from a 3-column table format.
        Format: Item (number) | Value | Description
        """
        # Store table for use by converters and validation
        self.last_table = table
        self.last_table_title = table.title if hasattr(table, 'title') else ""

        explanations = {}
        table_data = self.table_parser.extract_3column_callout_explanations(table)

        for callout_num, (value_lines, description_lines, row_conditionals) in table_data.items():
            # Combine value and description into explanation lines
            # Both value_lines and description_lines now include conditionals and blank lines inline
            all_lines = []

            # Add any row-level conditionals before
            if row_conditionals:
                all_lines.extend(row_conditionals)

            # Add value lines with context
            if value_lines:
                # Format: "`value`:"
                value_text = value_lines[0] if value_lines else ""
                # If value is code-like (contains backticks or special chars), keep it formatted
                if value_text:
                    all_lines.append(f"{value_text}:")

                # Add additional value lines if multi-line (includes conditionals and blank lines)
                for line in value_lines[1:]:
                    all_lines.append(line)

            # Add description lines (already includes conditionals and blank lines)
            all_lines.extend(description_lines)

            # Check if marked as optional
            is_optional = False
            if all_lines and (all_lines[0].lower().startswith('optional.') or
                             all_lines[0].lower().startswith('optional:') or
                             'optional' in all_lines[0].lower()[:50]):  # Check first 50 chars
                is_optional = True
                # Don't remove "optional" text - it's part of the description

            explanations[callout_num] = Callout(callout_num, all_lines, is_optional)

        return explanations, table.end_line

    def _extract_from_list(self, lines: List[str], start_line: int) -> Tuple[Dict[int, Callout], int]:
        """Extract callout explanations from list format (<1> text)."""
        # Clear table data since list format doesn't have tables
        self.last_table = None
        self.last_table_title = ""

        explanations = {}
        i = start_line + 1  # Start after the closing delimiter

        # Skip blank lines and continuation markers (+)
        while i < len(lines) and (not lines[i].strip() or lines[i].strip() == '+'):
            i += 1

        # Collect consecutive callout explanation lines
        while i < len(lines):
            match = self.CALLOUT_EXPLANATION.match(lines[i])
            if match:
                num = int(match.group(1))
                first_line = match.group(2).strip()
                explanation_lines = [first_line]
                i += 1

                # Collect continuation lines (lines that don't start with a new callout)
                # Continue until we hit a blank line, a new callout, or certain patterns
                while i < len(lines):
                    line = lines[i]
                    # Stop if we hit a blank line, new callout, or list start marker
                    if not line.strip() or self.CALLOUT_EXPLANATION.match(line) or line.startswith('[start='):
                        break
                    # Add continuation line preserving original formatting
                    explanation_lines.append(line)
                    i += 1

                # Check if marked as optional (only in first line)
                is_optional = False
                if first_line.lower().startswith('optional.') or first_line.lower().startswith('optional:'):
                    is_optional = True
                    # Remove "Optional." or "Optional:" from first line
                    explanation_lines[0] = first_line[9:].strip()
                elif '(Optional)' in first_line or '(optional)' in first_line:
                    is_optional = True
                    explanation_lines[0] = re.sub(r'\s*\(optional\)\s*', ' ', first_line, flags=re.IGNORECASE).strip()

                explanations[num] = Callout(num, explanation_lines, is_optional)
            else:
                break

        return explanations, i - 1

    def remove_callouts_from_code(self, content: List[str]) -> List[str]:
        """
        Remove callout numbers and preceding comment syntax from code block content.
        Handles multiple callouts per line and various comment styles (//,  #, --, ;).
        """
        cleaned = []
        for line in content:
            # Remove all callout numbers with their preceding comment syntax
            cleaned.append(self.CALLOUT_WITH_COMMENT.sub('', line).rstrip())
        return cleaned

    def validate_callouts(self, callout_groups: List[CalloutGroup], explanations: Dict[int, Callout]) -> Tuple[bool, List[int], List[int]]:
        """
        Validate that callout numbers in code match explanation numbers.
        Returns tuple of (is_valid, code_nums_list, explanation_nums_list).

        Returns:
            - is_valid: True if unique callout numbers match
            - code_nums_list: List of callout numbers from code (unique, sorted)
            - explanation_nums_list: List of callout numbers from explanations
              (preserves duplicates if from table, sorted)
        """
        # Extract unique callout numbers from code groups
        code_nums_set = set()
        for group in callout_groups:
            code_nums_set.update(group.callout_numbers)

        # Get explanation numbers, preserving duplicates if from a table
        if self.last_table:
            # Use table parser to get raw callout numbers (with duplicates)
            explanation_nums_list = self.table_parser.get_table_callout_numbers(self.last_table)
        else:
            # List format: dict keys are already unique
            explanation_nums_list = list(explanations.keys())

        explanation_nums_set = set(explanation_nums_list)

        # Validation compares unique numbers only
        is_valid = code_nums_set == explanation_nums_set

        return is_valid, sorted(code_nums_set), sorted(explanation_nums_list)
