"""
Generate AsciiDoc warnings report for callout conversion issues.
"""

from datetime import datetime
from typing import List, Dict, Set
from pathlib import Path


class WarningInfo:
    """Information about a specific warning."""

    def __init__(self, warning_type: str, file_name: str, line_info: str,
                 code_nums: List[int] = None, explanation_nums: List[int] = None):
        self.warning_type = warning_type  # 'mismatch' or 'missing'
        self.file_name = file_name
        self.line_info = line_info  # e.g., "211" or "55-72"
        self.code_nums = code_nums or []
        self.explanation_nums = explanation_nums or []


def parse_warning_message(warning_msg: str) -> WarningInfo:
    """
    Parse a warning message to extract structured information.

    Examples:
    - "WARNING: file.adoc lines 55-72: Callout mismatch: code has [1, 2], explanations have [1, 3]"
    - "WARNING: file.adoc line 211: Code block has callouts [1, 2, 3, 4] but no explanations found..."
    """
    import re

    # Extract file name and line info
    match = re.match(r'WARNING: (.+?) lines? ([\d-]+):', warning_msg)
    if not match:
        return None

    file_name = match.group(1)
    line_info = match.group(2)

    # Determine warning type and extract callout numbers
    if 'Callout mismatch' in warning_msg:
        # Parse: "code has [1, 2], explanations have [1, 3]"
        code_match = re.search(r'code has \[([^\]]+)\]', warning_msg)
        exp_match = re.search(r'explanations have \[([^\]]+)\]', warning_msg)

        code_nums = []
        exp_nums = []

        if code_match:
            code_nums = [int(n.strip()) for n in code_match.group(1).split(',')]
        if exp_match:
            exp_nums = [int(n.strip()) for n in exp_match.group(1).split(',')]

        return WarningInfo('mismatch', file_name, line_info, code_nums, exp_nums)

    elif 'but no explanations found' in warning_msg:
        # Parse: "Code block has callouts [1, 2, 3, 4] but no explanations found"
        callouts_match = re.search(r'has callouts \[([^\]]+)\]', warning_msg)

        code_nums = []
        if callouts_match:
            code_nums = [int(n.strip()) for n in callouts_match.group(1).split(',')]

        return WarningInfo('missing', file_name, line_info, code_nums, [])

    return None


def analyze_mismatch(code_nums: List[int], exp_nums: List[int]) -> List[str]:
    """
    Analyze what's wrong with a callout mismatch.

    Returns a list of issue descriptions.
    """
    issues = []
    code_set = set(code_nums)
    exp_set = set(exp_nums)

    # Check for duplicates in explanations
    exp_counts = {}
    for num in exp_nums:
        exp_counts[num] = exp_counts.get(num, 0) + 1

    duplicates = [num for num, count in exp_counts.items() if count > 1]
    if duplicates:
        for dup in duplicates:
            count = exp_counts[dup]
            issues.append(f"Duplicate callout: {dup} (appears {count} times in explanations)")

    # Check for missing callouts (in code but not in explanations)
    missing_in_exp = code_set - exp_set
    if missing_in_exp:
        for num in sorted(missing_in_exp):
            issues.append(f"Missing callout: {num} (in code but not in explanations)")

    # Check for extra callouts (in explanations but not in code)
    extra_in_exp = exp_set - code_set
    if extra_in_exp:
        for num in sorted(extra_in_exp):
            issues.append(f"Extra callout: {num} (in explanations but not in code)")

    # Check for off-by-one errors
    if code_nums and exp_nums:
        code_start = min(code_nums)
        exp_start = min(exp_nums)
        if code_start != exp_start and not (missing_in_exp or extra_in_exp or duplicates):
            issues.append(f"Off-by-one error (code starts at {code_start}, explanations start at {exp_start})")

    return issues


