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
parser.add_argument('--input-url', type=str, help='URL of the KML file to download')
parser.add_argument('--output-csv', type=str, help='Path to the output CSV file')
args = parser.parse_args()

def local(searchDir=None):
    if not searchDir:
        searchDir = input('Show me the directory containing the track files (defaults to user Downloads folder): ')
        if searchDir == '':
            searchDir = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:
            searchDir = os.path.abspath(searchDir)

    # Save the current working directory
    cwd = os.getcwd()

    # Change to the search directory
    os.chdir(searchDir)

    # Search for KML files in the current directory
    for kml in glob.glob('*.kml'):
        output_file = searchDir + "/" + kml.replace('.kml', '.csv')
        if os.path.exists(output_file):
            overwrite = input(f"File '{output_file}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                print(f"Skipping {kml}...")
                continue

        print(f"Exporting {kml} to csv...")
        export(searchDir + "/" + kml)
        print(f"Saving to {output_file}...")
        os.rename(kml.replace('.kml', '.csv'), output_file)
        print("Done!")

    # Change back to the original working directory
    os.chdir(cwd)

    # Count the total number of KML files
    os.chdir(searchDir)
    total_files = len(glob.glob('*.kml'))
    os.chdir(cwd)

    print(f"A total of {total_files} files in '{searchDir}' folder were exported to csv.")

def remote():
    tn = input("Enter the tail number of your aircraft : ")
    
    print(f"Finding history for aircraft: {tn}...")
    tn = tn.upper()
    pdataRAW = fas.findPlaneData(tn)
    
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
    with open("track.kml", "wb") as f:
        f.write(trackRAW.content)
    print("Done!")
    
    local()

def fURL(url, output_file=None):
    print(f"Downloading track from {url}...")
    trackRAW = fas.downloadFromURL(url)
    if not output_file:
        output_file = "track.kml"
    with open(output_file, "wb") as f:
        f.write(trackRAW.content)
    print("Done!")
    
    local()

# Main logic based on command-line arguments
if args.input_kml:
    if args.output_csv:
        if os.path.exists(args.output_file):
            overwrite = input(f"File '{args.output_file}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                print(f"Skipping '{args.input_file}'...")
                sys.exit(0)
        print(f"Exporting '{args.input_file}'...")
        export(args.input_file)
        print(f"Saving to '{args.output_file}'...")
        os.rename(args.input_file.replace('.kml', '.csv'), args.output_file)
        print(f"Exported '{args.input_file}' to '{args.output_file}'")
    else:
        default_output = args.input_file.replace('.kml', '.csv')
        export(args.input_file)
        print(f"Exported '{args.input_file}' to '{default_output}'")

elif args.input_url:
    fURL(args.input_url, args.output_file)

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
        local()
    elif option == '2':
        remote()
    elif option == '3':
        url = input("Enter the full URL to the track file you want to download: ")
        fURL(url)
    else:
        print("Invalid option. Exiting...")
        sys.exit(1)
