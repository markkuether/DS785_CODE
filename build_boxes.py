import math
import copy
'''
Builds a geographical box in order to query 
OpenSky network for airtraffic within the boundaries.

Read in a CSV containing airport lat, lon, and elev.
Calculates an X mile box around the airport with
and elevation of 2000' above ground level.

Outputs a csv with original fiels and box details appended
Units are in feet.
'''


def get_dist(coord1: tuple, coord2: tuple):
    # Uses Haversine formulat to calcualte the distnace
    # between two geographic coordiantes in statute miles.
    # Obtained from:
    # https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    

    conv = 1609.23  # meters per mile
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    r = 6371e3  # approx radius of the earth in meters
    rad = math.pi/180

    phi1 = lat1*(rad)
    phi2 = lat2*(rad)
    dPhi = (lat2-lat1)*rad
    dLambda = (lon2-lon1)*rad
    sdp = math.sin(dPhi/2)
    sdl = math.sin(dLambda/2)
    cp1 = math.cos(phi1)
    cp2 = math.cos(phi2)
    a = sdp**2 + (cp1*cp2*sdl**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_meters = r*c
    d_miles = d_meters/conv

    return round(d_miles, 2)


def build_box(coord: tuple, elev: float, dist: float, height: float):
    # Defines lat, long, and elevation limits
    # Feeds an incrementing distance into haversigne
    # distiance formula until the distance is ~2.5 miles.
    # Returns coordinate limits and elevation of box.

    # incrimenting d.dd by delta provides a good step
    # for distance in miles.
    lat = 0
    lon = 1
    delta = .001
    lat_offset = 0
    lon_offset = 0
    elev_box_size = 0
    coord = (float(coord[lat]), float(coord[lon]))
    new_lat = coord[lat]
    new_lon = coord[lon]

    while lat_offset < dist:
        new_lat += delta
        c1 = coord
        c2 = (new_lat, coord[lon])
        lat_offset = get_dist(c1, c2)

    while lon_offset < dist:
        new_lon += delta
        c1 = coord
        c2 = (coord[lat], new_lon)
        lon_offset = get_dist(c1, c2)

    delta_lat = abs(coord[lat]-new_lat)
    delta_lon = abs(coord[lon]-new_lon)
    low_lat = round(coord[lat]-delta_lat, 4)
    up_lat = round(coord[lat]+delta_lat, 4)
    low_lon = round(coord[lon]-delta_lon, 4)
    up_lon = round(coord[lon]+delta_lon, 4)

    box = [low_lat, up_lat, low_lon, up_lon]
    box += [elev+height]

    return box


    #############
    # MAIN CODE #
    #############
height = 2000
dist = 3.0

in_root = "C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Input_Data/"
in_name = "LANDING_PLANE_APT_DATA.csv"
in_file = in_root + in_name
out_root = "C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Output_Data/"
out_name = "LANDING_PLANE_APT_BOX.csv"
out_file = out_root + out_name

with open(in_file, "r", encoding="utf-8-sig") as inputfile:
    with open(out_file, "w", encoding="utf-8") as outputfile:
        # Get headers from input file
        # prepare output file headers
        line = inputfile.readline().strip()
        line = line.replace(chr(34), "")
        input_headers = line.split(",")
        output_headers = copy.deepcopy(input_headers)
        output_headers += ["low_lat", "high_lat"]
        output_headers += ["low_lon", "high_lon"]
        output_headers += ["top"]

        out_hdr_line = ",".join(output_headers)
        out_hdr_line += "\n"
        outputfile.write(out_hdr_line)

        # Expected col_names (N_Number,LocId,Latitude,Longitude,Elevation)
        pos = {hdr: index for index, hdr in enumerate(input_headers)}

        # Get input data and build box
        line = inputfile.readline().strip()
        while line:
            line = line.replace(chr(34), "")
            fields = line.strip().split(",")
            lat_string = fields[pos["Latitude"]]
            lon_string = fields[pos["Longitude"]]
            elev_string = fields[pos["Elevation"]]

            lat = float(lat_string)
            lon = float(lon_string)
            elev = float(elev_string)

            box = build_box((lat, lon), elev, dist, height)
            low_lat = box[0]
            high_lat = box[1]
            low_lon = box[2]
            high_lon = box[3]
            top = box[4]
            top_m = round((top * .3048), 1)  # conv feet to meters

            fields += [str(low_lat), str(high_lat)]
            fields += [str(low_lon), str(high_lon)]
            fields += [str(top)]

            output_line = ",".join(fields)
            output_line += "\n"
            outputfile.write(output_line)

            line = inputfile.readline().strip()
