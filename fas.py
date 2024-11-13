import requests

def findPlaneData(tail_number):
    # Simulated function to find plane data; replace this with actual logic as needed
    return [
        ["20241031", "1441Z", "KGON", "KGON"],
        ["20241030", "1500Z", "KGON", "KBDL"]
    ]

def downloadKML(tail_number, plane_data, flight_index):
    # Simulated download of KML; replace with actual API call if needed
    url = f"https://www.example.com/kml/{tail_number}/{plane_data[flight_index][0]}"
    response = requests.get(url)
    response.raise_for_status()
    return response

import subprocess

def downloadFromURL(url, headers=None):
    # Modify URL by removing '/tracklog' and adding '/google_earth'
    if url.endswith('/tracklog'):
        url = url.rsplit('/tracklog', 1)[0] + '/google_earth'
    print(f"DEBUG: Modified URL: {url}")
    
    # Use wget to download the file directly if authentication isn't required
    try:
        output_file = "track.kml"
        result = subprocess.run(["wget", "-O", output_file, url], check=True, capture_output=True, text=True)
        print(result.stdout)
        return open(output_file, "rb")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading from URL using wget: {e.stderr}")
        return None
    if url.endswith('/tracklog'):
        url = url.rsplit('/tracklog', 1)[0] + '/google_earth'
    print(f"DEBUG: Modified URL: {url}")
    # Modify URL by removing '/tracklog' and adding '/google_earth'
    if url.endswith('/tracklog'):
        url = url.rsplit('/tracklog', 1)[0] + '/google_earth'
    
