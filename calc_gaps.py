import os
import csv
import sys
import copy

'''
Calculates delta gap between time stamp.
Used for segmenting "flights"
Flights are segmented if time gap > 30 sec.
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

v_read = "v8"
v_write = "v9"

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
        prev_row = []
        cur_flight = 0

        with open(out_file, "w", encoding="utf-8", newline="") as data_out:
            csv_out = csv.writer(data_out)
            out_header = copy.deepcopy(header)
            out_header.append("delta_time")
            out_header.append("flt_num")
            csv_out.writerow(out_header)

            last_plane = ""
            last_time = 0
            for row in csv_in:
                icao = row[pos["icao24"]]
                row_time = int(row[pos["time"]])
                if icao == last_plane:
                    delta = row_time-last_time
                    last_time = row_time
                    if delta > 45:
                        cur_flight += 1
                else:
                    cur_flight = 0
                    delta = 0
                    last_plane = icao
                    last_time = row_time

                row.append(delta)
                row.append(cur_flight)
                csv_out.writerow(row)
