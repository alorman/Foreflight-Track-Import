#!/usr/bin/env python3

import argparse
import os
import sys
import glob

# Import the 'export' function from your updated kml2g1000.py
# Make sure kml2g1000.py is in the same folder or install it as a module.
from kml2g1000 import export


def convert_single_kml(input_kml, output_csv=None):
    """
    Convert a single KML file to CSV.
    If output_csv is None, use the same directory & base name as the input KML.
    If output_csv exists, skip conversion.
    """
    input_kml = os.path.abspath(input_kml)

    # Ensure the single KML file actually exists
    if not os.path.isfile(input_kml):
        print(f"Error: KML file '{input_kml}' does not exist.")
        sys.exit(1)

    # Determine the final CSV path
    if output_csv is None:
        base, _ = os.path.splitext(input_kml)
        output_csv = base + '.csv'
    else:
        output_csv = os.path.abspath(output_csv)

        # If the user provided a directory, use the same base name
        if os.path.isdir(output_csv):
            base_name = os.path.splitext(os.path.basename(input_kml))[0] + '.csv'
            output_csv = os.path.join(output_csv, base_name)
        else:
            # If it's a file, ensure the parent directory exists
            out_dir = os.path.dirname(output_csv) or '.'
            if not os.path.isdir(out_dir):
                print(f"Error: Output directory '{out_dir}' does not exist.")
                sys.exit(1)

    # Skip if file already exists
    if os.path.exists(output_csv):
        print(f"Skipping '{output_csv}' (already exists).")
        return

    print(f"Converting '{input_kml}' -> '{output_csv}'")
    try:
        # Call the export function, passing the exact output file path
        export(input_kml, output_csv)
    except Exception as e:
        print(f"Error converting '{input_kml}': {e}")
        sys.exit(1)
    else:
        print(f"Done converting '{input_kml}' -> '{output_csv}'")


def convert_directory_kml(input_kml_dir, output_csv_dir=None):
    """
    Convert all KML files in a directory to CSV.
    If output_csv_dir is None, use the same directory as the input_kml_dir.
    If output files exist, skip them.
    Throw an error if the directory doesn't exist.
    """
    input_kml_dir = os.path.abspath(input_kml_dir)
    if not os.path.isdir(input_kml_dir):
        print(f"Error: Input directory '{input_kml_dir}' does not exist.")
        sys.exit(1)

    if output_csv_dir is None:
        # Use the same directory for outputs
        output_csv_dir = input_kml_dir
    else:
        output_csv_dir = os.path.abspath(output_csv_dir)
        # Throw an error if this output directory doesn't exist
        if not os.path.isdir(output_csv_dir):
            print(f"Error: Output directory '{output_csv_dir}' does not exist.")
            sys.exit(1)

    # Find all KML files
    kml_files = glob.glob(os.path.join(input_kml_dir, '*.kml'))
    if not kml_files:
        print(f"No KML files found in '{input_kml_dir}'")
        return

    for kml_path in kml_files:
        base_name = os.path.splitext(os.path.basename(kml_path))[0] + '.csv'
        output_path = os.path.join(output_csv_dir, base_name)

        if os.path.exists(output_path):
            print(f"Skipping '{output_path}' (already exists).")
            continue

        print(f"Converting '{kml_path}' -> '{output_path}'")
        try:
            export(kml_path, output_path)
        except Exception as e:
            print(f"Error converting '{kml_path}': {e}")
        else:
            print(f"Done converting '{kml_path}' -> '{output_path}'")

    print("All possible KML files have been processed.")


def download_and_convert_url(input_url, output_csv=None):
    """
    Example placeholder for downloading from a FlightAware URL, saving a KML,
    then converting to CSV. Adjust for your actual download logic.
    """
    import requests
    import tempfile

    print(f"Downloading KML from URL: {input_url}")
    try:
        resp = requests.get(input_url)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to download KML from {input_url}: {e}")
        sys.exit(1)

    # Write the downloaded KML to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kml', delete=False) as tmp:
        tmp.write(resp.content)
        tmp_kml_path = tmp.name

    print(f"Download complete. Temporary KML saved at {tmp_kml_path}")
    # Convert that KML to CSV
    convert_single_kml(tmp_kml_path, output_csv)

    # Optionally remove the temp file
    try:
        os.remove(tmp_kml_path)
        print(f"Removed temporary file: {tmp_kml_path}")
    except OSError as e:
        print(f"Could not delete temp file {tmp_kml_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='KML to G1000 CSV Converter',
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Input arguments
    parser.add_argument(
        '--input-kml',
        type=str,
        help='Specify a single KML file (ForeFlight or FlightAware) for conversion.'
    )
    parser.add_argument(
        '--input-kml-dir',
        type=str,
        help='Specify a directory of KML files (acts on all *.kml in the directory).'
    )
    parser.add_argument(
        '--input-url',
        type=str,
        help='Specify a FlightAware (or other) URL to download a KML for conversion.'
    )

    # Output arguments
    parser.add_argument(
        '--output-csv',
        type=str,
        help=(
            "Output CSV file name for a single KML. "
            "If not specified, uses the same directory/name as --input-kml. "
            "Skipped if a file with this name already exists."
        )
    )
    parser.add_argument(
        '--output-csv-dir',
        type=str,
        help=(
            "Output directory for multiple CSV files, used with --input-kml-dir. "
            "If not specified, uses the same directory as --input-kml-dir. "
            "Skipped if files already exist. If the directory does not exist, "
            "the script throws an error and exits."
        )
    )

    args = parser.parse_args()

    # Decide which operation to perform
    if args.input_kml_dir:
        convert_directory_kml(args.input_kml_dir, args.output_csv_dir)
    elif args.input_kml:
        convert_single_kml(args.input_kml, args.output_csv)
    elif args.input_url:
        download_and_convert_url(args.input_url, args.output_csv)
    else:
        # No valid sub-command provided; print usage and exit
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
