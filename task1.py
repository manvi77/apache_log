import re
import os

REGEX = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (\d+) (\S.*)'


def parseApachelog(line):
    """
    watch each log line for slow requests
    """
    match = re.search(REGEX, line)
    if match is None:
        print("Warning: log line is not parsed!!!")
        return 
    host_name = match.group(1)
    time_stamp = match.group(2)
    response_time = int(match.group(8))
    if response_time > 1000:
        print("Response time of host {} accessed at [{}] is longer than 1 second ({})"
        .format(host_name, time_stamp, response_time))

def getApacheLogfile(path):
    """
    Read apache log file
    """
    with open(os.path.join(path, "apache.log"), "r") as fid:
        lines = [l.strip() for l in fid.readlines()]
        #print(lines)
    for line in lines:
        parseApachelog(line)

if __name__ == "__main__":
    path = os.getcwd()
    getApacheLogfile(path)
