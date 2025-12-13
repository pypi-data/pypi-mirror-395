#!/usr/bin/env python3
"""
Check Source Directives

Detects code blocks (----) that are missing [source] directive in AsciiDoc files.
This helps prevent AsciiDoc-to-DocBook XML conversion errors.

Usage:
  check-source-directives                    # Scan current directory
  check-source-directives asciidoc          # Scan asciidoc/ directory
  check-source-directives --fix             # Scan and fix issues in current directory
  check-source-directives --fix asciidoc    # Scan and fix issues in asciidoc/ directory
"""

import argparse
import sys
from doc_utils.missing_source_directive import find_missing_source_directives
from doc_utils.version_check import check_version_on_startup
from doc_utils.version import __version__

# ANSI color codes
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[0;32m'
NC = '\033[0m'  # No Color

def main():
    # Check for updates (non-blocking)
    check_version_on_startup()

    parser = argparse.ArgumentParser(
        description='Detect code blocks (----) missing [source] directive in AsciiDoc files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Scan current directory
  %(prog)s asciidoc          # Scan asciidoc/ directory
  %(prog)s --fix             # Scan and fix issues in current directory
  %(prog)s --fix asciidoc    # Scan and fix issues in asciidoc/ directory
        """
    )
    parser.add_argument('directory', nargs='?', default='.',
                        help='Directory to scan (default: current directory)')
    parser.add_argument('--fix', action='store_true',
                        help='Automatically insert [source] directives where missing')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    args = parser.parse_args()

    mode = "Fixing" if args.fix else "Scanning for"
    print(f"{mode} code blocks missing [source] directive in: {args.directory}")
    print("=" * 64)
    print()

    try:
        results = find_missing_source_directives(
            scan_dir=args.directory,
            auto_fix=args.fix
        )
    except ValueError as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Unexpected error: {e}{NC}", file=sys.stderr)
        sys.exit(1)

    # Display results
    for file_info in results['file_details']:
        filepath = file_info['filepath']
        issues = file_info['issues']

        print(f"{YELLOW}File: {filepath}{NC}")

        for issue in issues:
            print(f"  {RED}Line {issue['line_num']}:{NC} Code block without [source] directive")
            print(f"    Previous line ({issue['prev_line_num']}): {issue['prev_line']}")
            print()

        if args.fix:
            if file_info.get('fixed'):
                print(f"  {GREEN}✓ Fixed {len(issues)} issue(s){NC}")
            elif 'error' in file_info:
                print(f"  {RED}✗ Failed to fix file: {file_info['error']}{NC}")
            print()

    # Summary
    print("=" * 64)
    if results['total_issues'] == 0:
        print(f"{GREEN}✓ No issues found!{NC}")
        sys.exit(0)
    else:
        if args.fix:
            print(f"{GREEN}Fixed {results['total_issues']} code block(s) in {results['files_fixed']} file(s){NC}")
            sys.exit(0)
        else:
            print(f"{RED}Found {results['total_issues']} code block(s) missing [source] directive in {results['files_with_issues']} file(s){NC}")
            print(f"\nRun with --fix to automatically fix these issues")
            sys.exit(1)

if __name__ == '__main__':
    main()
