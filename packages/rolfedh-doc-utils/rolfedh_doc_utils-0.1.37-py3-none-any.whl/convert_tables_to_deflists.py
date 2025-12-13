#!/usr/bin/env python3
"""
convert-tables-to-deflists: Convert AsciiDoc tables to definition lists.

Converts 2-column AsciiDoc tables to definition list format, where:
- The first column becomes the term
- The second column becomes the definition

Tables with more than 2 columns are skipped (use --columns to specify which
columns to use as term and definition).

Usage:
    convert-tables-to-deflists [OPTIONS] [PATH]

Examples:
    # Preview changes (dry-run mode)
    convert-tables-to-deflists .

    # Apply changes to all .adoc files
    convert-tables-to-deflists --apply .

    # Process a single file
    convert-tables-to-deflists --apply path/to/file.adoc

    # Use columns 1 and 3 for 3-column tables
    convert-tables-to-deflists --columns 1,3 .

    # Skip tables with headers
    convert-tables-to-deflists --skip-header-tables .
"""

import argparse
import sys
import re
from pathlib import Path
from typing import List, Optional, Tuple

from callout_lib.table_parser import TableParser, AsciiDocTable
from doc_utils.version import __version__
from doc_utils.file_utils import parse_exclude_list_file


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


def print_colored(message: str, color: str = Colors.NC) -> None:
    """Print a message with optional color."""
    print(f"{color}{message}{Colors.NC}")


