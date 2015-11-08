__author__ = 'Adam'
import datetime
import email.utils
import json

# Returns a list of all unique hashtags
def parse_hashtag(string):
    matches = [word for word in string.split() if word.startswith("#")]
    return [hashtag.lower() for hashtag in list(set(matches))]

# Read JSON by line and creates a JSONArray using lines
def parse_by_line(json_lines):
    json_array = []
    for json_line in json_lines:
        json_array.append(json.loads(json_line))
    return json_array

# Returns the value of a JSON using tag as a parameter
# Necessary because it compensates for JSON Obejcts without
# an associated tag
def parse_json(json_object, tag):
    if tag in json_object:
        text = json_object[tag]
    else:
        text = 'NULL'
    return text

# Parses twitter timestamps into Python readable format
def parse_timestamps(twitter_time):
    time_tuple = email.utils.parsedate_tz(twitter_time.strip())
    python_time = datetime.datetime(*time_tuple[:6])
    return python_time - datetime.timedelta(seconds=time_tuple[-1])