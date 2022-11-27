from datetime import datetime
import os
import sys

'''
Parses raw text files from OPENSKY network.
Transforms measures to english nautical units.
Writes output as a csv file.
'''


def get_files(path_name: str):
    # Gets list of files to process
    file_list = []
    full_listing = os.listdir(path_name)
    for item in full_listing:
        if item.endswith("_raw.txt"):
            file_list.append(item)
    return file_list


def to_knots(vel: str):
    # Converts from meters per second
    # to knots (naut miles per hour)
    try:
        meters_per_sec = float(vel)
        knot = round(meters_per_sec * 1.94384, 1)
        knot_str = str(knot)
    except:
        knot_str = vel

    return knot_str


def to_feet(meters: str):
    # Converts from meters to feet
    try:
        meters_val = float(meters)
        feet = round(meters_val * 3.28084, 1)
        feet_str = str(feet)
    except:
        feet_str = meters

    return feet_str


def to_fpm(mps: str):
    # converts from meters per second
    # to feet per minute
    try:
        meters_per_sec = float(mps)
        feet_per_sec = meters_per_sec * 0.3048
        feet_per_min = feet_per_sec * 60
        fpm = str(round(feet_per_min, 1))
    except:
        fpm = mps
    return fpm


#############
# MAIN CODE #
#############
'''
BASIS FOR FILTERING DATA
Data table starts with (+---...)
Data lines start with pipe symbol (|)
Header rows contain the text 'time'
Data rows do not contain the text 'time'
Non data rows do not start with (|) or (+---...)
Headers for all files are the same.
'''


in_root = "D:/input/"
out_root = "D:/output/csv_unfiltered/"
headers = ["time", "icao24", "callsign"]
headers += ["lat", "lon", "velocity", "heading", "vertrate"]
headers += ["baroaltitude", "geoaltitude"]
headers += ["lastposupdate", "lastcontact"]
pos = {hdr: index for index, hdr in enumerate(headers)}
header_line = ",".join(headers)
header_line += "\n"

# Gather list of files to process
file_list = get_files("d:/input/")
for in_name in file_list:
    in_file = in_root + in_name
    byte_size = os.stat(in_file).st_size
    mb_size = round(byte_size/1024/1024, 0)
    print(f"Processing {in_name} - {mb_size}MB...")

    out_name = in_name[:-8] + ".csv"  # Remove _raw.txt
    out_file = out_root + out_name

    is_header = False
    with open(in_file, "r", encoding="utf-8") as data_in:
        with open(out_file, "w", encoding="utf-8") as data_out:

            # Write headers to output file.
            data_out.write(header_line)

            # Read through start of log to start of data.
            # For all files, there should be no blank lines.
            # If we read 10 blank lines - end of file.
            blank_count = 0
            line = "X"
            is_table = False
            eof = False
            while (not eof) and (not is_table):
                is_table = ("+---" in line)
                if not line:
                    blank_count += 1
                    eof = (blank_count > 10)
                line = data_in.readline().strip()

            # We are now either at the end of the file
            # or at the top of the data table(s).
            # Read data
            while not eof:
                is_header = ("time" in line)
                is_data = (line[:1] == "|")
                if (is_data) and (not is_header):
                    line = line[1:-1]  # take off end pipes
                    data = line.split("|")
                    data = [item.strip() for item in data]

                    # Convert from metric to english
                    # includes rounding to single point precision
                    data[pos["velocity"]] = to_knots(data[pos["velocity"]])
                    data[pos["baroaltitude"]] = to_feet(
                        data[pos["baroaltitude"]])
                    data[pos["geoaltitude"]] = to_feet(
                        data[pos["geoaltitude"]])
                    data[pos["vertrate"]] = to_fpm(data[pos["vertrate"]])

                    # Round heading to single point precision
                    # for readability
                    hdg = float(data[pos["heading"]])
                    data[pos["heading"]] = str(round(hdg, 1))

                    # Reformat and write out to csv
                    line_out = ",".join(data)
                    line_out += "\n"
                    data_out.write(line_out)

                line = data_in.readline().strip()
                if not line:
                    blank_count += 1
                    eof = (blank_count > 10)

print("COMPLETED")
