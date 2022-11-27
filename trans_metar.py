'''
trans_metar.py
Reads a CSV file with station, GMT time stamp, and raw metar data
Extracts winds speed, direction, altimeter settings from metar
Writes CSV with startion, timestamp, wind speed, wind dir,
 wind dir var, gust spd, and altimeter setting.

This is be combined with ADS-B data to estimate air speed.
'''

import re


def parse_weather(metar: str):
    # reads a single metar.
    # Breaks out wind speed, gust, dir
    # and alt settings using reg ex.
    # Returns list of setttings
    # [wind dir, wind dir var, wind spd, wind gust, alt]
    #airport_re = "K\w{3}"
    #time_re = "\d{6}Z"
    winds_re = "\w{5}KT"
    wind_gust_re = "\w{5}G\d\dKT"
    wind_variance_re = "\d{3}V\d{3}"
    altimeter_re = "A\d{4}"

    #airport_id = "(Airport not found)"
    #time_val = "(Time not found)"
    winds = ""
    wind_speed = ""
    wind_dir = ""
    variance = ""
    gust = "0"
    altimeter = ""

    #airport_found = re.search(airport_re, metar)
    #time_found = re.search(time_re, metar)
    winds_found = re.search(winds_re, metar)
    gust_found = re.search(wind_gust_re, metar)
    variance_found = re.search(wind_variance_re, metar)
    altimeter_found = re.search(altimeter_re, metar)

    # if airport_found:
    #    airport_id = airport_found.group()
    # if time_found:
    #    time_val = time_found.group()
    if winds_found:
        # Winds pattern = #####KT or VRB##KT
        winds = winds_found.group()
        if "/////" in winds:  # Special case for this data set.
            pass
        else:
            wind_dir = winds[:3]
            if wind_dir == "vrb":
                wind_dir = "000"
            wind_speed = winds[3:5]

    if gust_found:
        # Wind Gust Pattern = #####G##KT or VRB##G##KT
        winds = gust_found.group()
        wind_dir = winds[:3]
        if wind_dir == "vrb":
            wind_dir = "000"
        wind_speed = winds[3:5]
        gust = winds[6:8]

    if variance_found:
        variance = variance_found.group()
    if altimeter_found:
        altimeter = altimeter_found.group()

    report = []
    report.append(wind_dir)
    report.append(variance)
    report.append(wind_speed)
    report.append(gust)
    report.append(altimeter)

    return report


airport_field = 0
date_field = 1
metar_field = 2
re_string1 = "^K[A-Z]{3} \\d{6}Z \\w+KT"
re_string2 = "^K[A-Z]{3} \\d{6}Z AUTO \\w+KT"

root = "C:/Users/Mark/Documents/By_Subject/"
root += "Data Science Masters/DS785/Code_Scripts/"
in_path = root + "Input_Data/"
out_path = root + "Output_data/"

input_name = "all_weather_data_raw.txt"
output_name = "all_weather_data_comp.csv"

input_file = in_path + input_name
output_file = out_path + output_name

out_headers = "airport,date,wind_dir,wind_var,wind_spd,wind_gust,altimeter"
out_headers += "\n"

data_in = open(input_file, "r", encoding="utf-8")
data_out = open(output_file, "w", encoding="utf-8")
data_out.write(out_headers)

headerline = data_in.readline()
line = data_in.readline()
has_data = True
while line:
    in_data = line.split(",")
    no_data = ("")
    out_data = []
    out_data.append(in_data[airport_field])
    out_data.append(in_data[date_field])
    metar_report = parse_weather(in_data[metar_field])
    out_data += metar_report
    out_line = ",".join(out_data)
    out_line += "\n"
    if has_data:
        data_out.write(out_line)
    line = data_in.readline()
    has_data = ("No Data" not in line)

data_out.close()
data_in.close()
