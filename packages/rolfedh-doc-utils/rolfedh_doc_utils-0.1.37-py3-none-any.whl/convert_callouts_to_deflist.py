#!/usr/bin/env python3
"""
convert-callouts-to-deflist - Convert AsciiDoc callouts to definition list format

Converts code blocks with callout-style annotations (<1>, <2>, etc.) to cleaner
definition list format with "where:" prefix, bulleted list format, or inline comments.

This tool automatically scans all .adoc files in the current directory (recursively)
by default, or you can specify a specific file or directory.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple

# Import from callout_lib
from callout_lib import (
    CalloutDetector,
    DefListConverter,
    BulletListConverter,
    CommentConverter,
)

# Import warnings report generator
from doc_utils.warnings_report import generate_warnings_report

# Import version
from doc_utils.version import __version__


# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color


def print_colored(message: str, color: str = Colors.NC) -> None:
    """Print message with color"""
    print(f"{color}{message}{Colors.NC}")


class CalloutConverter:
    """Converts callout-style documentation to various formats."""

    def __init__(self, dry_run: bool = False, verbose: bool = False, output_format: str = 'deflist',
                 max_comment_length: int = 120, force: bool = False, definition_prefix: str = ""):
        self.dry_run = dry_run
        self.verbose = verbose
        self.output_format = output_format  # 'deflist', 'bullets', or 'comments'
        self.max_comment_length = max_comment_length  # Max length for inline comments
        self.force = force  # Force strip callouts even with warnings
        self.definition_prefix = definition_prefix  # Prefix to add before definitions (e.g., "Specifies ")
        self.changes_made = 0
        self.warnings = []  # Collect warnings for summary
        self.long_comment_warnings = []  # Warnings for comments exceeding max length

        # Initialize detector and converters
        self.detector = CalloutDetector()

    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def convert_file(self, input_file: Path) -> Tuple[int, bool]:
        """
        Convert callouts in a file to the specified output format.
        Returns tuple of (number of conversions, whether file was modified).
        """
        # Read input file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = [line.rstrip('\n') for line in f]
        except Exception as e:
            print_colored(f"Error reading {input_file}: {e}", Colors.RED)
            return 0, False

        self.log(f"Processing {input_file} ({len(lines)} lines)")

        # Find all code blocks
        blocks = self.detector.find_code_blocks(lines)
        self.log(f"Found {len(blocks)} code blocks")

        if not blocks:
            return 0, False

        # Process blocks in reverse order to maintain line numbers
        new_lines = lines.copy()
        conversions = 0

        for block in reversed(blocks):
            # Extract callouts from code (returns list of CalloutGroups)
            callout_groups = self.detector.extract_callouts_from_code(block.content)

            if not callout_groups:
                self.log(f"No callouts in block at line {block.start_line + 1}")
                continue

            # Extract all callout numbers for logging
            all_callout_nums = []
            for group in callout_groups:
                all_callout_nums.extend(group.callout_numbers)

            self.log(f"Block at line {block.start_line + 1} has callouts: {all_callout_nums}")

            # Extract explanations
            explanations, explanation_end = self.detector.extract_callout_explanations(new_lines, block.end_line)

            if not explanations:
                self.log(f"No explanations found after block at line {block.start_line + 1}")
                # Warn user about code blocks with callouts but no explanations
                warning_msg = (
                    f"WARNING: {input_file.name} line {block.start_line + 1}: "
                    f"Code block has callouts {sorted(set(all_callout_nums))} but no explanations found after it. "
                    f"This may indicate: explanations are shared with another code block, "
                    f"explanations are in an unexpected location, or documentation error (missing explanations). "
                    f"Consider reviewing this block manually."
                )
                print_colored(warning_msg, Colors.YELLOW)
                self.warnings.append(warning_msg)

                # In force mode, strip callouts anyway
                if not self.force:
                    continue
                else:
                    self.log(f"FORCE MODE: Stripping callouts from block at line {block.start_line + 1} despite missing explanations")

                    # Just strip callouts without creating explanation list
                    converted_content = self.detector.remove_callouts_from_code(block.content)

                    # Replace in document
                    has_source_prefix = self.detector.CODE_BLOCK_START.match(new_lines[block.start_line])
                    if has_source_prefix:
                        content_start = block.start_line + 2  # After [source] and ----
                    else:
                        content_start = block.start_line + 1  # After ---- only
                    content_end = block.end_line

                    # Build new section with just code (no explanations)
                    new_section = (
                        new_lines[:content_start] +
                        converted_content +
                        [new_lines[content_end]] +  # Keep closing delimiter
                        new_lines[content_end + 1:]  # Keep rest of file
                    )

                    new_lines = new_section
                    conversions += 1
                    self.changes_made += 1
                    continue

            # Validate callouts match
            is_valid, code_nums, explanation_nums = self.detector.validate_callouts(callout_groups, explanations)
            if not is_valid and explanations:  # Only validate if we have explanations
                # Format warning message with file and line numbers
                line_range = f"{block.start_line + 1}-{block.end_line + 1}"
                warning_msg = (
                    f"WARNING: {input_file.name} lines {line_range}: Callout mismatch: "
                    f"code has {sorted(code_nums)}, explanations have {sorted(explanation_nums)}"
                )
                print_colored(warning_msg, Colors.YELLOW)
                self.warnings.append(warning_msg)

                # In force mode, convert anyway
                if not self.force:
                    continue
                else:
                    self.log(f"FORCE MODE: Converting block at line {block.start_line + 1} despite callout mismatch")

            self.log(f"Converting block at line {block.start_line + 1}")

            # Convert based on format option
            use_deflist_fallback = False
            if self.output_format == 'comments':
                # For comments format, replace callouts inline in the code
                converted_content, long_warnings = CommentConverter.convert(
                    block.content, callout_groups, explanations, block.language,
                    max_length=self.max_comment_length, shorten_long=False
                )

                # If there are long comment warnings, fall back to definition list
                if long_warnings:
                    for lw in long_warnings:
                        warning_msg = (
                            f"WARNING: {input_file.name} lines {block.start_line + 1}-{block.end_line + 1}: "
                            f"Callout <{lw.callout_num}> explanation too long ({lw.length} chars) "
                            f"for inline comment (max: {self.max_comment_length}). Falling back to definition list format."
                        )
                        print_colored(warning_msg, Colors.YELLOW)
                        self.warnings.append(warning_msg)
                        self.long_comment_warnings.append((input_file.name, block.start_line + 1, lw))

                    # Fall back to definition list
                    self.log(f"Falling back to definition list for block at line {block.start_line + 1}")
                    converted_content = self.detector.remove_callouts_from_code(block.content)
                    output_list = DefListConverter.convert(callout_groups, explanations, self.detector.last_table_title, self.definition_prefix)
                    use_deflist_fallback = True
                else:
                    output_list = []  # No separate list after code block for comments
            else:
                # For deflist and bullets, remove callouts from code and create separate list
                converted_content = self.detector.remove_callouts_from_code(block.content)

                if self.output_format == 'bullets':
                    output_list = BulletListConverter.convert(callout_groups, explanations, self.detector.last_table_title)
                else:  # default to 'deflist'
                    output_list = DefListConverter.convert(callout_groups, explanations, self.detector.last_table_title, self.definition_prefix)

            # Replace in document
            # Check if block has [source] prefix
            has_source_prefix = self.detector.CODE_BLOCK_START.match(new_lines[block.start_line])
            if has_source_prefix:
                content_start = block.start_line + 2  # After [source] and ----
            else:
                content_start = block.start_line + 1  # After ---- only
            content_end = block.end_line

            # For comments format (without fallback), remove explanations but don't add new list
            # For deflist/bullets format, remove old explanations and add new list
            if self.output_format == 'comments' and not use_deflist_fallback:
                # Remove old callout explanations (list or table format)
                # Find where explanations/table actually starts to preserve content in between
                if self.detector.last_table:
                    explanation_start_line = self.detector.last_table.start_line
                else:
                    # List format: skip blank lines after code block
                    explanation_start_line = block.end_line + 1
                    while explanation_start_line < len(new_lines) and not new_lines[explanation_start_line].strip():
                        explanation_start_line += 1

                new_section = (
                    new_lines[:content_start] +
                    converted_content +
                    [new_lines[content_end]] +  # Keep closing delimiter
                    new_lines[content_end + 1:explanation_start_line] +  # Preserve content between code and explanations
                    new_lines[explanation_end + 1:]  # Skip explanations/table, keep rest
                )
            else:
                # Remove old callout explanations and add new list
                # Find where explanations/table actually starts
                if self.detector.last_table:
                    # Table format: preserve content between code block and table start
                    explanation_start_line = self.detector.last_table.start_line
                else:
                    # List format: skip blank lines after code block
                    explanation_start_line = block.end_line + 1
                    while explanation_start_line < len(new_lines) and not new_lines[explanation_start_line].strip():
                        explanation_start_line += 1

                # Build the new section
                new_section = (
                    new_lines[:content_start] +
                    converted_content +
                    [new_lines[content_end]] +  # Keep closing delimiter
                    new_lines[content_end + 1:explanation_start_line] +  # Preserve content between code and explanations
                    output_list +
                    new_lines[explanation_end + 1:]
                )

            new_lines = new_section
            conversions += 1
            self.changes_made += 1

        # Write output
        if conversions > 0 and not self.dry_run:
            try:
                with open(input_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines) + '\n')
                self.log(f"Wrote {input_file}")
            except Exception as e:
                print_colored(f"Error writing {input_file}: {e}", Colors.RED)
                return 0, False

        return conversions, conversions > 0


def find_adoc_files(path: Path, exclude_dirs: List[str] = None, exclude_files: List[str] = None) -> List[Path]:
    """
    Find all .adoc files in the given path.

    Args:
        path: Path to search (file or directory)
        exclude_dirs: List of directory patterns to exclude
        exclude_files: List of file patterns to exclude

    Returns:
        List of Path objects for .adoc files
    """
    adoc_files = []
    exclude_dirs = exclude_dirs or []
    exclude_files = exclude_files or []

    # Always exclude .vale directory by default (Vale linter fixtures)
    if '.vale' not in exclude_dirs:
        exclude_dirs.append('.vale')

    if path.is_file():
        if path.suffix == '.adoc':
            # Check if file should be excluded
            if not any(excl in str(path) for excl in exclude_files):
                adoc_files.append(path)
    elif path.is_dir():
        # Recursively find all .adoc files
        for adoc_file in path.rglob('*.adoc'):
            # Check if in excluded directory
            if any(excl in str(adoc_file) for excl in exclude_dirs):
                continue
            # Check if file should be excluded
            if any(excl in str(adoc_file) for excl in exclude_files):
                continue
            adoc_files.append(adoc_file)

    return sorted(adoc_files)


def load_exclusion_list(exclusion_file: Path) -> Tuple[List[str], List[str]]:
    """
    Load exclusion list from file.
    Returns tuple of (excluded_dirs, excluded_files).
    """
    excluded_dirs = []
    excluded_files = []

    try:
        with open(exclusion_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # If it ends with /, it's a directory
                if line.endswith('/'):
                    excluded_dirs.append(line.rstrip('/'))
                else:
                    # Could be file or directory - check if it has extension
                    if '.' in Path(line).name:
                        excluded_files.append(line)
                    else:
                        excluded_dirs.append(line)
    except Exception as e:
        print_colored(f"Warning: Could not read exclusion file {exclusion_file}: {e}", Colors.YELLOW)

    return excluded_dirs, excluded_files


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Convert AsciiDoc callouts to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Convert AsciiDoc callout-style documentation to various formats.

This script identifies code blocks with callout numbers (<1>, <2>, etc.) and their
corresponding explanation lines, then converts them to your chosen format.

Formats:
  deflist  - Definition list with "where:" prefix (default)
  bullets  - Bulleted list format
  comments - Inline comments within code (removes separate explanations)

Examples:
  %(prog)s                                    # Process all .adoc files in current directory
  %(prog)s modules/                          # Process all .adoc files in modules/
  %(prog)s assemblies/my-guide.adoc          # Process single file
  %(prog)s --dry-run modules/               # Preview changes without modifying
  %(prog)s --format bullets modules/        # Convert to bulleted list format
  %(prog)s --format comments src/           # Convert to inline comments
  %(prog)s --exclude-dir .vale modules/     # Exclude .vale directory

Example transformation (deflist format):
  FROM:
    [source,yaml]
    ----
    name: <my-secret> <1>
    key: <my-key> <2>
    ----
    <1> Secret name
    <2> Key value

  TO:
    [source,yaml]
    ----
    name: <my-secret>
    key: <my-key>
    ----

    where:

    `<my-secret>`::
    Secret name

    `<my-key>`::
    Key value
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
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['deflist', 'bullets', 'comments'],
        default='deflist',
        help='Output format: "deflist" for definition list (default), "bullets" for bulleted list, "comments" for inline comments'
    )
    parser.add_argument(
        '--max-comment-length',
        type=int,
        default=120,
        help='Maximum length for inline comments before falling back to definition list (default: 120 characters)'
    )
    parser.add_argument(
        '--exclude-dir',
        action='append',
        dest='exclude_dirs',
        default=[],
        help='Directory to exclude (can be used multiple times)'
    )
    parser.add_argument(
        '--exclude-file',
        action='append',
        dest='exclude_files',
        default=[],
        help='File to exclude (can be used multiple times)'
    )
    parser.add_argument(
        '--exclude-list',
        type=Path,
        help='Path to file containing directories/files to exclude, one per line'
    )
    parser.add_argument(
        '--warnings-report',
        dest='warnings_report',
        action='store_true',
        default=True,
        help='Generate warnings report file (default: enabled)'
    )
    parser.add_argument(
        '--no-warnings-report',
        dest='warnings_report',
        action='store_false',
        help='Disable warnings report file generation'
    )
    parser.add_argument(
        '--warnings-file',
        type=Path,
        default=Path('callout-warnings-report.adoc'),
        help='Path for warnings report file (default: callout-warnings-report.adoc)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force strip callouts from code blocks even with warnings (USE WITH CAUTION: only after reviewing and fixing callout issues)'
    )
    parser.add_argument(
        '-s', '--specifies',
        action='store_true',
        help='Add "Specifies " prefix before each definition (only applies to deflist format)'
    )
    parser.add_argument(
        '--prefix',
        type=str,
        default='',
        help='Custom prefix to add before each definition (only applies to deflist format, e.g., "Indicates ")'
    )

    args = parser.parse_args()

    # Load exclusion list if provided
    if args.exclude_list:
        if args.exclude_list.exists():
            excluded_dirs, excluded_files = load_exclusion_list(args.exclude_list)
            args.exclude_dirs.extend(excluded_dirs)
            args.exclude_files.extend(excluded_files)
        else:
            print_colored(f"Warning: Exclusion list file not found: {args.exclude_list}", Colors.YELLOW)

    # Convert path to Path object
    target_path = Path(args.path)

    # Check if path exists
    if not target_path.exists():
        print_colored(f"Error: Path does not exist: {target_path}", Colors.RED)
        sys.exit(1)

    # Display dry-run mode message
    if args.dry_run:
        print_colored("DRY RUN MODE - No files will be modified", Colors.YELLOW)

    # Find all AsciiDoc files
    adoc_files = find_adoc_files(target_path, args.exclude_dirs, args.exclude_files)

    if not adoc_files:
        if target_path.is_file():
            print_colored(f"Warning: {target_path} is not an AsciiDoc file (.adoc)", Colors.YELLOW)
        else:
            print(f"No AsciiDoc files found in {target_path}")
        print("Processed 0 AsciiDoc file(s)")
        return

    print(f"Found {len(adoc_files)} AsciiDoc file(s) to process")

    # If force mode is enabled, show warning and ask for confirmation
    if args.force and not args.dry_run:
        print_colored("\n⚠️  FORCE MODE ENABLED ⚠️", Colors.YELLOW)
        print_colored("This will strip callouts from code blocks even when warnings are present.", Colors.YELLOW)
        print_colored("You should only use this option AFTER:", Colors.YELLOW)
        print_colored("  1. Reviewing all warnings in the warnings report", Colors.YELLOW)
        print_colored("  2. Manually fixing callout issues where appropriate", Colors.YELLOW)
        print_colored("  3. Confirming that remaining warnings are acceptable", Colors.YELLOW)
        print()
        response = input("Are you sure you want to proceed with force mode? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print_colored("Operation cancelled.", Colors.YELLOW)
            sys.exit(0)
        print()

    # Determine definition prefix
    definition_prefix = ""
    if args.specifies:
        definition_prefix = "Specifies "
    elif args.prefix:
        definition_prefix = args.prefix
        # Add trailing space if user didn't include one
        if definition_prefix and not definition_prefix.endswith(' '):
            definition_prefix += ' '

    # Create converter
    converter = CalloutConverter(dry_run=args.dry_run, verbose=args.verbose, output_format=args.format,
                                 max_comment_length=args.max_comment_length, force=args.force,
                                 definition_prefix=definition_prefix)

    # Process each file
    files_processed = 0
    files_modified = 0
    total_conversions = 0

    for file_path in adoc_files:
        try:
            conversions, modified = converter.convert_file(file_path)

            if modified:
                files_modified += 1
                total_conversions += conversions
                if args.dry_run:
                    print_colored(f"Would modify: {file_path} ({conversions} code block(s))", Colors.YELLOW)
                else:
                    print_colored(f"Modified: {file_path} ({conversions} code block(s))", Colors.GREEN)
            elif args.verbose:
                print(f"  No callouts found in: {file_path}")

            files_processed += 1

        except KeyboardInterrupt:
            print_colored("\nOperation cancelled by user", Colors.YELLOW)
            sys.exit(1)
        except Exception as e:
            print_colored(f"Unexpected error processing {file_path}: {e}", Colors.RED)
            if args.verbose:
                import traceback
                traceback.print_exc()

    # Summary
    print(f"\nProcessed {files_processed} AsciiDoc file(s)")
    if args.dry_run and files_modified > 0:
        print(f"Would modify {files_modified} file(s) with {total_conversions} code block conversion(s)")
    elif files_modified > 0:
        print_colored(f"Modified {files_modified} file(s) with {total_conversions} code block conversion(s)", Colors.GREEN)
    else:
        print("No files with callouts to convert")

    # Display warning summary if any warnings were collected
    if converter.warnings:
        # Generate warnings report if enabled
        if args.warnings_report:
            try:
                generate_warnings_report(converter.warnings, args.warnings_file)
                print_colored(f"\n⚠️  {len(converter.warnings)} Warning(s) - See {args.warnings_file} for details", Colors.YELLOW)
                print()
                print_colored(f"Suggestion: Review and fix the callout issues listed in {args.warnings_file}, then rerun this command.", Colors.YELLOW)
            except Exception as e:
                print_colored(f"\n⚠️  {len(converter.warnings)} Warning(s):", Colors.YELLOW)
                print_colored(f"Error generating warnings report: {e}", Colors.RED)
                # Fall back to displaying warnings in console
                for warning in converter.warnings:
                    print_colored(f"  {warning}", Colors.YELLOW)
                print()
                print_colored("Suggestion: Fix the callout issues listed above and rerun this command.", Colors.YELLOW)
        else:
            # Console-only output (legacy behavior)
            print_colored(f"\n⚠️  {len(converter.warnings)} Warning(s):", Colors.YELLOW)
            for warning in converter.warnings:
                print_colored(f"  {warning}", Colors.YELLOW)
            print()
            print_colored("Suggestion: Fix the callout issues listed above and rerun this command.", Colors.YELLOW)
        print()

    if args.dry_run and files_modified > 0:
        print_colored("DRY RUN - No files were modified", Colors.YELLOW)

    return 0 if files_processed >= 0 else 1


if __name__ == '__main__':
    sys.exit(main())
