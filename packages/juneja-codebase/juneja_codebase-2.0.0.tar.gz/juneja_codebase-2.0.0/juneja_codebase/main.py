#!/usr/bin/env python3
"""
Main CLI entry point for juneja-codebase
"""

import argparse
import os
import shutil
import zipfile
from pathlib import Path


def get_templates_dir():
    """Get the path to the templates directory"""
    return Path(__file__).parent / "templates"


def list_subjects():
    """List all available subjects"""
    templates_dir = get_templates_dir()
    subjects = [d.name for d in templates_dir.iterdir() if d.is_dir()]
    return subjects


def copy_subject_files(subject, output_dir):
    """Copy files for a specific subject to the output directory"""
    templates_dir = get_templates_dir()
    subject_dir = templates_dir / subject
    
    if not subject_dir.exists():
        print(f"Error: Subject '{subject}' not found!")
        print(f"Available subjects: {', '.join(list_subjects())}")
        return False
    
    output_path = Path(output_dir) / subject
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Copy all files from subject directory
    for item in subject_dir.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(subject_dir)
            dest_path = output_path / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_path)
            print(f"Created: {dest_path}")
    
    return True


def copy_all_subjects(output_dir):
    """Copy files for all subjects to the output directory"""
    subjects = list_subjects()
    success = True
    
    for subject in subjects:
        print(f"\n=== Generating {subject} files ===")
        if not copy_subject_files(subject, output_dir):
            success = False
    
    return success


def create_zip_archive(subject, output_file):
    """Create a zip archive for a specific subject or all subjects"""
    templates_dir = get_templates_dir()
    
    if subject:
        # Zip specific subject
        subject_dir = templates_dir / subject
        if not subject_dir.exists():
            print(f"Error: Subject '{subject}' not found!")
            return False
        
        zip_name = output_file if output_file else f"{subject}.zip"
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in subject_dir.rglob('*'):
                if item.is_file():
                    arcname = subject / item.relative_to(subject_dir)
                    zipf.write(item, arcname)
                    print(f"Added to zip: {arcname}")
        
        print(f"\n✓ Created zip file: {zip_name}")
        return True
    else:
        # Zip all subjects
        zip_name = output_file if output_file else "all_subjects.zip"
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for subject_dir in templates_dir.iterdir():
                if subject_dir.is_dir():
                    print(f"\nAdding {subject_dir.name} to zip...")
                    for item in subject_dir.rglob('*'):
                        if item.is_file():
                            arcname = item.relative_to(templates_dir)
                            zipf.write(item, arcname)
                            print(f"Added: {arcname}")
        
        print(f"\n✓ Created zip file: {zip_name}")
        return True


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="Generate code files for academic practicals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    juneja-codebase --list                              # List available subjects
    juneja-codebase --all                               # Generate all code files
    juneja-codebase --subject compiler_design           # Generate specific subject files
    juneja-codebase --all --output ./my_codes           # Generate to specific directory
    juneja-codebase --all --zip                         # Create zip of all subjects
    juneja-codebase --subject compiler_design --zip     # Create zip of specific subject
        """
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available subjects'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Generate code files for all subjects'
    )
    
    parser.add_argument(
        '--subject', '-s',
        type=str,
        help='Generate code files for a specific subject'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='.',
        help='Output directory or zip filename (default: current directory)'
    )
    
    parser.add_argument(
        '--zip', '-z',
        action='store_true',
        help='Create a zip file instead of extracting files'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    # List subjects
    if args.list:
        subjects = list_subjects()
        print("Available subjects:")
        for i, subject in enumerate(subjects, 1):
            print(f"  {i}. {subject}")
        return
    
    # Create zip archive
    if args.zip:
        if args.all:
            create_zip_archive(None, args.output if args.output != '.' else None)
        elif args.subject:
            create_zip_archive(args.subject, args.output if args.output != '.' else None)
        else:
            print("Error: Please specify --all or --subject with --zip")
            parser.print_help()
        return
    
    # Generate files
    if args.all:
        print("Generating all subject files...")
        copy_all_subjects(args.output)
        print(f"\n✓ All files generated in: {os.path.abspath(args.output)}")
    elif args.subject:
        print(f"Generating {args.subject} files...")
        copy_subject_files(args.subject, args.output)
        print(f"\n✓ Files generated in: {os.path.abspath(args.output)}")
    else:
        # No action specified, show help
        parser.print_help()
        print("\n" + "="*70)
    print("💡 TIP: If 'juneja-codebase' command doesn't work in your system, use:")
    print("    python -m juneja_codebase.main --list")
    print("    python -m juneja_codebase.main --all")
        print("="*70)


if __name__ == '__main__':
    main()
