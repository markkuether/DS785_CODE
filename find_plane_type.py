import csv
import os
import pyodbc

'''
Reads through all CSV files
Builds dictionary for airplanes
using icao24 code.

Builds a SQL query to find mfg and model

Writes updates into next versions of tables.
'''


def get_files(path_name: str):
    # Gets list of files to process
    file_list = []
    full_listing = os.listdir(path_name)
    for item in full_listing:
        if item.endswith(".csv"):
            file_list.append(item)
    return file_list


def make_sql(hex_codes: set):
    sql_select = "SELECT m.MODE_S_CODE_HEX, r.MFR, r.MODEL"
    sql_from = "FROM FAA_Reg_Aircraft.dbo.MSTR AS m"
    sql_from += " JOIN FAA_Reg_Aircraft.dbo.ACFTREF AS r"
    sql_from += " ON m.MFR_MDL_CODE = r.CODE"
    sql_where = "WHERE MODE_S_CODE_HEX IN "
    sql_where += "("
    for item in hex_codes:
        sql_where += f"'{item}',"

    sql_where = sql_where[:-1]  # remove trailing comma
    sql_where += ")"

    sql_parts = [sql_select, sql_from, sql_where]
    sql_string = " ".join(sql_parts)
    sql_string += ";"  # needed for pyodbc

    return sql_string


'''
select m.MODE_S_CODE_HEX, r.MFR, r.MODEL
from FAA_Reg_Aircraft.dbo.MSTR as m
JOIN FAA_Reg_Aircraft.dbo.ACFTREF AS r
on m.MFR_MDL_CODE = r.CODE
where MODE_S_CODE_HEX in () 
'''


#############
# MAIN CODE #
#############
v_in = "v3"
v_out = "v4"
in_root = "D:/OUTPUT/CSV_UNFILTERED/" + v_in + "/"
out_root = "D:/OUTPUT/CSV_UNFILTERED/" + v_out + "/"


#out_root = "D:/OUTPUT/"
#out_log = "UNDEFINED_ADDRESSES.TXT"
#out_file = out_root + out_log

headers = ["time", "icao24", "callsign"]
headers += ["lat", "lon", "velocity", "heading", "vertrate"]
headers += ["baroaltitude", "geoaltitude"]
headers += ["lastposupdate", "lastcontact"]
pos = {hdr: index for index, hdr in enumerate(headers)}

out_hdrs = ["time", "icao24", "callsign"]
out_hdrs += ["mfr", "model"]
out_hdrs += ["lat", "lon", "velocity", "heading", "vertrate"]
out_hdrs += ["baroaltitude", "geoaltitude"]
out_hdrs += ["lastposupdate", "lastcontact"]

# {icao24:callsign}
all_files = get_files(in_root)
for in_name in all_files:
    in_file = in_root + in_name

    out_name = in_name[:-7] + "_" + v_out + ".csv"
    out_file = out_root + out_name

    print(f"Processing {in_name} --> {out_name}")

    hex_codes = set([])
    plane_models = {}
    print("   Reading icao24 codes...")
    with open(in_file, "r", encoding="utf-8", newline='') as data_in:
        csv_in = csv.reader(data_in)
        header = next(csv_in)

        for row in csv_in:
            code = row[pos["icao24"]]
            hex_codes.add(code)

    # Build dictionary of mfg and model
    print("   Building SQL Statement...")
    if len(hex_codes) > 0:
        sql_string = make_sql(hex_codes)
        print("   Connecting to database...")
        cnxn = pyodbc.connect('DSN=SQLEXPRESS;Trusted_Connection=yes;')
        cursor = cnxn.cursor()
        print("   Running Query & Filling Dictionary...")
        cursor.execute(sql_string)

        result_row = cursor.fetchone()
        while result_row:
            code = result_row[0].strip().upper()
            mfr = result_row[1].strip().upper()
            model = result_row[2].strip().upper()
            plane_models[code] = [mfr, model]
            result_row = cursor.fetchone()

        cnxn.close()

    print("   Re-opening Files for read-write...")
    # Reopen file - write to next version with mfr and model data
    with open(in_file, "r", encoding="utf-8", newline='') as data_in:
        with open(out_file, "w", encoding="utf-8", newline='') as data_out:
            csv_in = csv.reader(data_in)
            csv_out = csv.writer(data_out)
            header = next(csv_in)
            csv_out.writerow(out_hdrs)

            # Build next version of csv file.
            if len(plane_models.keys()) > 0:
                for row in csv_in:
                    code = row[pos["icao24"]].upper()
                    new_row = row[:3]  # Up to callsign
                    if code in plane_models:
                        new_row += plane_models[code]
                    else:
                        new_row += ["NA", "NA"]
                    new_row += row[3:]
                    csv_out.writerow(new_row)

print("COMPLETED")
