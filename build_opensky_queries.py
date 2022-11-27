from datetime import datetime, timedelta

'''
Reads in the date, latitude, longitude, and elevation
details from the airport box files.

Converts date into a range of dates
Builds a SQL based query to query the 
OpenSky network data.

Writes the queryies to a text file.
'''

'''
SAMPLE QUERY:
select time,icao24,callsign,
lat,lon,velocity,heading,vertrate,
baroaltitude,geoaltitude,lastposupdate,lastcontact 
from state_vectors_data4 
where hour = 1633111200 
and lat >= 40.2026 
and lat <= 40.2766 
and lon >= -75.6047 
and lon <= -75.5087 
and geoaltitude < 703.5 
limit 200;
'''


def build_desc(fields: list, pos: dict):
    # Extracts field values and builds
    # a description line for each query
    # Reformats date
    # Outputs string with new line.

    date_parts = []
    date_val = fields[pos["ev_date"]]
    ev_dt = datetime.strptime(date_val, "%m/%d/%Y")
    date_parts.append(f"{ev_dt.year}")
    date_parts.append(f"{ev_dt.month:02d}")
    date_parts.append(f"{ev_dt.day:02d}")
    date_str = "-".join(date_parts)

    desc = fields[pos["N_Number"]]
    desc += f"_{fields[pos['LocId']]}"
    desc += f"_{date_str}"
    desc += f"_{fields[pos['Latitude']]}"
    desc += f"_{fields[pos['Longitude']]}"
    desc += "\n"

    return desc


def build_query(fields: list, pos: dict):

    # Build SQL Query
    select_txt = "select time, icao24, callsign,"
    select_txt += " lat, lon, velocity, heading, vertrate,"
    select_txt += " baroaltitude, geoaltitude,"
    select_txt += " lastposupdate, lastcontact"

    from_txt = "from state_vectors_data4"

    # Extract elements from fields
    ev_date = fields[pos["ev_date"]]
    low_lat = fields[pos["low_lat"]]
    high_lat = fields[pos["high_lat"]]
    low_lon = fields[pos["low_lon"]]
    high_lon = fields[pos["high_lon"]]
    top = fields[pos["top(m)"]]

    # Convert date to hour range
    # All Traffic from date 00:00Z to date+1 08:00Z
    # Total of 24+8 = 32 hours of traffic to ensure
    # we capture the accident aircraft data.
    date_start = datetime.strptime(ev_date, '%m/%d/%Y')
    next_day = timedelta(hours=32)
    date_end = date_start + next_day
    epoch_start = int(date_start.timestamp())
    epoch_end = int(date_end.timestamp())
    hour_start = epoch_start - (epoch_start % 3600)
    hour_end = epoch_end - (epoch_end % 3600)

    where_txt = f"where "
    where_txt += f"lat >= {low_lat} "
    where_txt += f"and lat <= {high_lat} "
    where_txt += f"and lon >= {low_lon} "
    where_txt += f"and lon <= {high_lon} "
    where_txt += f"and geoaltitude <= {top} "
    where_txt += f"and time >= {epoch_start} "
    where_txt += f"and time <= {epoch_end} "
    where_txt += f"and hour >= {hour_start} "
    where_txt += f"and hour <= {hour_end}"

    query_parts = [select_txt, from_txt, where_txt]
    full_query = " ".join(query_parts)

    return full_query

#############
# MAIN CODE #
#############


in_root = "C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Input_Data/"
in_name = "AIRPORT_BOX_DATE_DATA.csv"
in_file = in_root + in_name
out_root = "C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Output_data/"
out_name = "OPENSKY_QUERIES.TXT"
out_file = out_root + out_name

with open(in_file, "r", encoding="utf-8-sig") as inputfile:
    with open(out_file, "w", encoding="utf-8") as outputfile:
        line = inputfile.readline().strip()
        line = line.replace(chr(34), "")
        fields = line.split(",")
        pos = {hdr: index for index, hdr in enumerate(fields)}

        line = inputfile.readline().strip()
        while line:
            line = line.replace(chr(34), "")
            fields = line.split(",")
            desc = build_desc(fields, pos)

            outputfile.write(desc)

            query_string = build_query(fields, pos)
            query_string += ";\n\n"
            outputfile.write(query_string)

            line = inputfile.readline().strip()