def generate_warnings_report(warnings: List[str], output_path: Path = None) -> str:
    """
    Generate an AsciiDoc warnings report from warning messages.

    Args:
        warnings: List of warning message strings
        output_path: Path to write report file (if None, returns content only)

    Returns:
        The report content as a string
    """
    if not warnings:
        return ""

    # Parse all warnings
    parsed_warnings = []
    for warning in warnings:
        parsed = parse_warning_message(warning)
        if parsed:
            parsed_warnings.append(parsed)

    if not parsed_warnings:
        return ""

    # Group warnings by type
    mismatch_warnings = [w for w in parsed_warnings if w.warning_type == 'mismatch']
    missing_warnings = [w for w in parsed_warnings if w.warning_type == 'missing']

    # Generate report content
    lines = []
    lines.append("= Callout Conversion Warnings Report")
    lines.append(":toc:")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Summary
    lines.append("== Summary")
    lines.append("")
    lines.append(f"Total warnings: {len(parsed_warnings)}")
    if mismatch_warnings:
        lines.append(f"- Callout mismatches: {len(mismatch_warnings)}")
    if missing_warnings:
        lines.append(f"- Missing explanations: {len(missing_warnings)}")
    lines.append("")
    lines.append("== Recommended Actions")
    lines.append("")
    lines.append("1. Review each warning below and fix callout issues where appropriate")
    lines.append("2. For callout mismatches: Ensure code callouts match explanation numbers")
    lines.append("3. For missing explanations: Check if explanations are shared with another block or missing")
    lines.append("4. After fixing issues, rerun the conversion command")
    lines.append("")
    lines.append("== Force Mode Option")
    lines.append("")
    lines.append("CAUTION: Use this option sparingly and only after reviewing all warnings.")
    lines.append("")
    lines.append("If you've reviewed all warnings and confirmed that remaining issues are acceptable,")
    lines.append("you can use the `--force` option to strip callouts from code blocks despite warnings:")
    lines.append("")
    lines.append("[source,bash]")
    lines.append("----")
    lines.append("convert-callouts-to-deflist --force modules/")
    lines.append("----")
    lines.append("")
    lines.append("Force mode will:")
    lines.append("")
    lines.append("- Strip callouts from blocks with missing explanations (without creating explanation lists)")
    lines.append("- Convert blocks with callout mismatches using available explanations")
    lines.append("- Require confirmation before proceeding (unless in dry-run mode)")
    lines.append("")
    lines.append("IMPORTANT: Always work in a git branch and review changes with `git diff` before committing.")
    lines.append("")

    # Callout Mismatch section
    if mismatch_warnings:
        lines.append("== Callout Mismatch Warnings")
        lines.append("")
        lines.append("Callout numbers in code don't match explanation numbers.")
        lines.append("")

        for warning in mismatch_warnings:
            lines.append(f"=== {warning.file_name}")
            lines.append("")
            lines.append(f"*Lines {warning.line_info}*")
            lines.append("")
            lines.append(f"Code has:: {warning.code_nums}")
            lines.append(f"Explanations have:: {warning.explanation_nums}")
            lines.append("")

            issues = analyze_mismatch(warning.code_nums, warning.explanation_nums)
            if issues:
                lines.append("Issues detected::")
                for issue in issues:
                    lines.append(f"- {issue}")
                lines.append("")

    # Missing Explanations section
    if missing_warnings:
        lines.append("== Missing Explanations Warnings")
        lines.append("")
        lines.append("Code blocks with callouts but no explanations found after them.")
        lines.append("")

        for warning in missing_warnings:
            lines.append(f"=== {warning.file_name}")
            lines.append("")
            lines.append(f"*Line {warning.line_info}*")
            lines.append("")
            lines.append(f"Callouts in code:: {warning.code_nums}")
            lines.append("")
            lines.append("Possible causes::")
            lines.append("- Explanations shared with another code block (e.g., in conditional sections)")
            lines.append("- Explanations in unexpected location")
            lines.append("- Documentation error (missing explanations)")
            lines.append("")
            lines.append("Action:: Review this block manually")
            lines.append("")

    content = '\n'.join(lines)

    # Write to file if path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return content
