import csv
import os

'''
Reads through all CSV files
Builds dictionary for airplanes
using icao24 code.

If airplane is known, and call sign is null,
Fills in known callsign.

updates unfiltered data.
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
id_root = "D:/OUTPUT/"
id_name = "found_types.csv"
id_file = id_root + id_name

in_root = "D:/OUTPUT/csv_unfiltered/v2/"
out_root = "D:/OUTPUT/csv_unfiltered/v3/"

headers = ["time", "icao24", "callsign"]
headers += ["lat", "lon", "velocity", "heading", "vertrate"]
headers += ["baroaltitude", "geoaltitude"]
headers += ["lastposupdate", "lastcontact"]
pos = {hdr: index for index, hdr in enumerate(headers)}

id_hdrs = ["MODE_S_CODE_HEX", "N_NUMBER", "MFR", "model"]
idpos = {hdr: index for index, hdr in enumerate(id_hdrs)}

known_planes = {}  # {icao24:callsign}
# Step 1. Build a dictionary of known planes
print("CREATING DICTIONARY:")
with open(id_file, "r", encoding="utf-8-sig") as input_id:
    id_csv = csv.reader(input_id)
    hdr = next(id_csv)
    for row in id_csv:
        code = row[idpos["MODE_S_CODE_HEX"]].strip().upper()
        call_sign = row[idpos["N_NUMBER"]].strip().upper()
        known_planes[code] = call_sign


# STEP 2. Go back and replace "NULL" values.
# where we know the plane call sign
print()
print("UPDATING NULL VALS:")
all_files = get_files(in_root)
for in_name in all_files:
    print(f"Processing {in_name}....")
    in_file = in_root + in_name
    out_name = in_name[:-7] + "_v3.csv"  # remove .csv
    mod_file = out_root + out_name

    with open(in_file, "r", encoding="utf-8", newline="") as data_in:
        with open(mod_file, "w", encoding="utf-8", newline="") as data_out:

            csv_in = csv.reader(data_in)
            csv_out = csv.writer(data_out)

            header = next(csv_in)
            csv_out.writerow(header)

            for row in csv_in:
                code = row[pos["icao24"]].strip().upper()
                call_sign = row[pos["callsign"]].strip().upper()
                if call_sign == "NULL":
                    if code in known_planes:
                        row[pos["callsign"]] = known_planes[code]
                csv_out.writerow(row)


# STEP 3. Write out all unknown_planes
# remaining to log file. We need to look
# these up.

print("COMPLETED")
