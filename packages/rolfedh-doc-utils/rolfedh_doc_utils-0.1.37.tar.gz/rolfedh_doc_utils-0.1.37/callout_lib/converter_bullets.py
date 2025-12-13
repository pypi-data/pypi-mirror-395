"""
Bulleted List Converter Module

Converts callouts to bulleted list format following Red Hat style guide.
"""

import re
from typing import List, Dict
from .detector import CalloutGroup, Callout


class BulletListConverter:
    """Converts callouts to bulleted list format."""

    # Pattern to detect user-replaceable values in angle brackets
    USER_VALUE_PATTERN = re.compile(r'(?<!<)<([a-zA-Z][^>]*)>')

    @staticmethod
    def convert(callout_groups: List[CalloutGroup], explanations: Dict[int, Callout], table_title: str = "") -> List[str]:
        """
        Create bulleted list from callout groups and explanations.

        Follows Red Hat style guide format:
        - Each bullet starts with `*` followed by backticked code element
        - Colon separates element from explanation
        - Blank line between each bullet point

        For callouts with user-replaceable values in angle brackets, uses those.
        For callouts without values, uses the actual code line as the term.

        When multiple callouts share the same code line (same group), their
        explanations are merged with line breaks.

        Args:
            callout_groups: List of CalloutGroup objects from code block
            table_title: Optional table title (e.g., ".Descriptions of delete event")
                        Will be converted to lead-in sentence
            explanations: Dict mapping callout numbers to Callout objects

        Returns:
            List of strings representing the bulleted list
        """
        # Convert table title to lead-in sentence if present
        if table_title:
            # Remove leading dot and trailing period if present
            title_text = table_title.lstrip('.').rstrip('.')
            lines = [f'\n{title_text}:']  # Use colon for bulleted list lead-in
        else:
            lines = ['']  # Start with blank line before list

        # Process each group (which may contain one or more callouts)
        for group in callout_groups:
            code_line = group.code_line
            callout_nums = group.callout_numbers

            # Check if this is a user-replaceable value (contains angle brackets but not heredoc)
            # User values are single words/phrases in angle brackets like <my-value>
            user_values = BulletListConverter.USER_VALUE_PATTERN.findall(code_line)

            if user_values and len(user_values) == 1 and len(code_line) < 100:
                # This looks like a user-replaceable value placeholder
                # Format the value (ensure it has angle brackets)
                user_value = user_values[0]
                if not user_value.startswith('<'):
                    user_value = f'<{user_value}>'
                if not user_value.endswith('>'):
                    user_value = f'{user_value}>'
                term = f'`{user_value}`'
            else:
                # This is a code line - strip whitespace before wrapping in backticks
                term = f'`{code_line.strip()}`'

            # Collect all explanations for this group
            all_explanation_lines = []
            for idx, callout_num in enumerate(callout_nums):
                explanation = explanations[callout_num]

                # Add explanation lines, prepending "Optional. " to first line if needed
                for line_idx, line in enumerate(explanation.lines):
                    if line_idx == 0 and explanation.is_optional:
                        all_explanation_lines.append(f'Optional. {line}')
                    else:
                        all_explanation_lines.append(line)

                # If there are more callouts in this group, add a line break
                if idx < len(callout_nums) - 1:
                    all_explanation_lines.append('')

            # Format as bullet point: * `term`: explanation
            # First line uses the bullet marker
            lines.append(f'*   {term}: {all_explanation_lines[0]}')

            # Continuation lines (if any) are indented to align with first line
            for continuation_line in all_explanation_lines[1:]:
                if continuation_line:  # Skip empty lines for now
                    lines.append(f'    {continuation_line}')
                else:
                    lines.append('')

            # Add blank line after each bullet point
            lines.append('')

        return lines
