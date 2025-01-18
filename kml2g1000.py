import os
import math
from datetime import datetime
from lxml import etree as ET

def get_download_path():
    """Returns the path to the default download folder (Windows or Unix-like)."""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def getAll(root, node):
    """
    Returns an array containing the texts of all the specified child nodes of root.
    :param root: lxml root element
    :param node: node name to find
    :return: list of text values
    """
    return [_.text for _ in root.iterfind('.//' + node, namespaces=root.nsmap)]

def calcSpeed(fm, to, start, end):
    """
    Calculates the groundspeed given two lat/long coordinates and associated start/end datetimes.
    :param fm: (lat, lng) of the "from" point (float, float)
    :param to: (lat, lng) of the "to" point   (float, float)
    :param start: datetime of the "from" point
    :param end:   datetime of the "to" point
    :return: integer speed in knots
    """
    import math
    if not fm or not to:
        return 0
    dx = math.hypot(*[b - a for a, b in zip(fm, to)]) * 60.0  # distance in nautical miles
    dt = (end - start).total_seconds() / 3600.0  # time in hours
    return round(dx / dt) if dt else 0

def export(input_kml, output_path=None):
    """
    Converts a KML track log into G1000 CSV format.
    If 'output_path' is a file path, writes to that exact file.
    If 'output_path' is a directory, writes basename.csv inside it.
    If 'output_path' is None, writes to the default downloads folder.

    :param input_kml:   Path to the .kml file
    :param output_path: Path (file or directory) for the .csv output
    :return: None
    """
    # 1. Determine final CSV path
    if not output_path:
        # Default to user's download folder
        default_dir = get_download_path()
        base_name = os.path.splitext(os.path.basename(input_kml))[0] + '.csv'
        file_path = os.path.join(default_dir, base_name)
    else:
        # User supplied something. Check if it's a dir or a file
        output_path = os.path.abspath(output_path)
        if os.path.isdir(output_path):
            # It's a directory, so append the KML's base name + .csv
            base_name = os.path.splitext(os.path.basename(input_kml))[0] + '.csv'
            file_path = os.path.join(output_path, base_name)
        else:
            # It's a file path
            file_path = output_path

    # 2. Print debug info (optional, remove if too verbose)
    print(f"DEBUG inside kml2g1000.export() --> Input KML: {input_kml}")
    print(f"DEBUG inside kml2g1000.export() --> Output CSV: {file_path}")

    # 3. If you still want to skip existing files, you can check here
    #    or let the caller handle overwriting logic. For now, we'll keep a simple check:
    if os.path.exists(file_path):
        print(f"Skipping {file_path} (already exists)")
        return

    # 4. Prepare G1000 CSV header, format, etc.
    hdr = (
        "  Lcl Date, Lcl Time, UTCOfst, AtvWpt,     Latitude,    Longitude,    AltB, "
        "BaroA,  AltMSL,   OAT,    IAS, GndSpd,    VSpd,  Pitch,   Roll,  LatAc, "
        "NormAc,   HDG,   TRK, volt1,  FQtyL,  FQtyR, E1 FFlow, E1 FPres, E1 OilT, "
        "E1 OilP, E1 MAP, E1 RPM, E1 CHT1, E1 CHT2, E1 CHT3, E1 CHT4, E1 EGT1, "
        "E1 EGT2, E1 EGT3, E1 EGT4,  AltGPS, TAS, HSIS,    CRS,   NAV1,   NAV2, "
        "   COM1,    COM2,   HCDI,   VCDI, WndSpd, WndDr, WptDst, WptBrg, MagVar, "
        "AfcsOn, RollM, PitchM, RollC, PichC, VSpdG, GPSfix,  HAL,   VAL, "
        "HPLwas, HPLfd, VPLwas"
    )

    fmt = (
        "{date}, {time},   00:00,       , {lat: >12}, {lng: >12},        ,      , "
        "{alt: >7},      ,       , {gspd: >6}"
    )
    tail = (
        ",        ,       ,       ,       ,       ,      ,      ,      ,       ,       ,"
        "         ,         ,        ,        ,       ,       ,        ,        ,        ,"
        "        ,        ,        ,        ,        ,    ,     ,       ,       ,       ,"
        "        ,        ,       ,       ,       ,      ,       ,       ,       ,       ,"
        "      ,       ,      ,      ,      ,       ,     ,      ,       ,      ,       "
    )

    # 5. Parse the KML
    tree = ET.parse(input_kml)
    root = tree.getroot()

    # Collect all timestamps and coordinates
    whens = getAll(root, 'when')
    coords = getAll(root, 'gx:coord')

    # Create CSV data
    csv_lines = [hdr]

    # 6. Iterate all points in the KML
    fm = None
    start_time = None
    for when, coord in zip(whens, coords):
        # e.g. 2022-06-09T15:42:34.400527954Z
        date_str, time_str = when.split("T")
        time_str = time_str.rstrip("Z")  # remove trailing "Z"
        lng_str, lat_str, alt_str = coord.split(" ")

        # Convert to numerical
        lat_val = float(lat_str)
        lng_val = float(lng_str)
        alt_val = float(alt_str) * 3.28084  # meters -> feet

        # Compute ground speed
        to = (lat_val, lng_val)
        # remove fractional seconds from time_str if present
        time_str_simplified = time_str.split(".")[0]
        end_dt = datetime.strptime(
            date_str + " " + time_str_simplified, "%Y-%m-%d %H:%M:%S"
        )
        gspd = calcSpeed(fm, to, start_time, end_dt) if fm and start_time else 0
        fm = to
        start_time = end_dt

        # Build CSV line
        csv_line = fmt.format(
            date=date_str,
            time=time_str_simplified,
            lat=lat_val,
            lng=lng_val,
            alt=round(alt_val),
            gspd=gspd,
        )
        csv_lines.append(csv_line + tail)

    # 7. Finally, write the CSV file
    with open(file_path, "w") as f:
        f.write("\n".join(csv_lines) + "\n")

    print(f"Done. CSV exported to: {file_path}")
