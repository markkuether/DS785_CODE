import os
import csv
import sys

'''
Reads a list of airplane mfr's and models
That we wish to keep or discard.

Reads in all files and only writes out
lines for the mfr and models we wish to keep.
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
disc_name = "mfr_removal_list.txt"
keep_name = "b_c_p_keep_list.txt"
disc_file = root_dir + disc_name
keep_file = root_dir + keep_name

v_read = "v4"
v_write = "v5"

in_root = "D:/output/csv_unfiltered/" + v_read + "/"
out_root = "D:/output/csv_unfiltered/" + v_write + "/"

headers = ["time", "icao24", "callsign"]
headers += ["mfr", "model"]
headers += ["lat", "lon", "velocity", "heading", "vertrate"]
headers += ["baroaltitude", "geoaltitude"]
headers += ["lastposupdate", "lastcontact"]
pos = {hdr: index for index, hdr in enumerate(headers)}
keep = set([])
discard = set([])
disc_mfr = []  # Mfg's with aircraft to discard
keep_b_c_p = []  # Models to keep for Beech, Cessna, or Piper
bch = "BEECH"
csn = "CESSNA"
ppr = "PIPER"

# populate customer lists of mfr and models
with open(disc_file, "r", encoding="utf-8") as mfr_data:
    line = mfr_data.readline().strip().upper()
    while line:
        disc_mfr.append(line)
        line = mfr_data.readline().strip().upper()

with open(keep_file, "r", encoding="utf-8") as model_data:
    line = model_data.readline().strip().upper()
    while line:
        keep_b_c_p.append(line)
        line = model_data.readline().strip().upper()

all_files = get_files(in_root)

for in_name in all_files:
    in_file = in_root + in_name
    print(f"Processing {in_name}...")

    out_name = in_name[:-7]+"_" + v_write + ".csv"  # remove _v#.csv]
    out_file = out_root + out_name

    with open(in_file, "r", encoding="utf-8", newline="") as data_in:
        csv_in = csv.reader(data_in)
        header = next(csv_in)

        with open(out_file, "w", encoding="utf-8", newline="") as data_out:
            csv_out = csv.writer(data_out)
            csv_out.writerow(header)

            for row in csv_in:
                code = row[pos["icao24"]].strip().upper()
                mfr = row[pos["mfr"]].strip().upper()
                model = row[pos["model"]].strip().upper()

                # FILTERING LOGIC
                copy_row = True
                will_keep = (code in keep)
                wont_keep = (code in discard)

                if will_keep:
                    copy_row = True

                if wont_keep:
                    copy_row = False

                if (not will_keep) and (not wont_keep):
                    if mfr in disc_mfr:
                        copy_row = False
                        discard.add(code)
                    elif (bch in mfr) or (csn in mfr) or (ppr in mfr):
                        if model in keep_b_c_p:
                            copy_row = True
                            keep.add(code)
                        else:  # b_c_p we are not keeping
                            copy_row = False
                            discard.add(code)
                    else:  # all other airplane types
                        copy_row = True
                        keep.add(code)

                # Write to file.
                if copy_row:
                    csv_out.writerow(row)