class TableToDeflistConverter:
    """Converts AsciiDoc tables to definition lists."""

    def __init__(self, dry_run: bool = True, verbose: bool = False,
                 columns: Optional[Tuple[int, int]] = None,
                 skip_header_tables: bool = False,
                 skip_callout_tables: bool = True):
        """
        Initialize the converter.

        Args:
            dry_run: If True, don't modify files (preview mode)
            verbose: If True, show detailed output
            columns: Tuple of (term_col, def_col) for multi-column tables (1-indexed)
            skip_header_tables: If True, skip tables that have header rows
            skip_callout_tables: If True, skip tables that look like callout tables
        """
        self.dry_run = dry_run
        self.verbose = verbose
        self.columns = columns  # 1-indexed column numbers
        self.skip_header_tables = skip_header_tables
        self.skip_callout_tables = skip_callout_tables
        self.parser = TableParser()
        self.files_processed = 0
        self.files_modified = 0
        self.tables_converted = 0

    def find_adoc_files(self, path: Path, exclude_dirs: List[str] = None,
                        exclude_files: List[str] = None) -> List[Path]:
        """Find all .adoc files in the given path."""
        exclude_dirs = exclude_dirs or []
        exclude_files = exclude_files or []

        if path.is_file():
            return [path] if path.suffix == '.adoc' else []

        adoc_files = []
        for adoc_file in path.rglob('*.adoc'):
            # Skip excluded directories
            if any(excl in str(adoc_file) for excl in exclude_dirs):
                continue
            # Skip excluded files
            if any(excl in str(adoc_file) for excl in exclude_files):
                continue
            # Skip symlinks
            if adoc_file.is_symlink():
                continue
            adoc_files.append(adoc_file)

        return sorted(adoc_files)

    def _should_skip_table(self, table: AsciiDocTable) -> Tuple[bool, str]:
        """
        Determine if a table should be skipped.

        Returns:
            Tuple of (should_skip, reason)
        """
        # Skip empty tables
        if not table.rows:
            return True, "empty table"

        # Skip callout tables (they're handled by convert-callouts-to-deflist)
        if self.skip_callout_tables:
            if self.parser.is_callout_table(table) or self.parser.is_3column_callout_table(table):
                return True, "callout table (use convert-callouts-to-deflist)"

        # Check column count
        if table.rows:
            first_row_cols = len(table.rows[0].cells)

            # If specific columns are specified, verify they exist
            if self.columns:
                term_col, def_col = self.columns
                if term_col > first_row_cols or def_col > first_row_cols:
                    return True, f"specified columns ({term_col}, {def_col}) exceed table columns ({first_row_cols})"
            else:
                # Default: only process 2-column tables
                if first_row_cols != 2:
                    return True, f"{first_row_cols}-column table (use --columns to specify term and definition columns)"

        # Check for header row
        if self.skip_header_tables and self.parser._has_header_row(table):
            return True, "table has header row"

        return False, ""

    def _convert_table_to_deflist(self, table: AsciiDocTable) -> List[str]:
        """
        Convert a table to definition list format.

        Args:
            table: The AsciiDocTable to convert

        Returns:
            List of lines representing the definition list
        """
        output = []

        # Determine which columns to use (0-indexed internally)
        if self.columns:
            term_idx = self.columns[0] - 1  # Convert to 0-indexed
            def_idx = self.columns[1] - 1
        else:
            term_idx = 0
            def_idx = 1

        # Check if table has a header row
        has_header = self.parser._has_header_row(table)
        data_rows = table.rows[1:] if has_header else table.rows

        for row in data_rows:
            # Verify row has enough cells
            if len(row.cells) <= max(term_idx, def_idx):
                continue

            # Add conditionals before row
            if row.conditionals_before:
                output.extend(row.conditionals_before)

            # Get term (first specified column)
            term_cell = row.cells[term_idx]
            term = ' '.join(line.strip() for line in term_cell.content if line.strip())

            # Get definition (second specified column)
            def_cell = row.cells[def_idx]
            def_lines = def_cell.content

            # Create definition list entry
            if term:
                output.append(f'{term}::')

                # Add definition lines
                first_content_line = True
                for line in def_lines:
                    stripped = line.strip()

                    # Handle conditional directives
                    if stripped.startswith(('ifdef::', 'ifndef::', 'endif::')):
                        output.append(line)
                        continue

                    # Skip empty lines within definition but track them
                    if not stripped:
                        continue

                    # First content line gets no indent, subsequent lines do
                    if first_content_line:
                        output.append(stripped)
                        first_content_line = False
                    else:
                        output.append(f'+\n{stripped}')

                # Add blank line after entry
                output.append('')

            # Add conditionals after row
            if row.conditionals_after:
                output.extend(row.conditionals_after)

        # Remove trailing blank line if present
        if output and not output[-1].strip():
            output.pop()

        return output

    def process_file(self, file_path: Path) -> int:
        """
        Process a single file, converting tables to definition lists.

        Args:
            file_path: Path to the .adoc file

        Returns:
            Number of tables converted
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.rstrip('\n') for line in f]
        except Exception as e:
            print_colored(f"Error reading {file_path}: {e}", Colors.RED)
            return 0

        original_lines = lines.copy()
        tables = self.parser.find_tables(lines)
        conversions = 0

        # Process tables in reverse order to preserve line numbers
        for table in reversed(tables):
            should_skip, reason = self._should_skip_table(table)

            if should_skip:
                if self.verbose:
                    print(f"  Skipping table at line {table.start_line + 1}: {reason}")
                continue

            # Convert the table
            deflist_lines = self._convert_table_to_deflist(table)

            if deflist_lines:
                # Replace table with definition list
                lines[table.start_line:table.end_line + 1] = deflist_lines
                conversions += 1

                if self.verbose:
                    print(f"  Converted table at line {table.start_line + 1}")

        # Write changes if not in dry-run mode
        if conversions > 0:
            if self.dry_run:
                print_colored(f"Would modify: {file_path} ({conversions} table(s))", Colors.YELLOW)
            else:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines) + '\n')
                    print_colored(f"Modified: {file_path} ({conversions} table(s))", Colors.GREEN)
                except Exception as e:
                    print_colored(f"Error writing {file_path}: {e}", Colors.RED)
                    return 0

        return conversions

    def process_path(self, path: Path, exclude_dirs: List[str] = None,
                     exclude_files: List[str] = None) -> None:
        """
        Process all .adoc files in the given path.

        Args:
            path: File or directory path to process
            exclude_dirs: List of directory patterns to exclude
            exclude_files: List of file patterns to exclude
        """
        adoc_files = self.find_adoc_files(path, exclude_dirs, exclude_files)

        if not adoc_files:
            print_colored("No .adoc files found.", Colors.YELLOW)
            return

        if self.dry_run:
            print_colored("DRY RUN MODE - No files will be modified", Colors.YELLOW)
            print()

        for file_path in adoc_files:
            self.files_processed += 1
            conversions = self.process_file(file_path)

            if conversions > 0:
                self.files_modified += 1
                self.tables_converted += conversions

        # Print summary
        print()
        print(f"Processed {self.files_processed} file(s)")
        print(f"Tables converted: {self.tables_converted}")
        print(f"Files {'would be ' if self.dry_run else ''}modified: {self.files_modified}")

        if self.dry_run and self.files_modified > 0:
            print()
            print_colored("DRY RUN - No files were modified. Use --apply to apply changes.", Colors.YELLOW)


def parse_columns(columns_str: str) -> Tuple[int, int]:
    """
    Parse a columns specification like "1,3" into a tuple.

    Args:
        columns_str: String like "1,3" specifying term and definition columns

    Returns:
        Tuple of (term_column, definition_column) as 1-indexed integers

    Raises:
        argparse.ArgumentTypeError: If the format is invalid
    """
    try:
        parts = columns_str.split(',')
        if len(parts) != 2:
            raise ValueError("Expected exactly two column numbers")
        term_col = int(parts[0].strip())
        def_col = int(parts[1].strip())
        if term_col < 1 or def_col < 1:
            raise ValueError("Column numbers must be 1 or greater")
        if term_col == def_col:
            raise ValueError("Term and definition columns must be different")
        return (term_col, def_col)
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid columns format '{columns_str}': {e}. "
            "Use format like '1,2' or '1,3' (1-indexed column numbers)"
        )


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Convert AsciiDoc tables to definition lists.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes (default dry-run mode)
  convert-tables-to-deflists .

  # Apply changes to all .adoc files
  convert-tables-to-deflists --apply .

  # Process a single file
  convert-tables-to-deflists --apply path/to/file.adoc

  # For 3-column tables, use columns 1 and 3
  convert-tables-to-deflists --columns 1,3 .

  # Skip tables that have header rows
  convert-tables-to-deflists --skip-header-tables .

Notes:
  - By default, only 2-column tables are converted
  - Callout tables are automatically skipped (use convert-callouts-to-deflist)
  - Use --columns to specify which columns to use for multi-column tables
  - The first specified column becomes the term, the second becomes the definition
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
        '--apply',
        action='store_true',
        help='Apply changes (default is dry-run mode)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    parser.add_argument(
        '--columns',
        type=parse_columns,
        metavar='TERM,DEF',
        help='Column numbers to use as term and definition (1-indexed, e.g., "1,3")'
    )

    parser.add_argument(
        '--skip-header-tables',
        action='store_true',
        help='Skip tables that have header rows'
    )

    parser.add_argument(
        '--include-callout-tables',
        action='store_true',
        help='Include callout tables (normally skipped)'
    )

    parser.add_argument(
        '--exclude-dir',
        action='append',
        default=[],
        metavar='DIR',
        help='Directory pattern to exclude (can be specified multiple times)'
    )

    parser.add_argument(
        '--exclude-file',
        action='append',
        default=[],
        metavar='FILE',
        help='File pattern to exclude (can be specified multiple times)'
    )

    parser.add_argument(
        '--exclude-list',
        type=Path,
        metavar='FILE',
        help='Path to file containing exclusion patterns (one per line)'
    )

    args = parser.parse_args()

    # Parse exclusion list if provided
    exclude_dirs = list(args.exclude_dir)
    exclude_files = list(args.exclude_file)

    if args.exclude_list:
        list_dirs, list_files = parse_exclude_list_file(args.exclude_list)
        exclude_dirs.extend(list_dirs)
        exclude_files.extend(list_files)

    # Create converter
    converter = TableToDeflistConverter(
        dry_run=not args.apply,
        verbose=args.verbose,
        columns=args.columns,
        skip_header_tables=args.skip_header_tables,
        skip_callout_tables=not args.include_callout_tables
    )

    # Process files
    path = Path(args.path)
    if not path.exists():
        print_colored(f"Error: Path does not exist: {path}", Colors.RED)
        return 1

    converter.process_path(path, exclude_dirs, exclude_files)

    return 0


if __name__ == '__main__':
    sys.exit(main())
