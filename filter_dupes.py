import os
import csv
import sys

'''
Removes duplicate data points based on
latitude, longitude, velocity, and heading.

only writes original data points.
'''


def get_files(path_name: str):
    # Gets list of files to process
    file_list = []
    full_listing = os.listdir(path_name)
    for item in full_listing:
        if item.endswith(".csv"):
            file_list.append(item)
    return file_list


root_dir = "D:/OUTPUT/"

v_read = "v6"
v_write = "v8"

in_root = "D:/output/csv_unfiltered/" + v_read + "/"
out_root = "D:/output/csv_unfiltered/" + v_write + "/"

headers = ["time", "icao24", "callsign"]
headers += ["mfr", "model"]
headers += ["lat", "lon", "velocity", "heading", "vertrate"]
headers += ["baroaltitude", "geoaltitude"]
headers += ["lastposupdate", "lastcontact"]
pos = {hdr: index for index, hdr in enumerate(headers)}

all_files = get_files(in_root)

for in_name in all_files:
    in_file = in_root + in_name
    print(f"Processing {in_name}...")

    out_name = in_name[:-6] + v_write + ".csv"  # remove _v#.csv]
    out_file = out_root + out_name
    ac_data = set([])

    with open(in_file, "r", encoding="utf-8", newline="") as data_in:
        csv_in = csv.reader(data_in)
        header = next(csv_in)

        with open(out_file, "w", encoding="utf-8", newline="") as data_out:
            csv_out = csv.writer(data_out)
            csv_out.writerow(header)

            for row in csv_in:
                lat = row[pos["lat"]]
                lon = row[pos["lon"]]
                vel = row[pos["velocity"]]
                hdg = row[pos["heading"]]
                data_point = (lat, lon, vel, hdg)
                if data_point not in ac_data:
                    ac_data.add(data_point)
                    csv_out.writerow(row)
