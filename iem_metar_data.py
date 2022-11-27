import json
import time
import datetime
import sys

"""
Example script that scrapes data from the IEM ASOS download service
https://github.com/akrherz/iem/blob/main/scripts/asos/iem_scraper_example.py

This script accesses the IEM ASOS download service to gather METAR data
for specific airports and dates.

Modified by Mark Kuether
"""


# Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen
except ImportError:
    print("Not gonna happen.")
    sys.exit()

# Number of attempts to download data
MAX_ATTEMPTS = 2
# HTTPS here can be problematic for installs that don't have Lets Encrypt CA
SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"


def download_data(uri):
    """Fetch the data from the IEM
    The IEM download service has some protections in place to keep the number
    of inbound requests in check.  This function implements an exponential
    backoff to keep individual downloads from erroring.
    Args:
      uri (string): URL to fetch
    Returns:
      string data
    """
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            data = urlopen(uri, timeout=300).read().decode("utf-8")
            if data is not None and not data.startswith("ERROR"):
                return data
        except Exception as exp:
            print("download_data(%s) failed with %s" % (uri, exp))
            time.sleep(5)
        attempt += 1

    print("Exhausted attempts to download, returning empty data")
    return ""


def get_stations_from_filelist(filename):
    """Build a listing of stations from a simple file listing the stations.
    The file should simply have one station per line - MK.
    """
    stations = []
    for line in open(filename):
        stations.append(line.strip())
    return stations


def get_stations_from_networks():
    """Build a station list by using a bunch of IEM networks.
    ### This function was not used for this project - MK ###
    """
    stations = []
    states = """AK AL AR AZ CA CO CT DE FL GA HI IA ID IL IN KS KY LA MA MD ME
     MI MN MO MS MT NC ND NE NH NJ NM NV NY OH OK OR PA RI SC SD TN TX UT VA VT
     WA WI WV WY"""
    networks = []
    for state in states.split():
        networks.append("%s_ASOS" % (state,))

    for network in networks:
        # Get metadata
        uri = (
            "https://mesonet.agron.iastate.edu/geojson/network/%s.geojson"
        ) % (network,)
        data = urlopen(uri)
        jdict = json.load(data)
        for site in jdict["features"]:
            stations.append(site["properties"]["sid"])
    return stations


def download_alldata():
    """An alternative method that fetches all available data.
    Service supports up to 24 hours worth of data at a time.
    ### This function was not used for this project - MK ###"""
    # timestamps in UTC to request data for
    startts = datetime.datetime(2012, 8, 1)
    endts = datetime.datetime(2012, 9, 1)
    interval = datetime.timedelta(hours=24)

    service = SERVICE + "data=all&tz=Etc/UTC&format=comma&latlon=yes&"

    now = startts
    while now < endts:
        thisurl = service
        thisurl += now.strftime("year1=%Y&month1=%m&day1=%d&")
        thisurl += (now + interval).strftime("year2=%Y&month2=%m&day2=%d&")
        print("Downloading: %s" % (now,))
        data = download_data(thisurl)
        outfn = "%s.txt" % (now.strftime("%Y%m%d"),)
        with open(outfn, "w") as fh:
            fh.write(data)
        now += interval


def write_header(filepath: str, header: str):
    # Written by MK
    # Writes a header at the top of a csv file.

    outfile = open(filepath, "a", encoding="utf-8")
    outfile.write(header)
    outfile.close()

    return True


def check_data(data: str, station: str, header: str):
    # Written by MK.
    # Checks to see if no data was returned. If no data
    # was returned, it indicates this so those stations
    # lacking weather data are easy to find and identify.
    if len(data) == len(header):
        data = f"{station},0000-00-00 00:00,No Data\n"
    else:
        new_line = "\n"
        eol_pos = data.index(new_line)
        data = data[eol_pos+1:]
    return data


def get_time_place(full_file: str):
    # Written by MK
    # Extracts specific dates and airport id's from
    # the accident CSV file created using SQL scripts.
    # Returns a list of 2-tuple records of date and id.
    all_records = []
    date_field = "ev_date"
    airport_field = "ev_nr_apt_id"
    with open(full_file, "r", encoding="utf-8-sig") as raw:
        line = raw.readline()
        headers = line.split(",")
        header_pos = {header: pos for pos, header in enumerate(headers)}
        d_pos = header_pos[date_field]
        a_pos = header_pos[airport_field]
        line = raw.readline()

        while line:
            fields = line.split(",")
            this_record = (fields[d_pos], fields[a_pos])
            all_records.append(this_record)
            line = raw.readline()

    return all_records


def main():
    """Our main method
    This method modified from downloaded script
    to fit the specific goals of this project - MK"""

    # Set initial paths andfile names
    in_root = "C:/Users/Mark/Documents/"
    in_root += "By_Subject/Data Science Masters/"
    in_root += "DS785/Code_Scripts/Input_Data/"
    input_name = "LANDING ACCIDENT DATA WITH N NUMBERS.csv"
    input_file = in_root + input_name

    out_root = "C:/Users/Mark/Documents/By_Subject/"
    out_root += "Data Science Masters/DS785/Code_Scripts/Output_data/"
    output_name = "all_weather_data.txt"
    output_file = out_root + output_name
    header = "station,valid,metar\n"

    # Get all records from the input CSV file.
    all_records = get_time_place(input_file)
    date_fld = 0
    place_fld = 1

    # Create a single header for the entire file.
    mybool = write_header(output_file, header)

    for record in all_records:
        ev_date_str = record[date_fld]
        ev_date_parts = ev_date_str.split("/")
        day_part = int(ev_date_parts[1])
        month_part = int(ev_date_parts[0])
        year_part = int(ev_date_parts[2])
        ap_id = record[place_fld]
        ev_date = datetime.datetime(
            year=year_part, month=month_part, day=day_part)

        # timestamps in UTC to request data for
        startts = ev_date
        endts = ev_date+datetime.timedelta(days=1)

        # URL copied from request made using web page UI and parsed in code
        # https://mesonet.agron.iastate.edu/request/download.phtml?network=WI_ASOS

        service = SERVICE
        startstring = startts.strftime("year1=%Y&month1=%m&day1=%d&")
        endstring = endts.strftime("year2=%Y&month2=%m&day2=%d&")

        service += f"station={ap_id}&"
        service += "data=metar&"
        service += startstring
        service += endstring
        service += "tz=Etc" + chr(37) + "2FUTC&"
        service += "&format=onlycomma&latlon=no&elev=no"
        service += "&missing=M&trace=T&direct=no"

        uri = service
        print("Downloading: %s" % (ap_id,))
        data = download_data(uri)
        data = check_data(data, ap_id, header)

        out = open(output_file, "a")
        out.write(data)
        out.close()


if __name__ == "__main__":
    # download_alldata()
    main()
