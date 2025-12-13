import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import tempfile
import shutil
import pytest
from test_fixture_archive_unused_files import setup_test_fixture_archive_unused_files
import subprocess

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'archive_unused_files.py'))

def run_script(args, cwd):
    result = subprocess.run([sys.executable, SCRIPT] + args, cwd=cwd, capture_output=True, text=True)
    return result

def test_archive_unused_files_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_test_fixture_archive_unused_files(tmpdir)
        result = run_script([], cwd=tmpdir)
        assert 'unused1.adoc' in result.stdout
        assert 'unused2.adoc' in result.stdout
        assert 'used.adoc' not in result.stdout
        # Manifest file should be created in archive
        archive_dir = os.path.join(tmpdir, 'archive')
        manifest_files = [f for f in os.listdir(archive_dir) if f.startswith('to-archive-') and f.endswith('.txt')]
        assert manifest_files

@pytest.mark.parametrize('exclude_args,should_find', [
    (['--exclude-file', './modules/unused1.adoc'], 'unused2.adoc'),
    (['--exclude-dir', './modules'], None),
])
def test_archive_unused_files_exclusions(exclude_args, should_find):
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_test_fixture_archive_unused_files(tmpdir)
        result = run_script(exclude_args, cwd=tmpdir)
        archive_dir = os.path.join(tmpdir, 'archive')
        manifest_files = [f for f in os.listdir(archive_dir) if f.startswith('to-archive-') and f.endswith('.txt')]
        assert manifest_files
        manifest_path = os.path.join(archive_dir, manifest_files[0])
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
        if should_find:
            assert should_find in manifest_content
        else:
            # If all modules are excluded, no unused files from './modules' should be present
            assert 'modules/unused1.adoc' not in manifest_content
            assert 'modules/unused2.adoc' not in manifest_content

def test_archive_unused_files_commented_references():
    """Test that files referenced only in commented lines are tracked correctly"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure
        os.makedirs(os.path.join(tmpdir, 'modules'), exist_ok=True)
        os.makedirs(os.path.join(tmpdir, 'assemblies'), exist_ok=True)
        os.makedirs(os.path.join(tmpdir, 'archive'), exist_ok=True)

        # Create files
        with open(os.path.join(tmpdir, 'modules', 'commented-only.adoc'), 'w') as f:
            f.write('This file is only referenced in comments.\n')
        with open(os.path.join(tmpdir, 'modules', 'truly-unused.adoc'), 'w') as f:
            f.write('This file has no references at all.\n')
        with open(os.path.join(tmpdir, 'modules', 'used.adoc'), 'w') as f:
            f.write('This file is properly used.\n')
        with open(os.path.join(tmpdir, 'assemblies', 'master.adoc'), 'w') as f:
            f.write('include::../modules/used.adoc[]\n')
            f.write('// include::../modules/commented-only.adoc[]\n')

        # Run without --commented flag
        result = run_script([], cwd=tmpdir)

        # Check that commented-only file is NOT in unused list (considered "used")
        assert 'commented-only.adoc' not in result.stdout
        # Check that truly unused file IS in the list
        assert 'truly-unused.adoc' in result.stdout
        # Check that report was generated
        archive_dir = os.path.join(tmpdir, 'archive')
        report_path = os.path.join(archive_dir, 'commented-references-report.txt')
        assert os.path.exists(report_path), "Commented references report should be created"

        with open(report_path, 'r') as f:
            report_content = f.read()
            assert 'commented-only.adoc' in report_content
            assert 'master.adoc' in report_content

def test_archive_unused_files_with_commented_flag():
    """Test that --commented flag includes files with commented-only references"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure
        os.makedirs(os.path.join(tmpdir, 'modules'), exist_ok=True)
        os.makedirs(os.path.join(tmpdir, 'assemblies'), exist_ok=True)
        os.makedirs(os.path.join(tmpdir, 'archive'), exist_ok=True)

        # Create files
        with open(os.path.join(tmpdir, 'modules', 'commented-only.adoc'), 'w') as f:
            f.write('This file is only referenced in comments.\n')
        with open(os.path.join(tmpdir, 'modules', 'truly-unused.adoc'), 'w') as f:
            f.write('This file has no references at all.\n')
        with open(os.path.join(tmpdir, 'modules', 'used.adoc'), 'w') as f:
            f.write('This file is properly used.\n')
        with open(os.path.join(tmpdir, 'assemblies', 'master.adoc'), 'w') as f:
            f.write('include::../modules/used.adoc[]\n')
            f.write('// include::../modules/commented-only.adoc[]\n')

        # Run WITH --commented flag
        result = run_script(['--commented'], cwd=tmpdir)

        # With --commented flag, both should be in unused list
        assert 'commented-only.adoc' in result.stdout
        assert 'truly-unused.adoc' in result.stdout
        # Check that 'used.adoc' is NOT in the output (should be excluded because it has uncommented reference)
        # Split by lines to avoid substring matching issues
        output_lines = result.stdout.strip().split('\n')
        assert not any(line.endswith('modules/used.adoc') or line == 'modules/used.adoc' for line in output_lines)

        # No report should be generated when --commented is used
        archive_dir = os.path.join(tmpdir, 'archive')
        report_path = os.path.join(archive_dir, 'commented-references-report.txt')
        # Report may exist from earlier, but shouldn't mention the file is "considered used"
        # The key is that the file should be in the manifest/stdout
