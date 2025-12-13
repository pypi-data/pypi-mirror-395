#!/usr/bin/env python3
"""
convert-callouts-interactive - Interactive AsciiDoc callout converter

Interactively converts code blocks with callouts, prompting for format choice
(definition list, bulleted list, or inline comments) for each code block.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# Import from callout_lib
from callout_lib import (
    CalloutDetector,
    DefListConverter,
    BulletListConverter,
    CommentConverter,
    CodeBlock,
)

# Import version
from doc_utils.version import __version__


# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


def print_colored(message: str, color: str = Colors.NC) -> None:
    """Print message with color"""
    print(f"{color}{message}{Colors.NC}")


def print_separator(char: str = '=', length: int = 80, color: str = Colors.CYAN) -> None:
    """Print a separator line"""
    print_colored(char * length, color)


class InteractiveCalloutConverter:
    """Interactive converter for AsciiDoc callouts."""

    def __init__(self, dry_run: bool = False, context_lines: int = 3):
        self.dry_run = dry_run
        self.context_lines = context_lines
        self.detector = CalloutDetector()
        self.changes_made = 0
        self.warnings = []
        self.apply_to_all = None  # None, 'deflist', 'bullets', 'comments', or 'skip'

    def show_code_block_preview(self, lines: List[str], block: CodeBlock, file_path: Path) -> None:
        """Display a preview of the code block with context."""
        print_separator('=', 80, Colors.CYAN)
        print_colored(f"\nFile: {file_path}", Colors.BOLD)
        print_colored(f"Code block at lines {block.start_line + 1}-{block.end_line + 1}", Colors.BLUE)
        if block.language:
            print_colored(f"Language: {block.language}", Colors.BLUE)
        print()

        # Show context before
        context_start = max(0, block.start_line - self.context_lines)
        if context_start < block.start_line:
            print_colored("  ... context before ...", Colors.CYAN)
            for i in range(context_start, block.start_line):
                print_colored(f"  {i + 1:4d} | {lines[i]}", Colors.CYAN)

        # Show the code block itself
        # Check if has [source] prefix
        has_source_prefix = self.detector.CODE_BLOCK_START.match(lines[block.start_line])
        if has_source_prefix:
            print_colored(f"  {block.start_line + 1:4d} | {lines[block.start_line]}", Colors.YELLOW)
            print_colored(f"  {block.start_line + 2:4d} | {lines[block.start_line + 1]}", Colors.YELLOW)
            content_start_line = block.start_line + 2
        else:
            print_colored(f"  {block.start_line + 1:4d} | {lines[block.start_line]}", Colors.YELLOW)
            content_start_line = block.start_line + 1

        # Show code content with callouts highlighted
        for i, line in enumerate(block.content):
            line_num = content_start_line + i
            if '<' in line and '>' in line and any(f'<{n}>' in line for n in range(1, 100)):
                # Highlight lines with callouts
                print_colored(f"  {line_num + 1:4d} | {line}", Colors.MAGENTA)
            else:
                print(f"  {line_num + 1:4d} | {line}")

        # Show closing delimiter
        print_colored(f"  {block.end_line + 1:4d} | {lines[block.end_line]}", Colors.YELLOW)

        # Show context after (callout explanations)
        context_end = min(len(lines), block.end_line + 1 + self.context_lines + 10)  # More context for explanations
        if block.end_line + 1 < context_end:
            print_colored("  ... callout explanations ...", Colors.CYAN)
            for i in range(block.end_line + 1, context_end):
                if i >= len(lines):
                    break
                # Stop showing context if we hit a new section
                if lines[i].strip() and lines[i].startswith('='):
                    break
                print_colored(f"  {i + 1:4d} | {lines[i]}", Colors.CYAN)
        print()

    def get_user_choice_for_long_comments(self, block: CodeBlock, long_warnings) -> Optional[str]:
        """
        Prompt user for choice when comments are too long.
        Returns: 'shorten', 'deflist', 'bullets', 'skip', or None for quit
        """
        print_colored("\n⚠️  WARNING: Long Comment Detected", Colors.YELLOW)
        print()
        for lw in long_warnings:
            print_colored(f"  Callout <{lw.callout_num}>: {lw.length} characters", Colors.YELLOW)
            print_colored(f"  Text: {lw.text[:100]}{'...' if len(lw.text) > 100 else ''}", Colors.CYAN)
            print()

        print("This explanation is too long for a readable inline comment.")
        print("\nWhat would you like to do?")
        print("  [s] Use Shortened version (first sentence only)")
        print("  [d] Use Definition list format instead")
        print("  [b] Use Bulleted list format instead")
        print("  [k] Skip this block")
        print("  [q] Skip current file")
        print("  [Q] Quit script entirely (Ctrl+C)")

        while True:
            try:
                choice = input("\nYour choice [s/d/b/k/q/Q]: ").strip()

                if choice in ['Q', 'QUIT', 'EXIT']:
                    # Quit script entirely
                    print_colored("\nQuitting script...", Colors.YELLOW)
                    sys.exit(0)
                elif choice.lower() in ['q', 'quit', 'exit']:
                    # Skip current file
                    return None
                elif choice.lower() in ['s', 'shorten', 'short']:
                    return 'shorten'
                elif choice.lower() in ['d', 'deflist']:
                    return 'deflist'
                elif choice.lower() in ['b', 'bullets', 'bullet']:
                    return 'bullets'
                elif choice.lower() in ['k', 'skip']:
                    return 'skip'
                else:
                    print_colored("Invalid choice. Please enter s, d, b, k, q, or Q.", Colors.RED)

            except (KeyboardInterrupt, EOFError):
                print()
                return None

    def get_user_choice(self, block_num: int, total_blocks: int) -> Optional[str]:
        """
        Prompt user for conversion choice.
        Returns: 'deflist', 'bullets', 'comments', 'skip', or None for quit
        """
        print_colored(f"\n[Code block {block_num}/{total_blocks}]", Colors.BOLD)

        # Check if user wants to apply same choice to all
        if self.apply_to_all:
            print_colored(f"Applying previous choice to all: {self.apply_to_all}", Colors.GREEN)
            return self.apply_to_all

        print("\nChoose conversion format:")
        print("  [d] Definition list (where:)")
        print("  [b] Bulleted list")
        print("  [c] Inline comments")
        print("  [s] Skip this block")
        print("  [a] Apply choice to All remaining blocks")
        print("  [q] Skip current file")
        print("  [Q] Quit script entirely (Ctrl+C)")

        while True:
            try:
                choice = input("\nYour choice [d/b/c/s/a/q/Q]: ").strip()

                if choice in ['Q', 'QUIT', 'EXIT']:
                    # Quit script entirely
                    print_colored("\nQuitting script...", Colors.YELLOW)
                    sys.exit(0)
                elif choice.lower() in ['q', 'quit', 'exit']:
                    # Skip current file
                    return None
                elif choice.lower() in ['s', 'skip']:
                    return 'skip'
                elif choice.lower() in ['d', 'deflist']:
                    return 'deflist'
                elif choice.lower() in ['b', 'bullets', 'bullet']:
                    return 'bullets'
                elif choice.lower() in ['c', 'comments', 'comment']:
                    return 'comments'
                elif choice.lower() in ['a', 'all']:
                    # Ask for the format to apply to all
                    print("\nWhat format should be applied to all remaining blocks?")
                    print("  [d] Definition list")
                    print("  [b] Bulleted list")
                    print("  [c] Inline comments")
                    print("  [s] Skip all")
                    format_choice = input("Format [d/b/c/s]: ").strip().lower()

                    if format_choice in ['d', 'deflist']:
                        self.apply_to_all = 'deflist'
                        return 'deflist'
                    elif format_choice in ['b', 'bullets', 'bullet']:
                        self.apply_to_all = 'bullets'
                        return 'bullets'
                    elif format_choice in ['c', 'comments', 'comment']:
                        self.apply_to_all = 'comments'
                        return 'comments'
                    elif format_choice in ['s', 'skip']:
                        self.apply_to_all = 'skip'
                        return 'skip'
                    else:
                        print_colored("Invalid choice. Please try again.", Colors.RED)
                else:
                    print_colored("Invalid choice. Please enter d, b, c, s, a, or q.", Colors.RED)

            except (KeyboardInterrupt, EOFError):
                print()
                return None

    def convert_file(self, input_file: Path) -> Tuple[int, bool]:
        """
        Interactively convert callouts in a file.
        Returns tuple of (number of conversions, whether file was modified).
        """
        # Read input file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = [line.rstrip('\n') for line in f]
        except Exception as e:
            print_colored(f"Error reading {input_file}: {e}", Colors.RED)
            return 0, False

        # Find all code blocks with callouts
        all_blocks = self.detector.find_code_blocks(lines)
        blocks_with_callouts = []

        for block in all_blocks:
            callout_groups = self.detector.extract_callouts_from_code(block.content)
            if callout_groups:
                blocks_with_callouts.append(block)

        if not blocks_with_callouts:
            print(f"No code blocks with callouts found in {input_file}")
            return 0, False

        print_colored(f"\n{'='*80}", Colors.GREEN)
        print_colored(f"Processing: {input_file}", Colors.BOLD)
        print_colored(f"Found {len(blocks_with_callouts)} code block(s) with callouts", Colors.GREEN)
        print_colored(f"{'='*80}\n", Colors.GREEN)

        # Process blocks and collect conversions
        conversions = []  # List of (block, format_choice) tuples
        total_blocks = len(blocks_with_callouts)

        for idx, block in enumerate(blocks_with_callouts, 1):
            # Show preview
            self.show_code_block_preview(lines, block, input_file)

            # Get user choice
            choice = self.get_user_choice(idx, total_blocks)

            if choice is None:
                print_colored("\nSkipping remaining blocks in this file.", Colors.YELLOW)
                return 0, False
            elif choice == 'skip':
                print_colored("Skipping this block.\n", Colors.YELLOW)
                continue

            # If user chose comments, check for long comments first
            if choice == 'comments':
                # Extract callouts to check comment lengths
                callout_groups = self.detector.extract_callouts_from_code(block.content)
                explanations, _ = self.detector.extract_callout_explanations(lines, block.end_line)

                # Check for long comments
                long_warnings = CommentConverter.check_comment_lengths(
                    explanations, block.language, max_length=120
                )

                if long_warnings:
                    # Prompt user for what to do with long comments
                    long_choice = self.get_user_choice_for_long_comments(block, long_warnings)

                    if long_choice is None:
                        print_colored("\nSkipping remaining blocks in this file.", Colors.YELLOW)
                        return 0, False
                    elif long_choice == 'skip':
                        print_colored("Skipping this block.\n", Colors.YELLOW)
                        continue
                    elif long_choice == 'shorten':
                        # Store that we want shortened comments
                        conversions.append((block, 'comments-shorten'))
                        print_colored("Will convert to: inline comments (shortened)\n", Colors.GREEN)
                        continue
                    else:
                        # User chose deflist or bullets instead
                        choice = long_choice
                        print_colored(f"Will convert to: {choice} instead\n", Colors.GREEN)

            conversions.append((block, choice))
            print_colored(f"Will convert to: {choice}\n", Colors.GREEN)

        if not conversions:
            print("No blocks selected for conversion.")
            return 0, False

        # Apply conversions (in reverse order to maintain line numbers)
        new_lines = lines.copy()

        for block, format_choice in reversed(conversions):
            # Extract callouts
            callout_groups = self.detector.extract_callouts_from_code(block.content)
            explanations, explanation_end = self.detector.extract_callout_explanations(new_lines, block.end_line)

            if not explanations:
                # Get callout numbers for warning message
                all_callout_nums = []
                for group in callout_groups:
                    all_callout_nums.extend(group.callout_numbers)

                warning_msg = (
                    f"WARNING: {input_file.name} line {block.start_line + 1}: "
                    f"Code block has callouts {sorted(set(all_callout_nums))} but no explanations found after it. "
                    f"This may indicate: explanations are shared with another code block, "
                    f"explanations are in an unexpected location, or documentation error (missing explanations). "
                    f"Consider reviewing this block manually."
                )
                print_colored(warning_msg, Colors.YELLOW)
                self.warnings.append(warning_msg)
                continue

            # Validate
            is_valid, code_nums, explanation_nums = self.detector.validate_callouts(callout_groups, explanations)
            if not is_valid:
                warning_msg = (
                    f"WARNING: {input_file.name} lines {block.start_line + 1}-{block.end_line + 1}: "
                    f"Callout mismatch: code has {sorted(code_nums)}, explanations have {sorted(explanation_nums)}"
                )
                print_colored(warning_msg, Colors.YELLOW)
                self.warnings.append(warning_msg)
                continue

            # Convert based on choice
            if format_choice == 'comments' or format_choice == 'comments-shorten':
                shorten = (format_choice == 'comments-shorten')
                converted_content, _ = CommentConverter.convert(
                    block.content, callout_groups, explanations, block.language,
                    max_length=None, shorten_long=shorten
                )
                output_list = []
            else:
                converted_content = self.detector.remove_callouts_from_code(block.content)
                if format_choice == 'bullets':
                    output_list = BulletListConverter.convert(callout_groups, explanations, self.detector.last_table_title)
                else:  # deflist
                    output_list = DefListConverter.convert(callout_groups, explanations, self.detector.last_table_title)

            # Replace in document
            has_source_prefix = self.detector.CODE_BLOCK_START.match(new_lines[block.start_line])
            if has_source_prefix:
                content_start = block.start_line + 2
            else:
                content_start = block.start_line + 1
            content_end = block.end_line

            if format_choice == 'comments':
                # Keep everything, just replace code content
                new_section = (
                    new_lines[:content_start] +
                    converted_content +
                    new_lines[content_end:]
                )
            else:
                # Remove old explanations, add new list
                new_section = (
                    new_lines[:content_start] +
                    converted_content +
                    [new_lines[content_end]] +
                    output_list +
                    new_lines[explanation_end + 1:]
                )

            new_lines = new_section
            self.changes_made += 1

        # Write output
        total_conversions = len(conversions)
        if total_conversions > 0 and not self.dry_run:
            try:
                with open(input_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines) + '\n')
                print_colored(f"\n✓ Saved changes to {input_file}", Colors.GREEN)
            except Exception as e:
                print_colored(f"Error writing {input_file}: {e}", Colors.RED)
                return 0, False
        elif self.dry_run:
            print_colored(f"\n[DRY RUN] Would save {total_conversions} conversion(s) to {input_file}", Colors.YELLOW)

        return total_conversions, total_conversions > 0


def find_adoc_files(path: Path, exclude_dirs: List[str] = None) -> List[Path]:
    """Find all .adoc files in the given path."""
    adoc_files = []
    exclude_dirs = exclude_dirs or []

    # Always exclude .vale directory
    if '.vale' not in exclude_dirs:
        exclude_dirs.append('.vale')

    if path.is_file():
        if path.suffix == '.adoc':
            adoc_files.append(path)
    elif path.is_dir():
        for adoc_file in path.rglob('*.adoc'):
            if any(excl in str(adoc_file) for excl in exclude_dirs):
                continue
            adoc_files.append(adoc_file)

    return sorted(adoc_files)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Interactively convert AsciiDoc callouts to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Interactive AsciiDoc callout converter.

This tool scans .adoc files for code blocks with callouts and prompts you
to choose the conversion format for each block individually:
  - Definition list (where:)
  - Bulleted list
  - Inline comments

For each code block with callouts, you'll see:
  - File name and location
  - Code block preview with context
  - Callout explanations

Then choose how to convert that specific block, or apply a choice to all
remaining blocks.

Examples:
  %(prog)s myfile.adoc              # Process single file interactively
  %(prog)s modules/                 # Process all .adoc files in directory
  %(prog)s --dry-run modules/       # Preview without making changes
  %(prog)s --context 5 myfile.adoc  # Show 5 lines of context
        """
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='File or directory to process (default: current directory)'
    )
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '-c', '--context',
        type=int,
        default=3,
        help='Number of context lines to show before/after code blocks (default: 3)'
    )
    parser.add_argument(
        '--exclude-dir',
        action='append',
        dest='exclude_dirs',
        default=[],
        help='Directory to exclude (can be used multiple times)'
    )

    args = parser.parse_args()

    # Convert path to Path object
    target_path = Path(args.path)

    if not target_path.exists():
        print_colored(f"Error: Path does not exist: {target_path}", Colors.RED)
        sys.exit(1)

    if args.dry_run:
        print_colored("DRY RUN MODE - No files will be modified\n", Colors.YELLOW)

    # Find all AsciiDoc files
    adoc_files = find_adoc_files(target_path, args.exclude_dirs)

    if not adoc_files:
        if target_path.is_file():
            print_colored(f"Error: {target_path} is not an AsciiDoc file (.adoc)", Colors.RED)
        else:
            print(f"No AsciiDoc files found in {target_path}")
        sys.exit(1)

    if len(adoc_files) > 1:
        print(f"Found {len(adoc_files)} AsciiDoc file(s) to process\n")

    # Create converter
    converter = InteractiveCalloutConverter(dry_run=args.dry_run, context_lines=args.context)

    # Process each file
    files_modified = 0
    total_conversions = 0

    for file_path in adoc_files:
        try:
            conversions, modified = converter.convert_file(file_path)

            if modified:
                files_modified += 1
                total_conversions += conversions

        except KeyboardInterrupt:
            print_colored("\n\nScript interrupted by user (Ctrl+C)", Colors.YELLOW)
            sys.exit(0)
        except Exception as e:
            print_colored(f"\nUnexpected error processing {file_path}: {e}", Colors.RED)
            import traceback
            traceback.print_exc()

    # Summary
    print_separator('=', 80, Colors.GREEN)
    print_colored("\nSummary:", Colors.BOLD)
    print(f"  Files processed: {len(adoc_files)}")
    if args.dry_run and files_modified > 0:
        print(f"  Would modify: {files_modified} file(s)")
        print(f"  Total conversions: {total_conversions}")
    elif files_modified > 0:
        print_colored(f"  Files modified: {files_modified}", Colors.GREEN)
        print_colored(f"  Total conversions: {total_conversions}", Colors.GREEN)
    else:
        print("  No files modified")

    if converter.warnings:
        print_colored(f"\n⚠  {len(converter.warnings)} Warning(s):", Colors.YELLOW)
        for warning in converter.warnings:
            print_colored(f"  {warning}", Colors.YELLOW)
        print()
        print_colored("Suggestion: Fix the callout mismatches in the files above and rerun this command.", Colors.YELLOW)

    if args.dry_run and files_modified > 0:
        print_colored("\nDRY RUN - No files were modified", Colors.YELLOW)

    print_separator('=', 80, Colors.GREEN)


if __name__ == '__main__':
    main()
