# doc_utils/unused_adoc.py

import os
import re
from .file_utils import collect_files, write_manifest_and_archive
from .topic_map_parser import detect_repo_type, get_all_topic_map_references

def find_scan_directories(base_path='.', exclude_dirs=None):
    """
    Automatically find all 'modules' and 'assemblies' directories in the repository.
    
    Returns a list of paths to scan.
    """
    scan_dirs = []
    exclude_dirs = exclude_dirs or []
    
    for root, dirs, files in os.walk(base_path):
        # Skip symbolic links to prevent issues
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        
        # Skip excluded directories
        for exclude_dir in exclude_dirs:
            abs_exclude = os.path.abspath(exclude_dir)
            if os.path.abspath(root).startswith(abs_exclude):
                dirs[:] = []  # Don't descend into excluded directories
                break
        
        # Skip hidden directories and common non-content directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'build', 'dist', 'target']]
        
        # Look for modules and assemblies directories
        for d in dirs:
            if d in ['modules', 'assemblies']:
                dir_path = os.path.join(root, d)
                # Check if this directory or any subdirectory contains .adoc files
                has_adoc = False
                for subroot, subdirs, subfiles in os.walk(dir_path):
                    # Skip symbolic links
                    subdirs[:] = [sd for sd in subdirs if not os.path.islink(os.path.join(subroot, sd))]
                    if any(f.endswith('.adoc') for f in subfiles):
                        has_adoc = True
                        break
                if has_adoc:
                    scan_dirs.append(dir_path)
    
    # Also check for modules/rn pattern if modules exists
    modules_dirs = [d for d in scan_dirs if os.path.basename(d) == 'modules']
    for modules_dir in modules_dirs:
        rn_dir = os.path.join(modules_dir, 'rn')
        if os.path.isdir(rn_dir):
            # Check if rn directory or subdirectories contain .adoc files
            has_adoc = False
            for subroot, subdirs, subfiles in os.walk(rn_dir):
                subdirs[:] = [sd for sd in subdirs if not os.path.islink(os.path.join(subroot, sd))]
                if any(f.endswith('.adoc') for f in subfiles):
                    has_adoc = True
                    break
            if has_adoc:
                scan_dirs.append(rn_dir)
    
    return scan_dirs

def find_unused_adoc(scan_dirs=None, archive_dir='./archive', archive=False, exclude_dirs=None, exclude_files=None, include_commented=False):
    # Print safety warning
    print("\n⚠️  SAFETY: Work in a git branch! Run without --archive first to preview.\n")

    # If no scan_dirs provided, auto-discover them
    if not scan_dirs:
        scan_dirs = find_scan_directories(exclude_dirs=exclude_dirs)
        if scan_dirs:
            print(f"Auto-discovered directories to scan:")
            for dir_path in sorted(scan_dirs):
                print(f"  - {dir_path}")
        else:
            print("No 'modules' or 'assemblies' directories found containing .adoc files.")
            print("Please run this tool from your documentation repository root.")
            return

    # Detect repository type
    repo_type = detect_repo_type()
    print(f"Detected repository type: {repo_type}")

    # Collect all .adoc files in scan directories
    asciidoc_files = collect_files(scan_dirs, {'.adoc'}, exclude_dirs, exclude_files)

    # Track which files are referenced (uncommented and commented separately)
    referenced_files = set()  # Files in uncommented includes
    commented_only_files = {}  # Files referenced ONLY in commented lines: {basename: [(file, line_num, line_text)]}

    if repo_type == 'topic_map':
        # For OpenShift-docs style repos, get references from topic maps
        topic_references = get_all_topic_map_references()
        # Convert to basenames for comparison
        referenced_files.update(os.path.basename(ref) for ref in topic_references)

    # Patterns for finding includes (both commented and uncommented)
    include_pattern = re.compile(r'include::(.+?)\[')
    commented_include_pattern = re.compile(r'^\s*//.*include::(.+?)\[')

    adoc_files = collect_files(['.'], {'.adoc'}, exclude_dirs, exclude_files)

    for file_path in adoc_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    # Check if this is a commented include
                    commented_match = commented_include_pattern.search(line)
                    if commented_match:
                        include_basename = os.path.basename(commented_match.group(1))
                        # Track location of commented reference
                        if include_basename not in commented_only_files:
                            commented_only_files[include_basename] = []
                        commented_only_files[include_basename].append((file_path, line_num, line.strip()))
                    else:
                        # Check for uncommented includes
                        uncommented_match = include_pattern.search(line)
                        if uncommented_match:
                            include_basename = os.path.basename(uncommented_match.group(1))
                            referenced_files.add(include_basename)
                            # If we found an uncommented reference, remove from commented_only tracking
                            if include_basename in commented_only_files:
                                del commented_only_files[include_basename]
        except Exception as e:
            print(f"Warning: could not read {file_path}: {e}")

    # Determine which files are unused based on the include_commented flag
    if include_commented:
        # When --commented is used: treat files with commented-only references as unused
        # Only files with uncommented references are considered "used"
        unused_files = [f for f in asciidoc_files if os.path.basename(f) not in referenced_files]
        commented_only_unused = []
    else:
        # Default behavior: files referenced only in commented lines are considered "used"
        # They should NOT be in the unused list, but we track them for reporting
        all_referenced = referenced_files.union(set(commented_only_files.keys()))
        unused_files = [f for f in asciidoc_files if os.path.basename(f) not in all_referenced]

        # Generate list of files referenced only in comments for the report
        commented_only_unused = []
        for basename, references in commented_only_files.items():
            # Find the full path for this basename in asciidoc_files
            matching_files = [f for f in asciidoc_files if os.path.basename(f) == basename]
            for f in matching_files:
                commented_only_unused.append((f, references))

    unused_files = list(dict.fromkeys(unused_files))  # Remove duplicates

    # Print summary
    print(f"Found {len(unused_files)} unused files out of {len(asciidoc_files)} total files in scan directories")

    # Generate detailed report for commented-only references
    if commented_only_unused and not include_commented:
        report_path = os.path.join(archive_dir, 'commented-references-report.txt')
        os.makedirs(archive_dir, exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as report:
            report.write("Files Referenced Only in Commented Lines\n")
            report.write("=" * 70 + "\n\n")
            report.write(f"Found {len(commented_only_unused)} files that are referenced only in commented-out includes.\n")
            report.write("These files are considered 'used' by default and will NOT be archived.\n\n")
            report.write("To archive these files along with other unused files, use the --commented flag.\n\n")
            report.write("-" * 70 + "\n\n")

            for file_path, references in sorted(commented_only_unused):
                report.write(f"File: {file_path}\n")
                report.write(f"Referenced in {len(references)} commented line(s):\n")
                for ref_file, line_num, line_text in references:
                    report.write(f"  {ref_file}:{line_num}\n")
                    report.write(f"    {line_text}\n")
                report.write("\n")

        print(f"\n📋 Found {len(commented_only_unused)} files referenced only in commented lines.")
        print(f"   Detailed report saved to: {report_path}")
        print(f"   These files are considered 'used' and will NOT be archived by default.")
        print(f"   To include them in the archive operation, use the --commented flag.\n")

    return write_manifest_and_archive(
        unused_files, archive_dir, 'to-archive', 'to-archive', archive=archive
    )
