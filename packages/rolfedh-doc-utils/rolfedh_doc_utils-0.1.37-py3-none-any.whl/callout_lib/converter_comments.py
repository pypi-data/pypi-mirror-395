"""
Inline Comments Converter Module

Converts callouts to inline comments within code blocks.
"""

import re
from typing import List, Dict, Optional, Tuple
from .detector import CalloutGroup, Callout


class LongCommentWarning:
    """Represents a warning about a comment that exceeds the length threshold."""
    def __init__(self, callout_num: int, length: int, text: str, line_num: int = None):
        self.callout_num = callout_num
        self.length = length
        self.text = text
        self.line_num = line_num


class CommentConverter:
    """Converts callouts to inline comments in code."""

    # Map of programming language identifiers to their comment syntax
    COMMENT_SYNTAX = {
        # Single-line comment languages
        'java': '//',
        'javascript': '//',
        'js': '//',
        'typescript': '//',
        'ts': '//',
        'c': '//',
        'cpp': '//',
        'c++': '//',
        'csharp': '//',
        'cs': '//',
        'go': '//',
        'rust': '//',
        'swift': '//',
        'kotlin': '//',
        'scala': '//',
        'groovy': '//',

        # Hash comment languages
        'python': '#',
        'py': '#',
        'ruby': '#',
        'rb': '#',
        'perl': '#',
        'bash': '#',
        'sh': '#',
        'shell': '#',
        'yaml': '#',
        'yml': '#',
        'properties': '#',
        'r': '#',
        'powershell': '#',
        'ps1': '#',

        # SQL variants
        'sql': '--',
        'plsql': '--',
        'tsql': '--',

        # Lua
        'lua': '--',

        # Lisp-like
        'lisp': ';;',
        'scheme': ';;',
        'clojure': ';;',

        # Markup languages
        'html': '<!--',
        'xml': '<!--',
        'svg': '<!--',

        # Other
        'matlab': '%',
        'tex': '%',
        'latex': '%',
    }

    # Languages that need closing comment syntax
    COMMENT_CLOSING = {
        'html': '-->',
        'xml': '-->',
        'svg': '-->',
    }

    @staticmethod
    def get_comment_syntax(language: Optional[str]) -> tuple[str, str]:
        """
        Get comment syntax for a given language.
        Returns tuple of (opening, closing) comment markers.
        For single-line comments, closing is empty string.

        Args:
            language: Language identifier (e.g., 'java', 'python')

        Returns:
            Tuple of (opening_marker, closing_marker)
        """
        if not language:
            # Default to generic comment marker
            return '#', ''

        lang_lower = language.lower()
        opening = CommentConverter.COMMENT_SYNTAX.get(lang_lower, '#')
        closing = CommentConverter.COMMENT_CLOSING.get(lang_lower, '')

        return opening, closing

    @staticmethod
    def format_comment(text: str, opening: str, closing: str = '') -> str:
        """
        Format text as a comment using the given markers.

        Args:
            text: Comment text
            opening: Opening comment marker (e.g., '//', '#', '<!--')
            closing: Closing comment marker (e.g., '-->')

        Returns:
            Formatted comment string
        """
        if closing:
            return f'{opening} {text} {closing}'
        else:
            return f'{opening} {text}'

    @staticmethod
    def get_comment_length(explanation: Callout, opening: str, closing: str = '') -> int:
        """
        Calculate the total length of a comment including markers and text.

        Args:
            explanation: Callout explanation
            opening: Opening comment marker
            closing: Closing comment marker (if any)

        Returns:
            Total character length of the formatted comment
        """
        # Combine all explanation lines into single comment text
        comment_parts = []
        for exp_line in explanation.lines:
            comment_parts.append(exp_line.strip())
        comment_text = ' '.join(comment_parts)

        # Add "Optional:" prefix if needed
        if explanation.is_optional:
            comment_text = f'Optional: {comment_text}'

        # Calculate total length with markers
        if closing:
            total = len(f'{opening} {comment_text} {closing}')
        else:
            total = len(f'{opening} {comment_text}')

        return total

    @staticmethod
    def shorten_comment(explanation: Callout) -> str:
        """
        Shorten a comment to its first sentence or clause.

        Args:
            explanation: Callout explanation

        Returns:
            Shortened comment text
        """
        # Get first line
        first_line = explanation.lines[0] if explanation.lines else ''

        # Find first sentence-ending punctuation
        for delimiter in ['. ', '! ', '? ']:
            if delimiter in first_line:
                short = first_line.split(delimiter)[0] + delimiter.strip()
                return short

        # No sentence delimiter found, return first line
        return first_line

    @staticmethod
    def check_comment_lengths(explanations: Dict[int, Callout], language: Optional[str] = None,
                             max_length: int = 100) -> List[LongCommentWarning]:
        """
        Check if any comments exceed the maximum length threshold.

        Args:
            explanations: Dict of callout explanations
            language: Programming language for comment syntax
            max_length: Maximum allowed comment length (default: 100)

        Returns:
            List of LongCommentWarning objects for comments exceeding threshold
        """
        opening, closing = CommentConverter.get_comment_syntax(language)
        warnings = []

        for num, explanation in explanations.items():
            length = CommentConverter.get_comment_length(explanation, opening, closing)
            if length > max_length:
                # Combine all lines for warning text
                full_text = ' '.join(exp_line.strip() for exp_line in explanation.lines)
                warnings.append(LongCommentWarning(num, length, full_text))

        return warnings

    @staticmethod
    def convert(code_content: List[str], callout_groups: List[CalloutGroup],
                explanations: Dict[int, Callout], language: Optional[str] = None,
                max_length: Optional[int] = None, shorten_long: bool = False) -> Tuple[List[str], List[LongCommentWarning]]:
        """
        Convert callouts to inline comments within code.

        This replaces callout markers (<1>, <2>, etc.) with actual comments containing
        the explanation text. The comment syntax is determined by the code block's language.

        Args:
            code_content: Original code block content with callout markers
            callout_groups: List of CalloutGroup objects (not used for inline conversion)
            explanations: Dict mapping callout numbers to Callout objects
            language: Programming language identifier for comment syntax
            max_length: Maximum comment length before triggering warning (default: None = no limit)
            shorten_long: If True, automatically shorten long comments to first sentence

        Returns:
            Tuple of (converted lines, list of LongCommentWarning objects)
        """
        opening, closing = CommentConverter.get_comment_syntax(language)
        warnings = []

        # Check for long comments if max_length specified
        if max_length:
            warnings = CommentConverter.check_comment_lengths(explanations, language, max_length)

        # Pattern for callout number in code block
        CALLOUT_IN_CODE = re.compile(r'<(\d+)>')

        result_lines = []

        for line in code_content:
            # Find all callout markers on this line
            matches = list(CALLOUT_IN_CODE.finditer(line))

            if not matches:
                # No callouts on this line - keep as-is
                result_lines.append(line)
                continue

            # Process line with callouts
            # Start from the end to maintain positions during replacement
            modified_line = line

            for match in reversed(matches):
                callout_num = int(match.group(1))

                if callout_num not in explanations:
                    # Callout number not found in explanations - skip
                    continue

                explanation = explanations[callout_num]

                # Check if we should shorten this comment
                if shorten_long and any(w.callout_num == callout_num for w in warnings):
                    # Use shortened version
                    comment_text = CommentConverter.shorten_comment(explanation)
                    if explanation.is_optional:
                        comment_text = f'Optional: {comment_text}'
                else:
                    # Build comment text from explanation lines
                    # For inline comments, combine multi-line explanations with spaces
                    comment_parts = []
                    for exp_line in explanation.lines:
                        comment_parts.append(exp_line.strip())

                    comment_text = ' '.join(comment_parts)

                    # Add "Optional:" prefix if needed
                    if explanation.is_optional:
                        comment_text = f'Optional: {comment_text}'

                # Format as comment
                comment = CommentConverter.format_comment(comment_text, opening, closing)

                # Replace the callout marker with the comment
                start, end = match.span()
                modified_line = modified_line[:start] + comment + modified_line[end:]

            result_lines.append(modified_line)

        return result_lines, warnings
