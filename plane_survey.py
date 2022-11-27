import csv
import os
'''
Reads all files and extracts the
airplane types across all files
Creates a CSV file with airplane
mfr and type for reference.

Used to visually identify planes
that could be filtered out of the
data, such as commercial jet liners
or helicopters.
'''

def get_files(path_name: str):
    # Gets list of files to process
    file_list = []
    full_listing = os.listdir(path_name)
    for item in full_listing:
        if item.endswith(".csv"):
            file_list.append(item)
    return file_list

#############
# MAIN CODE #
#############


in_root = "D:/output/csv_unfiltered/v4/"
out_root = "D:/output/"
out_name = "plane_survey.csv"
out_file = out_root + out_name
out_hdrs = ["MFR", "MODEL"]
all_types = set([])
headers = ["time", "icao24", "callsign"]
headers += ["mfr", "model"]
headers += ["lat", "lon", "velocity", "heading", "vertrate"]
headers += ["baroaltitude", "geoaltitude"]
headers += ["lastposupdate", "lastcontact"]
pos = {hdr: index for index, hdr in enumerate(headers)}

all_files = get_files(in_root)
with open(out_file, "w", encoding="utf-8", newline='') as data_out:
    csv_out = csv.writer(data_out)
    csv_out.writerow(out_hdrs)

    for in_name in all_files:
        print(f"Reading {in_name}...")
        in_file = in_root + in_name
        with open(in_file, "r", encoding="utf-8", newline='') as data_in:
            csv_in = csv.reader(data_in)
            header = next(csv_in)

            for row in csv_in:
                mfr = row[pos["mfr"]].strip().upper()
                model = row[pos["model"]].strip().upper()
                if mfr != "NA" and model != "NA":
                    all_types.add(mfr + "_" + model)

    for item in all_types:
        parts = item.split("_")
        csv_out.writerow(parts)

print("COMPLETE")
