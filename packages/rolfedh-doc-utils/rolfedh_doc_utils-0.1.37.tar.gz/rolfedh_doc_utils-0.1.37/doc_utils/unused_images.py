# doc_utils/unused_images.py

import os
import re
from .file_utils import collect_files, write_manifest_and_archive

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg'}

def find_unused_images(scan_dirs, archive_dir, archive=False, exclude_dirs=None, exclude_files=None, include_commented=False):
    # Print safety warning
    print("\n⚠️  SAFETY: Work in a git branch! Run without --archive first to preview.\n")

    image_files = collect_files(scan_dirs, IMAGE_EXTENSIONS, exclude_dirs, exclude_files)
    adoc_files = collect_files(['.'], {'.adoc'}, exclude_dirs, exclude_files)

    # Track which images are referenced (uncommented and commented separately)
    referenced_images = set()  # Images in uncommented references
    commented_only_images = {}  # Images referenced ONLY in commented lines: {basename: [(file, line_num, line_text)]}

    # Patterns for finding image references (both commented and uncommented)
    image_ref_pattern = re.compile(r'(?i)image::([^\[]+)[\[]|image:([^\[]+)[\[]|"([^"\s]+\.(?:png|jpg|jpeg|gif|svg))"')
    commented_line_pattern = re.compile(r'^\s*//')

    for adoc_file in adoc_files:
        try:
            with open(adoc_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    # Check if this line is commented
                    is_commented = commented_line_pattern.match(line)

                    # Find all image references in the line
                    for match in image_ref_pattern.findall(line):
                        for group in match:
                            if group:
                                image_basename = os.path.basename(group)

                                if is_commented:
                                    # Track location of commented reference
                                    if image_basename not in commented_only_images:
                                        commented_only_images[image_basename] = []
                                    commented_only_images[image_basename].append((adoc_file, line_num, line.strip()))
                                else:
                                    # Add to uncommented references
                                    referenced_images.add(image_basename)
                                    # If we found an uncommented reference, remove from commented_only tracking
                                    if image_basename in commented_only_images:
                                        del commented_only_images[image_basename]
        except Exception as e:
            print(f"Warning: could not read {adoc_file}: {e}")

    # Determine which images are unused based on the include_commented flag
    if include_commented:
        # When --commented is used: treat images with commented-only references as unused
        # Only images with uncommented references are considered "used"
        unused_images = [f for f in image_files if os.path.basename(f) not in referenced_images]
        commented_only_unused = []
    else:
        # Default behavior: images referenced only in commented lines are considered "used"
        # They should NOT be in the unused list, but we track them for reporting
        all_referenced = referenced_images.union(set(commented_only_images.keys()))
        unused_images = [f for f in image_files if os.path.basename(f) not in all_referenced]

        # Generate list of images referenced only in comments for the report
        commented_only_unused = []
        for basename, references in commented_only_images.items():
            # Find the full path for this basename in image_files
            matching_files = [f for f in image_files if os.path.basename(f) == basename]
            for f in matching_files:
                commented_only_unused.append((f, references))

    unused_images = list(dict.fromkeys(unused_images))

    # Generate detailed report for commented-only references
    if commented_only_unused and not include_commented:
        report_path = os.path.join(archive_dir, 'commented-image-references-report.txt')
        os.makedirs(archive_dir, exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as report:
            report.write("Images Referenced Only in Commented Lines\n")
            report.write("=" * 70 + "\n\n")
            report.write(f"Found {len(commented_only_unused)} images that are referenced only in commented-out lines.\n")
            report.write("These images are considered 'used' by default and will NOT be archived.\n\n")
            report.write("To archive these images along with other unused images, use the --commented flag.\n\n")
            report.write("-" * 70 + "\n\n")

            for file_path, references in sorted(commented_only_unused):
                report.write(f"Image: {file_path}\n")
                report.write(f"Referenced in {len(references)} commented line(s):\n")
                for ref_file, line_num, line_text in references:
                    report.write(f"  {ref_file}:{line_num}\n")
                    report.write(f"    {line_text}\n")
                report.write("\n")

        print(f"\n📋 Found {len(commented_only_unused)} images referenced only in commented lines.")
        print(f"   Detailed report saved to: {report_path}")
        print(f"   These images are considered 'used' and will NOT be archived by default.")
        print(f"   To include them in the archive operation, use the --commented flag.\n")

    return write_manifest_and_archive(
        unused_images, archive_dir, 'unused-images', 'unused-images', archive=archive
    )
