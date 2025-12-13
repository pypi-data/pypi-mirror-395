"""
Definition List Converter Module

Converts callouts to AsciiDoc definition list format with "where:" prefix.
"""

import re
from typing import List, Dict
from .detector import CalloutGroup, Callout


class DefListConverter:
    """Converts callouts to definition list format."""

    # Pattern to detect user-replaceable values in angle brackets
    USER_VALUE_PATTERN = re.compile(r'(?<!<)<([a-zA-Z][^>]*)>')

    @staticmethod
    def convert(callout_groups: List[CalloutGroup], explanations: Dict[int, Callout], table_title: str = "",
                definition_prefix: str = "") -> List[str]:
        """
        Create definition list from callout groups and explanations.

        For callouts with user-replaceable values in angle brackets, uses those.
        For callouts without values, uses the actual code line as the term.

        When multiple callouts share the same code line (same group), their
        explanations are merged using AsciiDoc list continuation (+).

        Args:
            callout_groups: List of CalloutGroup objects from code block
            explanations: Dict mapping callout numbers to Callout objects
            table_title: Optional table title (e.g., ".Descriptions of delete event")
                        Will be converted to lead-in sentence (e.g., "Descriptions of delete event, where:")
            definition_prefix: Optional prefix to add before each definition (e.g., "Specifies ")

        Returns:
            List of strings representing the definition list
        """
        # Convert table title to lead-in sentence if present
        if table_title:
            # Remove leading dot and trailing period if present
            title_text = table_title.lstrip('.').rstrip('.')
            lines = [f'\n{title_text}, where:']
        else:
            lines = ['\nwhere:']

        # Process each group (which may contain one or more callouts)
        for group in callout_groups:
            code_line = group.code_line
            callout_nums = group.callout_numbers

            # COMMENTED OUT: User-replaceable value detection causes false positives
            # with Java generics (e.g., <MyEntity, Integer>) and other valid syntax
            # that uses angle brackets. Always use the full code line as the term.
            #
            # # Check if this is a user-replaceable value (contains angle brackets but not heredoc)
            # # User values are single words/phrases in angle brackets like <my-value>
            # user_values = DefListConverter.USER_VALUE_PATTERN.findall(code_line)
            #
            # if user_values and len(user_values) == 1 and len(code_line) < 100:
            #     # This looks like a user-replaceable value placeholder
            #     # Format the value (ensure it has angle brackets)
            #     user_value = user_values[0]
            #     if not user_value.startswith('<'):
            #         user_value = f'<{user_value}>'
            #     if not user_value.endswith('>'):
            #         user_value = f'{user_value}>'
            #     term = f'`{user_value}`'
            # else:
            #     # This is a code line - strip whitespace before wrapping in backticks
            #     term = f'`{code_line.strip()}`'

            # Always use the full code line - strip whitespace before wrapping in backticks
            term = f'`{code_line.strip()}`'

            # Add blank line before each term
            lines.append('')
            lines.append(f'{term}::')

            # Add explanations for all callouts in this group
            for idx, callout_num in enumerate(callout_nums):
                explanation = explanations[callout_num]

                # If this is not the first explanation in the group, add continuation marker
                if idx > 0:
                    lines.append('+')

                # Add explanation lines, prepending "Optional. " to first line if needed
                # Handle blank lines and conditionals by inserting continuation markers
                need_continuation = False
                had_content = False  # Track if we've output any non-conditional content

                for line_idx, line in enumerate(explanation.lines):
                    stripped = line.strip()

                    # Check if this is a blank line
                    if stripped == '':
                        # Next non-blank line will need a continuation marker
                        need_continuation = True
                        continue  # Skip blank lines

                    # Check if this is a conditional directive
                    is_conditional = stripped.startswith(('ifdef::', 'ifndef::', 'endif::'))

                    # Add continuation marker if:
                    # 1. Previous line was blank (need_continuation=True), OR
                    # 2. This is a conditional and we've had content before (need separator)
                    if need_continuation or (is_conditional and had_content and line_idx > 0):
                        lines.append('+')
                        need_continuation = False

                    # Add the line with optional prefix
                    if line_idx == 0:
                        # First line of definition
                        if explanation.is_optional:
                            # Optional marker takes precedence, then prefix
                            if definition_prefix:
                                lines.append(f'Optional. {definition_prefix}{line}')
                            else:
                                lines.append(f'Optional. {line}')
                        elif definition_prefix:
                            # Add prefix to first line
                            lines.append(f'{definition_prefix}{line}')
                        else:
                            lines.append(line)
                    else:
                        lines.append(line)

                    # Track that we've output content (not just conditionals)
                    if not is_conditional:
                        had_content = True

        return lines
