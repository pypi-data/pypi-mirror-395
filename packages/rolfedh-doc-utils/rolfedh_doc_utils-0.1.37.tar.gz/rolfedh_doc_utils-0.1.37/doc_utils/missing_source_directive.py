# doc_utils/missing_source_directive.py

"""
Detects code blocks (----) that are missing [source] directive on the preceding line.

This module provides functionality to scan AsciiDoc files for code blocks that lack
proper source directives, which can cause issues with AsciiDoc-to-DocBook XML conversion.
"""

import os
import re

def is_code_block_start(line):
    """Check if line is a code block delimiter (4 or more dashes)"""
    return re.match(r'^-{4,}$', line.strip())

def has_source_directive(line):
    """Check if line contains [source] directive"""
    # Match [source], [source,lang], [source, lang], etc.
    return re.match(r'^\[source[\s,]', line.strip())

def is_empty_or_whitespace(line):
    """Check if line is empty or contains only whitespace"""
    return len(line.strip()) == 0

def scan_file(filepath):
    """
    Scan a single AsciiDoc file for missing [source] directives.

    Args:
        filepath: Path to the AsciiDoc file to scan

    Returns:
        List of issue dictionaries containing line_num, prev_line_num, and prev_line
    """
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_code_block = False

        for i, line in enumerate(lines, start=1):
            # Check if current line is a code block delimiter
            if is_code_block_start(line):
                if not in_code_block:
                    # This is the START of a code block
                    prev_line_num = i - 1
                    prev_line = lines[prev_line_num - 1].rstrip() if prev_line_num > 0 else ""

                    # Check if [source] exists in previous lines (within last 3 lines)
                    # This handles cases where there's a title between [source] and ----
                    has_source_in_context = False
                    for lookback in range(1, min(4, i)):
                        check_line = lines[i - lookback - 1].strip()
                        if has_source_directive(check_line):
                            has_source_in_context = True
                            break
                        # Stop looking if we hit an empty line or structural element
                        if not check_line or check_line.startswith(('=', '----')):
                            break

                    # Only flag if:
                    # 1. No [source] directive in recent context
                    # 2. Previous line is not empty (which might be valid formatting)
                    if (not has_source_in_context and
                        not is_empty_or_whitespace(prev_line)):

                        # Additional heuristic: check if previous line looks like it should have [source]
                        # Skip if previous line is a title, comment, or other structural element
                        prev_stripped = prev_line.strip()

                        # Skip common valid patterns
                        if prev_stripped.startswith(('=', '//', 'NOTE:', 'TIP:', 'WARNING:', 'IMPORTANT:', 'CAUTION:')):
                            in_code_block = True
                            continue

                        # Skip if previous line is already an attribute block (but not [source])
                        if prev_stripped.startswith('[') and prev_stripped.endswith(']'):
                            # It's some other attribute like [id], [role], etc., might be intentional
                            in_code_block = True
                            continue

                        # Skip if previous line is just a plus sign (continuation)
                        if prev_stripped == '+':
                            in_code_block = True
                            continue

                        # Skip if previous line is a block title (starts with .)
                        if prev_stripped.startswith('.') and len(prev_stripped) > 1:
                            # This might be a title for a source block that's defined earlier
                            # Check if there's a [source] before the title
                            if i >= 3:
                                two_lines_back = lines[i - 3].strip()
                                if has_source_directive(two_lines_back):
                                    in_code_block = True
                                    continue

                        issues.append({
                            'line_num': i,
                            'prev_line_num': prev_line_num,
                            'prev_line': prev_line[:80]  # Truncate for display
                        })

                    in_code_block = True
                else:
                    # This is the END of a code block
                    in_code_block = False

    except Exception as e:
        raise IOError(f"Error reading {filepath}: {e}")

    return issues

def fix_file(filepath, issues):
    """
    Insert [source] directives for missing code blocks.

    Args:
        filepath: Path to the AsciiDoc file to fix
        issues: List of issue dictionaries from scan_file()

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Sort issues by line number in reverse order so we can insert from bottom to top
        # This prevents line number shifts from affecting subsequent insertions
        sorted_issues = sorted(issues, key=lambda x: x['line_num'], reverse=True)

        for issue in sorted_issues:
            line_num = issue['line_num']
            # Insert [source] directive before the ---- line (at line_num - 1, which is index line_num - 1)
            insert_index = line_num - 1
            lines.insert(insert_index, '[source]\n')

        # Write the modified content back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return True

    except Exception as e:
        raise IOError(f"Error fixing {filepath}: {e}")

def find_missing_source_directives(scan_dir='.', auto_fix=False):
    """
    Scan directory for AsciiDoc files with missing [source] directives.

    Args:
        scan_dir: Directory to scan (default: current directory)
        auto_fix: If True, automatically insert [source] directives

    Returns:
        Dictionary with statistics:
        - total_issues: Total number of issues found
        - files_with_issues: Number of files with issues
        - files_fixed: Number of files successfully fixed (if auto_fix=True)
        - file_details: List of dictionaries with file paths and their issues
    """
    if not os.path.isdir(scan_dir):
        raise ValueError(f"Directory '{scan_dir}' does not exist")

    total_issues = 0
    files_with_issues = 0
    files_fixed = 0
    file_details = []

    # Find all .adoc files (excluding symbolic links)
    adoc_files = []
    for root, dirs, files in os.walk(scan_dir):
        for filename in files:
            if filename.endswith('.adoc'):
                filepath = os.path.join(root, filename)
                # Skip symbolic links
                if not os.path.islink(filepath):
                    adoc_files.append(filepath)

    for filepath in sorted(adoc_files):
        issues = scan_file(filepath)

        if issues:
            files_with_issues += 1
            total_issues += len(issues)

            file_info = {
                'filepath': filepath,
                'issues': issues,
                'fixed': False
            }

            if auto_fix:
                try:
                    if fix_file(filepath, issues):
                        files_fixed += 1
                        file_info['fixed'] = True
                except Exception as e:
                    file_info['error'] = str(e)

            file_details.append(file_info)

    return {
        'total_issues': total_issues,
        'files_with_issues': files_with_issues,
        'files_fixed': files_fixed,
        'file_details': file_details
    }
