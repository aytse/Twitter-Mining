__author__ = 'Adam'
import datetime
import parse
import re

# STATIC VARIABLES
# Regular expression template that follows the
# structure of a HTML tag
TAG_RE = re.compile(r'<[^>]+>')

# Calculates the average from a list of numbers
# and rounds the number to the first 2 decimal
# points
def calculate_average(number_list):
    # Initial check if list is empty
    if not number_list:
        return 0

    # Sum initialization
    sum = 0

    # Calculates sum of all the numbers
    for element in number_list.values():
        sum += element

    # Returns the rounded average by dividing
    # number by number of integers in list
    return "{0:.2f}".format(float(sum)/len(number_list))

# Function that removes all Non ASCII and all
# content that is following a HTML format using
# regular expressions
def clean_text(string):
    # Removes all Non ASCII characters in string
    breakString = re.sub(r'[^\x00-\x7F]', '', string)

    # Removes all strings that follow a similar HTML format
    return TAG_RE.sub('', breakString)

# Adds times by a minute and returns the new time
def minute_offset(time):
    timestamp = datetime.datetime(time.year, time.month, time.day, time.hour, time.minute, time.second)
    timestamp = timestamp - datetime.timedelta(seconds=60)
    return timestamp

# Takes line delimited JSON file and creates a
# JSON out of it
def to_json_array(input_json):
    # Creates the input text file
    input_file = open(input_json, 'r')

    # Read the input file and creates and JSON Array from the input
    my_list = input_file.readlines()
    json_input = parse.parse_by_line(my_list)

    input_file.close()
    return json_input
