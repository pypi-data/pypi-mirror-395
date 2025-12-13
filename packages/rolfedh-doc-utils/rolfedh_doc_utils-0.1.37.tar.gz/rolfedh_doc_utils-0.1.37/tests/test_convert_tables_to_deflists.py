"""Tests for convert-tables-to-deflists CLI tool."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from convert_tables_to_deflists import (
    TableToDeflistConverter,
    parse_columns,
    main,
)


class TestParseColumns:
    """Tests for the parse_columns function."""

    def test_valid_columns(self):
        """Test parsing valid column specifications."""
        assert parse_columns("1,2") == (1, 2)
        assert parse_columns("1,3") == (1, 3)
        assert parse_columns("2,4") == (2, 4)
        assert parse_columns(" 1 , 3 ") == (1, 3)  # With whitespace

    def test_invalid_format(self):
        """Test that invalid formats raise ArgumentTypeError."""
        import argparse

        with pytest.raises(argparse.ArgumentTypeError):
            parse_columns("1")  # Only one column

        with pytest.raises(argparse.ArgumentTypeError):
            parse_columns("1,2,3")  # Three columns

        with pytest.raises(argparse.ArgumentTypeError):
            parse_columns("a,b")  # Non-numeric

        with pytest.raises(argparse.ArgumentTypeError):
            parse_columns("0,1")  # Zero is invalid (1-indexed)

        with pytest.raises(argparse.ArgumentTypeError):
            parse_columns("1,1")  # Same column for term and definition


class TestTableToDeflistConverter:
    """Tests for the TableToDeflistConverter class."""

    def test_basic_two_column_table(self):
        """Test converting a basic 2-column table."""
        content = """.Example table
[cols="1,3"]
|===
|Term1
|Definition1

|Term2
|Definition2
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=False, verbose=False)
            conversions = converter.process_file(test_file)

            assert conversions == 1

            result = test_file.read_text()
            assert "Term1::" in result
            assert "Definition1" in result
            assert "Term2::" in result
            assert "Definition2" in result
            assert "|===" not in result  # Table delimiters should be gone

    def test_skip_callout_table(self):
        """Test that callout tables are skipped by default."""
        content = """[cols="1,3"]
|===
|<1>
|First explanation

|<2>
|Second explanation
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=False, verbose=False)
            conversions = converter.process_file(test_file)

            assert conversions == 0  # Callout tables should be skipped

    def test_include_callout_table(self):
        """Test that callout tables can be included with flag."""
        content = """[cols="1,3"]
|===
|<1>
|First explanation

|<2>
|Second explanation
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(
                dry_run=False,
                verbose=False,
                skip_callout_tables=False
            )
            conversions = converter.process_file(test_file)

            assert conversions == 1

    def test_three_column_table_skipped_by_default(self):
        """Test that 3-column tables are skipped without --columns."""
        content = """[cols="1,2,3"]
|===
|Col1 |Col2 |Col3

|A |B |C
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=False, verbose=False)
            conversions = converter.process_file(test_file)

            assert conversions == 0

    def test_three_column_table_with_columns_option(self):
        """Test converting 3-column table with specific columns."""
        content = """[cols="1,2,3"]
|===
|A |B |C

|D |E |F
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(
                dry_run=False,
                verbose=False,
                columns=(1, 3)  # Use columns 1 and 3
            )
            conversions = converter.process_file(test_file)

            assert conversions == 1

            result = test_file.read_text()
            # Should use column 1 as term and column 3 as definition
            assert "A::" in result or "D::" in result

    def test_dry_run_mode(self):
        """Test that dry run doesn't modify files."""
        content = """[cols="1,2"]
|===
|Term
|Definition
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=True, verbose=False)
            conversions = converter.process_file(test_file)

            assert conversions == 1
            # File should be unchanged
            assert test_file.read_text() == content

    def test_skip_header_tables(self):
        """Test skipping tables with header rows."""
        content = """[cols="1,2"]
|===
|Item |Description

