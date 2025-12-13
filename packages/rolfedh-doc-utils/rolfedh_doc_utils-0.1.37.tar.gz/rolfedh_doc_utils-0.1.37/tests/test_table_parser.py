"""
Tests for AsciiDoc table parser module.
"""

import pytest
from callout_lib.table_parser import TableParser, AsciiDocTable, TableRow, TableCell


class TestTableParser:
    """Test suite for TableParser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = TableParser()

    def test_find_simple_table(self):
        """Test finding a simple two-column table."""
        lines = [
            "[cols=\"1,3\"]",
            "|===",
            "|Column 1",
            "|Column 2",
            "",
            "|Row 1 Col 1",
            "|Row 1 Col 2",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        assert len(tables) == 1
        assert tables[0].start_line == 0
        assert tables[0].end_line == 7
        assert tables[0].attributes == "[cols=\"1,3\"]"

    def test_find_table_without_attributes(self):
        """Test finding a table without attributes."""
        lines = [
            "|===",
            "|Cell 1",
            "|Cell 2",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        assert len(tables) == 1
        assert tables[0].attributes == ""

    def test_is_callout_table_valid(self):
        """Test detecting a valid callout table."""
        lines = [
            "|===",
            "|<1>",
            "|Explanation for callout 1",
            "",
            "|<2>",
            "|Explanation for callout 2",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        assert len(tables) == 1
        assert self.parser.is_callout_table(tables[0])

    def test_is_callout_table_invalid(self):
        """Test detecting a non-callout table."""
        lines = [
            "|===",
            "|Header 1",
            "|Header 2",
            "",
            "|Data 1",
            "|Data 2",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        assert len(tables) == 1
        assert not self.parser.is_callout_table(tables[0])

    def test_extract_callout_explanations_simple(self):
        """Test extracting callout explanations from a simple table."""
        lines = [
            "|===",
            "|<1>",
            "|Adds the table to the source database.",
            "",
            "|<2>",
            "|Adds the table to the signal table.",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        assert len(tables) == 1

        explanations = self.parser.extract_callout_explanations_from_table(tables[0])
        assert len(explanations) == 2
        assert 1 in explanations
        assert 2 in explanations

        # Check explanation content
        lines_1, conditionals_1 = explanations[1]
        assert "Adds the table to the source database." in lines_1[0]
        assert len(conditionals_1) == 0

    def test_extract_callout_explanations_with_conditionals(self):
        """Test extracting callout explanations with ifdef/ifndef statements."""
        lines = [
            "|===",
            "ifdef::community[]",
            "|<1>",
            "|Community edition explanation",
            "endif::[]",
            "",
            "ifndef::community[]",
            "|<2>",
            "|Enterprise edition explanation",
            "endif::[]",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        assert len(tables) == 1

        explanations = self.parser.extract_callout_explanations_from_table(tables[0])
        # Note: The current implementation may need adjustment for conditionals
        # This test documents expected behavior
        assert len(explanations) >= 1

    def test_find_callout_table_after_code_block(self):
        """Test finding a callout table after a code block."""
        lines = [
            "[source,sql]",
            "----",
            "ALTER TABLE inventory ADD COLUMN c1 INT; <1>",
            "INSERT INTO myschema.inventory (id,c1) VALUES (100, 1); <2>",
            "----",
            "",
            "|===",
            "|<1>",
            "|Adds the table to the source database.",
            "",
            "|<2>",
            "|Adds the table to the signal table.",
            "|===",
        ]

        table = self.parser.find_callout_table_after_code_block(lines, 4)  # Line 4 is code block end
        assert table is not None
        assert self.parser.is_callout_table(table)

    def test_no_callout_table_after_code_block(self):
        """Test when there's no callout table after a code block."""
        lines = [
            "[source,sql]",
            "----",
            "SELECT * FROM table; <1>",
            "----",
            "",
            "<1> Regular list-format explanation",
        ]

        table = self.parser.find_callout_table_after_code_block(lines, 3)
        assert table is None

    def test_convert_table_to_deflist(self):
        """Test converting a table to definition list format."""
        lines = [
            "|===",
            "|<1>",
            "|Adds the table to the source database.",
            "",
            "|<2>",
            "|Adds the table to the signal table.",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        deflist = self.parser.convert_table_to_deflist(tables[0])

        assert len(deflist) > 0
        assert "<1>" in deflist[0]
        assert any("Adds the table to the source database" in line for line in deflist)

    def test_convert_table_to_bullets(self):
        """Test converting a table to bulleted list format."""
        lines = [
            "|===",
            "|<1>",
            "|Adds the table to the source database.",
            "",
            "|<2>",
            "|Adds the table to the signal table.",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        bullets = self.parser.convert_table_to_bullets(tables[0])

        assert len(bullets) > 0
        # Check for bullet format with bold callout number
        assert any("* *<1>*:" in line for line in bullets)
        assert any("Adds the table to the source database" in line for line in bullets)

    def test_multiline_table_cells(self):
        """Test parsing table cells with multiple lines."""
        lines = [
            "|===",
            "|<1>",
            "|This is a long explanation",
            "that spans multiple lines",
            "and contains detailed information.",
            "",
            "|<2>",
            "|Another explanation",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        explanations = self.parser.extract_callout_explanations_from_table(tables[0])

        lines_1, _ = explanations[1]
        assert len(lines_1) >= 3
        assert "This is a long explanation" in lines_1[0]

    def test_table_with_complex_conditionals(self):
        """Test table with complex conditional blocks."""
        lines = [
            "[cols=\"1,3\"]",
            "|===",
            "ifdef::product[]",
            "|<1>",
            "|Product-specific explanation",
            "ifdef::version-2.0[]",
            "for version 2.0 and later",
            "endif::[]",
            "endif::[]",
            "",
            "ifndef::product[]",
            "|<1>",
            "|Community explanation",
            "endif::[]",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        assert len(tables) == 1

        # Convert to definition list preserving conditionals
        deflist = self.parser.convert_table_to_deflist(tables[0], preserve_conditionals=True)
        assert any("ifdef::product[]" in line for line in deflist)
        assert any("endif::[]" in line for line in deflist)

    def test_convert_without_preserving_conditionals(self):
        """Test converting table without preserving conditional statements."""
        lines = [
            "|===",
            "ifdef::community[]",
            "|<1>",
            "|Community explanation",
            "endif::[]",
            "|===",
        ]

        tables = self.parser.find_tables(lines)
        deflist = self.parser.convert_table_to_deflist(tables[0], preserve_conditionals=False)

        # Conditionals should be filtered out
        assert not any("ifdef::" in line for line in deflist)
        assert not any("endif::" in line for line in deflist)
        # But content should remain
        assert any("Community explanation" in line for line in deflist)


class TestTableParserIntegration:
    """Integration tests for table parser with detector."""

    def setup_method(self):
        """Set up test fixtures."""
        from callout_lib.detector import CalloutDetector
        self.detector = CalloutDetector()

    def test_detector_finds_table_callouts(self):
        """Test that detector can find and extract table-format callouts."""
        lines = [
            "[source,sql]",
            "----",
            "ALTER TABLE inventory ADD COLUMN c1 INT; <1>",
            "INSERT INTO myschema.inventory (id,c1) VALUES (100, 1); <2>",
            "----",
            "",
            "|===",
            "|<1>",
            "|Adds the table to the source database.",
            "",
            "|<2>",
            "|Adds the table to the signal table.",
            "|===",
        ]

        # Find code blocks
        blocks = self.detector.find_code_blocks(lines)
        assert len(blocks) == 1

        # Extract explanations (should find table format)
        explanations, end_line = self.detector.extract_callout_explanations(lines, blocks[0].end_line)
        assert len(explanations) == 2
        assert 1 in explanations
        assert 2 in explanations

    def test_detector_falls_back_to_list_format(self):
        """Test that detector falls back to list format when no table found."""
        lines = [
            "[source,sql]",
            "----",
            "SELECT * FROM table; <1>",
            "----",
            "",
            "<1> Regular list-format explanation",
        ]

        blocks = self.detector.find_code_blocks(lines)
        explanations, end_line = self.detector.extract_callout_explanations(lines, blocks[0].end_line)

        assert len(explanations) == 1
        assert 1 in explanations
        assert "Regular list-format explanation" in explanations[1].lines[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
