import os
import sys
import glob
import re
import readline
import argparse
from kml2g1000 import export
import fas
import pandas as pd
import copy
from datetime import datetime

# Function to enable tab-completion for file paths
def complete_path(text, state):
    import glob
    return (glob.glob(text + '*') + [None])[state]

# Enable tab-completion for input
readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete_path)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='KML to G1000 CSV Converter')
parser.add_argument('--input-kml', type=str, help='Path to the input KML file')
parser.add_argument('--input-kml-dir', type=str, help='Path to the directory containing KML files')
parser.add_argument('--input-url', type=str, help='URL of the KML file to download')
parser.add_argument('--output-csv', type=str, help='Path to the output CSV file (only for single file input)')
parser.add_argument('--output-csv-dir', type=str, help='Path to the directory to save output CSV files (only for directory input)')
args = parser.parse_args()

def local(searchDir=None, outputDir=None):
    if not searchDir:
        print("Error: No input directory specified.")
        sys.exit(1)
    searchDir = os.path.abspath(searchDir)

    # Set output directory to the input directory if not specified
    if not outputDir:
        outputDir = os.path.abspath(searchDir)

    # Create output directory if it doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Search for KML files in the specified directory
    for kml in glob.glob(os.path.join(searchDir, '*.kml')):
        output_file = os.path.join(outputDir, os.path.basename(kml).replace('.kml', '.csv'))
        if os.path.exists(output_file):
            overwrite = input(f"File '{output_file}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                print(f"Skipping {kml}...")
                continue

        print(f"Exporting {kml} to csv...")
        export(kml, output_file)
        print("Done!")

    # Count the total number of KML files
    total_files = len(glob.glob(os.path.join(searchDir, '*.kml')))
    print(f"A total of {total_files} files in '{searchDir}' folder were exported to csv.")

def remote():
    tn = input("Enter the tail number of your aircraft : ")
    
    print(f"Finding history for aircraft: {tn}...")
    tn = tn.upper()
    
    # Debugging: print tail number
    print(f"DEBUG: Tail number after conversion to upper case: {tn}")
    
    pdataRAW = fas.findPlaneData(tn)
    
    # Debugging: print raw plane data response
    print(f"DEBUG: Raw plane data response: {pdataRAW}")
    
    if not pdataRAW:
        print("No data found for the specified tail number.")
        return
    
    pdataDisplay = copy.deepcopy(pdataRAW)
    _data = ["Date", "Time", "Departure", "Destination"]

    for flight in pdataDisplay:
        flight[0] = datetime.strptime(flight[0], "%Y%m%d").strftime("%m/%d/%Y")
        flight[1] = datetime.strptime(flight[1][:-1], "%H%M").strftime("%H:%M " + "Z")
    
    historyData = pd.DataFrame(pdataDisplay, columns=_data)
    print(f"Found {len(pdataRAW)} flights for {tn} within the last 14 days:")
    print("#"*100)
    print(historyData)
    
    flight = input("Enter the flight you would like to download: ")
    if not re.fullmatch("^([0-9]){1}$|^([1-9]){2}$", flight) or int(flight) >= len(pdataRAW):
        print("ERROR: Invalid flight number. Exiting...")
        sys.exit(1)
    
    print(f"Downloading flight {flight}...")
    trackRAW = fas.downloadKML(tn, pdataRAW, int(flight))
    
    # Debugging: print raw track data response
    print(f"DEBUG: Raw track data response status: {trackRAW.status_code}")
    
    with open("track.kml", "wb") as f:
        f.write(trackRAW.content)
    print("Done!")
    
    local()

def fURL(url, output_file=None):
    import atexit
    output_file = "track.kml"  # Temporary file to store wget download

    # Register cleanup function to delete the downloaded file when the script exits
    def cleanup():
        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"Deleted temporary file: {output_file}")
    atexit.register(cleanup)
    print(f"Downloading track from {url}...")
    trackRAW = fas.downloadFromURL(url)
    
    # Debugging: print URL
    print(f"DEBUG: URL: {url}")
    
    if trackRAW is not None:
        print("DEBUG: File downloaded successfully.")
        
        with open(output_file, "wb") as f:
            f.write(trackRAW.read())
        print("Done!")
    else:
        print("Failed to download the track from the URL. Exiting...")
        sys.exit(1)

# Main logic based on command-line arguments
if args.input_kml_dir:
    if not os.path.isdir(args.input_kml_dir):
        print(f"Error: The specified input directory '{args.input_kml_dir}' does not exist.")
        sys.exit(1)
    
    outputDir = args.output_csv_dir if args.output_csv_dir else args.input_kml_dir
    local(searchDir=args.input_kml_dir, outputDir=os.path.abspath(outputDir))

elif args.input_kml:
    if os.path.isdir(args.input_kml):
        # Process all KML files in the directory
        local(searchDir=args.input_kml)
    else:
        # Process a single KML file
        if args.output_csv:
            if args.output_csv and os.path.exists(args.output_csv):
                overwrite = input(f"File '{args.output_csv}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
                if overwrite != 'y':
                    print(f"Skipping '{args.input_kml}'...")
                    sys.exit(0)
            print(f"Exporting '{args.input_kml}'...")
            export(args.input_kml, args.output_csv)
            print(f"Exported '{args.input_kml}' to '{args.output_csv}'")
        else:
            default_output = args.input_kml.replace('.kml', '.csv')
            export(args.input_kml, default_output)
            print(f"Exported '{args.input_kml}' to '{default_output}'")

elif args.input_url:
    fURL(args.input_url, args.output_csv)

else:
    print()
    print("Welcome to the KML to G1000 converter!")
    print("This program will convert all KML files in a folder to CSV files that can be imported into the Garmin G1000.")
    print("Please select an option:")
    print("\t\t1. Convert files in a local directory")
    print("\t\t2. Find files directly on flightaware.com")
    print("\t\t3. Input a URL")
    option = input("$: ")
    
    if option == '1':
        searchDir = input('Enter the directory containing the KML files: ').strip()
        if not searchDir:
            print("Error: No input directory specified.")
            sys.exit(1)
        outputDir = input('Enter the output directory for CSV files (leave blank to use the input directory): ').strip()
        if not outputDir:
            outputDir = searchDir
        local(searchDir=searchDir, outputDir=os.path.abspath(outputDir))
    elif option == '2':
        remote()
    elif option == '3':
        url = input("Enter the full URL to the track file you want to download: ")
        fURL(url)
    else:
        print("Invalid option. Exiting...")
        sys.exit(1)
