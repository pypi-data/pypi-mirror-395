#!/usr/bin/env python3
"""
Dataset Builder CLI Tool

Build custom golden datasets for Nova tasks from the command line.

Usage:
    python dataset_builder.py task.yaml my-dataset
    python dataset_builder.py task.yaml my-dataset --output /custom/path
    python dataset_builder.py task.yaml my-dataset --gcs gs://my-bucket
    python dataset_builder.py --validate task.yaml /path/to/dataset
"""
import argparse
import sys
import yaml
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.workflows.dataset_builder import (
    build_dataset_from_task,
    build_dataset_from_dict,
    DatasetBuilder
)


def build_command(args):
    """Execute build command."""
    print(f"\n🚀 Building dataset from {args.task_yaml}")

    result = build_dataset_from_task(
        task_yaml_path=args.task_yaml,
        dataset_name=args.dataset_name,
        output_dir=args.output,
        gcs_bucket=args.gcs,
        upload=args.upload
    )

    print(f"\n✅ Build Complete!")
    print(f"   📁 Local path: {result['dataset_path']}")
    print(f"   📋 Task ID: {result['task_id']}")
    print(f"   📊 Completeness: {result['validation']['completeness']:.1f}%")

    if result['validation']['errors']:
        print(f"\n   ❌ Errors:")
        for error in result['validation']['errors']:
            print(f"      - {error}")

    if result['validation']['warnings']:
        print(f"\n   ⚠️  Warnings:")
        for warning in result['validation']['warnings']:
            print(f"      - {warning}")

    if result['uploaded']:
        print(f"\n   ☁️  Uploaded to: {result['gcs_path']}")

    return 0 if result['validation']['valid'] else 1


def validate_command(args):
    """Execute validate command."""
    print(f"\n🔍 Validating dataset at {args.dataset_path}")

    # Load task data
    with open(args.task_yaml, 'r') as f:
        task_data = yaml.safe_load(f)

    builder = DatasetBuilder(
        task_data=task_data,
        output_dir=str(Path(args.dataset_path).parent)
    )

    validation = builder.validate_dataset(Path(args.dataset_path))

    print(f"\n📊 Validation Results:")
    print(f"   Valid: {'✅ Yes' if validation['valid'] else '❌ No'}")
    print(f"   Completeness: {validation['completeness']:.1f}%")

    if validation['errors']:
        print(f"\n   ❌ Errors:")
        for error in validation['errors']:
            print(f"      - {error}")

    if validation['warnings']:
        print(f"\n   ⚠️  Warnings:")
        for warning in validation['warnings']:
            print(f"      - {warning}")

    return 0 if validation['valid'] else 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Build golden datasets for Nova tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build dataset locally
  %(prog)s task.yaml my-dataset

  # Build and upload to GCS
  %(prog)s task.yaml my-dataset --gcs gs://my-bucket

  # Build with custom output directory
  %(prog)s task.yaml my-dataset --output /custom/path

  # Validate existing dataset
  %(prog)s --validate task.yaml /path/to/dataset

  # Build without uploading
  %(prog)s task.yaml my-dataset --gcs gs://my-bucket --no-upload
        """
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate dataset instead of building'
    )

    parser.add_argument(
        'task_yaml',
        help='Path to task YAML definition file'
    )

    parser.add_argument(
        'dataset_name',
        help='Dataset name (for build) or path (for validate)'
    )

    parser.add_argument(
        '--output', '-o',
        default='/tmp/golden-datasets',
        help='Output directory for datasets (default: /tmp/golden-datasets)'
    )

    parser.add_argument(
        '--gcs', '-g',
        help='GCS bucket to upload dataset (e.g., gs://my-bucket)'
    )

    parser.add_argument(
        '--no-upload',
        dest='upload',
        action='store_false',
        help='Do not upload to GCS even if bucket specified'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Dataset Builder CLI v1.0.0'
    )

    args = parser.parse_args()

    # Validate task YAML exists
    if not Path(args.task_yaml).exists():
        print(f"❌ Error: Task YAML file not found: {args.task_yaml}")
        return 1

    # Execute appropriate command
    try:
        if args.validate:
            return validate_command(args)
        else:
            return build_command(args)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