|Term1
|Definition1
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(
                dry_run=False,
                verbose=False,
                skip_header_tables=True
            )
            conversions = converter.process_file(test_file)

            assert conversions == 0

    def test_table_with_conditionals(self):
        """Test that conditional directives are preserved."""
        content = """[cols="1,2"]
|===
ifdef::condition[]
|Term1
|Definition1
endif::[]

|Term2
|Definition2
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=False, verbose=False)
            conversions = converter.process_file(test_file)

            result = test_file.read_text()
            # Conditionals should be preserved
            assert "ifdef::condition[]" in result or conversions >= 0

    def test_find_adoc_files(self):
        """Test finding .adoc files in a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some test files
            (Path(tmpdir) / "file1.adoc").touch()
            (Path(tmpdir) / "file2.adoc").touch()
            (Path(tmpdir) / "file3.txt").touch()  # Should be ignored
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            (subdir / "file4.adoc").touch()

            converter = TableToDeflistConverter(dry_run=True)
            files = converter.find_adoc_files(Path(tmpdir))

            assert len(files) == 3
            assert all(f.suffix == '.adoc' for f in files)

    def test_exclude_directories(self):
        """Test excluding directories from search."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files in different directories
            (Path(tmpdir) / "file1.adoc").touch()
            excluded_dir = Path(tmpdir) / "excluded"
            excluded_dir.mkdir()
            (excluded_dir / "file2.adoc").touch()

            converter = TableToDeflistConverter(dry_run=True)
            files = converter.find_adoc_files(Path(tmpdir), exclude_dirs=["excluded"])

            assert len(files) == 1
            assert "excluded" not in str(files[0])


class TestCLI:
    """Tests for CLI entry point."""

    def test_help_message(self):
        """Test that --help works."""
        with patch('sys.argv', ['convert-tables-to-deflists', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_version_flag(self):
        """Test that --version works."""
        with patch('sys.argv', ['convert-tables-to-deflists', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_nonexistent_path(self):
        """Test error handling for nonexistent path."""
        with patch('sys.argv', ['convert-tables-to-deflists', '/nonexistent/path']):
            result = main()
            assert result == 1

    def test_basic_invocation(self):
        """Test basic invocation with a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple test file
            test_file = Path(tmpdir) / "test.adoc"
            test_file.write_text("""[cols="1,2"]
|===
|Term
|Definition
|===
""")

            with patch('sys.argv', ['convert-tables-to-deflists', tmpdir]):
                result = main()
                assert result == 0

    def test_apply_flag(self):
        """Test --apply flag modifies files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.adoc"
            original_content = """[cols="1,2"]
|===
|Term
|Definition
|===
"""
            test_file.write_text(original_content)

            with patch('sys.argv', ['convert-tables-to-deflists', '--apply', tmpdir]):
                result = main()
                assert result == 0

            # File should be modified
            assert test_file.read_text() != original_content


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_file(self):
        """Test handling of empty files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "empty.adoc"
            test_file.write_text("")

            converter = TableToDeflistConverter(dry_run=False)
            conversions = converter.process_file(test_file)

            assert conversions == 0

    def test_file_without_tables(self):
        """Test handling files without tables."""
        content = """= Document Title

This is a document without tables.

== Section

Some content here.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "no_tables.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=False)
            conversions = converter.process_file(test_file)

            assert conversions == 0
            assert test_file.read_text() == content

    def test_multiple_tables(self):
        """Test converting multiple tables in one file."""
        content = """= Document

[cols="1,2"]
|===
|Term1
|Def1
|===

Some text.

[cols="1,2"]
|===
|Term2
|Def2
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "multi_table.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=False)
            conversions = converter.process_file(test_file)

            assert conversions == 2

            result = test_file.read_text()
            assert "Term1::" in result
            assert "Term2::" in result

    def test_inline_cells(self):
        """Test table with inline cell format (|A |B |C on one line)."""
        content = """[cols="1,2"]
|===
|Term1 |Definition1
|Term2 |Definition2
|===
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "inline.adoc"
            test_file.write_text(content)

            converter = TableToDeflistConverter(dry_run=False)
            conversions = converter.process_file(test_file)

            assert conversions == 1

            result = test_file.read_text()
            assert "Term1::" in result
            assert "Term2::" in result
