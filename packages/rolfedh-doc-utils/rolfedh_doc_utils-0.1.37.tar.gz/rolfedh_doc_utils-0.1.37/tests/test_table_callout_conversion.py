"""
Integration tests for converting table-format callouts to different output formats.
"""

import pytest
import os
from callout_lib.detector import CalloutDetector
from callout_lib.converter_deflist import DefListConverter
from callout_lib.converter_bullets import BulletListConverter
from callout_lib.converter_comments import CommentConverter


class TestTableCalloutConversion:
    """Test converting table-format callouts to various output formats."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = CalloutDetector()
        self.deflist_converter = DefListConverter()
        self.bullet_converter = BulletListConverter()
        self.comment_converter = CommentConverter()

    def test_convert_simple_table_to_deflist(self):
        """Test converting a simple table callout to definition list."""
        lines = [
            "[source,sql]",
            "----",
            "ALTER TABLE inventory ADD COLUMN c1 INT; <1>",
            "INSERT INTO myschema.inventory (id,c1) VALUES (100, 1); <2>",
            "----",
            "",
            "[cols=\"1,3\"]",
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

        # Extract callouts from code
        callout_groups = self.detector.extract_callouts_from_code(blocks[0].content)

        # Extract explanations (should detect table format)
        explanations, end_line = self.detector.extract_callout_explanations(lines, blocks[0].end_line)
        assert len(explanations) == 2

        # Convert to definition list
        deflist_lines = self.deflist_converter.convert(
            callout_groups, explanations
        )

        # Verify output
        assert len(deflist_lines) > 0
        deflist_text = '\n'.join(deflist_lines)
        assert "Adds the table to the source database" in deflist_text
        assert "Adds the table to the signal table" in deflist_text

    def test_convert_table_with_conditionals_to_deflist(self):
        """Test converting table with conditionals to definition list."""
        lines = [
            "[source,sql]",
            "----",
            "INSERT INTO signal (id, type) VALUES ('ad-hoc-1', 'snapshot'); <1>",
            "UPDATE signal SET status = 'complete' WHERE id = 'ad-hoc-1'; <2>",
            "----",
            "",
            "|===",
            "|<1>",
            "|Inserts a signal into the signal table.",
            "",
            "ifdef::product[]",
            "|<2>",
            "|Optional. Updates the signal status.",
            "endif::[]",
            "",
            "ifndef::product[]",
            "|<2>",
            "|Required. Updates the signal status.",
            "endif::[]",
            "|===",
        ]

        blocks = self.detector.find_code_blocks(lines)
        callout_groups = self.detector.extract_callouts_from_code(blocks[0].content)
        explanations, end_line = self.detector.extract_callout_explanations(lines, blocks[0].end_line)

        # Convert to definition list
        deflist_lines = self.deflist_converter.convert(
            callout_groups, explanations
        )

        deflist_text = '\n'.join(deflist_lines)

        # Verify conditionals are preserved
        assert "ifdef::product[]" in deflist_text or "ifndef::product[]" in deflist_text
        assert "endif::[]" in deflist_text

    def test_convert_simple_table_to_bullets(self):
        """Test converting a simple table callout to bulleted list."""
        lines = [
            "[source,java]",
            "----",
            "@Path(\"/api/data\") <1>",
            "public Response getData() { <2>",
            "----",
            "",
            "|===",
            "|<1>",
            "|Defines the REST endpoint path.",
            "",
            "|<2>",
            "|Implements the GET method handler.",
            "|===",
        ]

        blocks = self.detector.find_code_blocks(lines)
        callout_groups = self.detector.extract_callouts_from_code(blocks[0].content)
        explanations, end_line = self.detector.extract_callout_explanations(lines, blocks[0].end_line)

        # Convert to bullets
        bullet_lines = self.bullet_converter.convert(
            callout_groups, explanations
        )

        bullet_text = '\n'.join(bullet_lines)

        # Verify bullet format
        assert "* " in bullet_text
        assert "Defines the REST endpoint path" in bullet_text
        assert "Implements the GET method handler" in bullet_text

    def test_convert_table_multiline_to_comments(self):
        """Test converting table with multiline explanations to inline comments."""
        lines = [
            "[source,python]",
            "----",
            "def process_data(): <1>",
            "    return result <2>",
            "----",
            "",
            "|===",
            "|<1>",
            "|Short explanation for comment format.",
            "",
            "|<2>",
            "|Returns processed result.",
            "|===",
        ]

        blocks = self.detector.find_code_blocks(lines)
        callout_groups = self.detector.extract_callouts_from_code(blocks[0].content)
        explanations, end_line = self.detector.extract_callout_explanations(lines, blocks[0].end_line)

        # Convert to comments (need to pass code content, not block)
        comment_lines, warnings = self.comment_converter.convert(
            blocks[0].content, callout_groups, explanations
        )

        # Check if conversion succeeded
        assert len(comment_lines) > 0
        comment_text = '\n'.join(comment_lines)
        # Should have inline comments
        assert "#" in comment_text or "//" in comment_text

    def test_full_conversion_workflow(self):
        """Test the complete workflow of detecting and converting table callouts."""
        # This simulates what the CLI tools would do
        content = """
[source,sql]
----
CREATE TABLE users (id INT); <1>
INSERT INTO users VALUES (1); <2>
----

[cols="1,3"]
|===
|<1>
|Creates the users table with an id column.

|<2>
|Inserts a sample user record.
|===
        """.strip()

        lines = content.split('\n')

        # Step 1: Find code blocks
        blocks = self.detector.find_code_blocks(lines)
        assert len(blocks) == 1

        # Step 2: Extract callouts from code
        callout_groups = self.detector.extract_callouts_from_code(blocks[0].content)
        assert len(callout_groups) == 2

        # Step 3: Extract explanations (auto-detects table format)
        explanations, end_line = self.detector.extract_callout_explanations(
            lines, blocks[0].end_line
        )
        assert len(explanations) == 2
        assert 1 in explanations
        assert 2 in explanations

        # Step 4: Validate
        is_valid, code_nums, exp_nums = self.detector.validate_callouts(
            callout_groups, explanations
        )
        assert is_valid

        # Step 5: Convert to all formats
        deflist = self.deflist_converter.convert(callout_groups, explanations)
        bullets = self.bullet_converter.convert(callout_groups, explanations)
        comment_lines, comment_warnings = self.comment_converter.convert(blocks[0].content, callout_groups, explanations)

        # All conversions should succeed
        assert len(deflist) > 0
        assert len(bullets) > 0
        assert len(comment_lines) > 0

    def test_mixed_format_document(self):
        """Test document with both list-format and table-format callouts."""
        content = """
[source,sql]
----
SELECT * FROM users; <1>
----

<1> This uses traditional list format.

[source,sql]
----
DELETE FROM users; <1>
----

|===
|<1>
|This uses table format.
|===
        """.strip()

        lines = content.split('\n')
        blocks = self.detector.find_code_blocks(lines)

        # First block should use list format
        exp1, end1 = self.detector.extract_callout_explanations(lines, blocks[0].end_line)
        assert 1 in exp1
        assert "traditional list format" in exp1[1].lines[0]

        # Second block should use table format
        exp2, end2 = self.detector.extract_callout_explanations(lines, blocks[1].end_line)
        assert 1 in exp2
        assert "table format" in exp2[1].lines[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
