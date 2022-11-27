import os

'''
This reads lines from OPENSKY_QUERIES.TXT.
It prints the item and query on the screen, then
prompts the user to press enter.  

This allows me to copy the query and paste it
into a putty ssh session to the OPENSKY network.

After the data is received, and the putty session
is closed, pressing Enter will rename the log file
from putty.log to the specific airplane-aiport-date descriptor.

The script then prompts the next item.
'''
in_dir = "C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Input_Data/"
in_name = "OPENSKY_QUERIES.txt"
in_file = in_dir + in_name

raw_dir = "d:/input/"
first_name = "putty.log"
first_file = raw_dir + first_name

airplane_part = 0
airport_part = 1
date_part = 2

with open(in_file, "r", encoding="utf-8") as events:
    line = events.readline().strip()
    while line:
        if line[:1] == "N":  # AIRPLANE - AIRPORT - DATE
            fields = line.split("_")
            fields = fields[:3]
            new_name = "_".join(fields)
            new_name += "_raw.txt"

            line = events.readline().strip()
            sql_request = line
            print(f"{new_name}:")
            print(f"{sql_request}\n\n")
            ready = input("Login and submit query. Press Enter when ready.")

            second_file = raw_dir + new_name
            os.rename(first_file, second_file)

        line = events.readline().strip()  # blank line
        line = events.readline().strip()  # airplane line
