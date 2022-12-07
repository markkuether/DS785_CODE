import os
import csv
import sys
import copy


'''
This reads the title of each file and appends 3 columns
to represent the airplane call sign, the date, and the
airport to the data.

This is in prep for combining all files together for 
final analysis.
'''


def get_files(path_name: str):
    # Gets list of files to process
    file_list = []
    full_listing = os.listdir(path_name)
    for item in full_listing:
        if item.endswith(".csv"):
            file_list.append(item)
    return file_list


v_read = "v22"
v_write = "v23"

in_root = "D:/output/csv_unfiltered/" + v_read + "/"
out_root = "D:/output/csv_unfiltered/" + v_write + "/"
out_name = "all_data.csv"
out_file = out_root + out_name

headers = ["time", "icao24", "callsign"]
headers += ["mfr", "model"]
headers += ["lat", "lon", "velocity", "heading", "vertrate"]
headers += ["baroaltitude", "geoaltitude"]
headers += ["lastposupdate", "lastcontact"]
headers += ["delta_time", "flt_num", "apt_dst", "agl"]
headers += ["file_planeid", "file_apt", "file_date"]
pos = {hdr: index for index, hdr in enumerate(headers)}

with open(out_file, "w", encoding="utf-8", newline="") as data_out:
    csv_out = csv.writer(data_out)
    csv_out.writerow(headers)

all_files = get_files(in_root)
for in_name in all_files:
    in_file = in_root + in_name
    print(f"Processing {in_name}...")

    with open(in_file, "r", encoding="utf-8", newline="") as data_in:
        csv_in = csv.reader(data_in)
        header = next(csv_in)

        with open(out_file, "a", encoding="utf-8", newline="") as data_out:
            csv_out = csv.writer(data_out)
            for row in csv_in:
                csv_out.writerow(row)
