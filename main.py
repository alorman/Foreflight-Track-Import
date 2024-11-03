import os
import sys
import glob
import re
from kml2g1000 import export
import fas
import pandas as pd
import copy
from datetime import datetime

def local():
    searchDir = input('Show me the directory containing the track files (defaults to user Downloads folder): ')
    if searchDir == '':
        searchDir = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Save the current working directory
    cwd = os.getcwd()

    # Change to the search directory
    os.chdir(searchDir)

    # Search for KML files in the current directory
    for kml in glob.glob('*.kml'):
        print(f"Exporting {kml} to csv...")
        export(searchDir + "/" + kml)
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

def fURL():
    url = input("Enter the full URL to the track file you want to download: ")
    print(f"Downloading track from {url}...")
    trackRAW = fas.downloadFromURL(url)
    with open("track.kml", "wb") as f:
        f.write(trackRAW.content)
    print("Done!")
    
    local()

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
    fURL()
else:
    print("Invalid option. Exiting...")
    sys.exit(1)
