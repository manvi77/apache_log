import re
import os
import numpy as np

REGEX = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (\d+) (\S.*)'


def parseApachelog(line):
    """
    watch each log line for slow requests
    """
    match = re.search(REGEX, line)
    if match is None:
        print("Warning: log line is not parsed!!!")
        return 
    return int(match.group(8))
    
def statsOfApacheLog(response_times):
    """
    Compute stats of apache log using numpy
    """
    response_times = np.asarray(response_times)
    avg_res_times = int(np.mean(response_times))
    slow_100ms = sum(response_times > 100)
    slow_500ms = sum(response_times > 500)
    slow_1000ms = sum(response_times > 1000)
    print('Average response time {}ms'.format(avg_res_times))
    print('Number of responses slower than 100ms are {}'.format(slow_100ms))
    print('Number of responses slower than 500ms are {}'.format(slow_500ms))
    print('Number of responses slower than 1000ms are {}'.format(slow_1000ms))

    
def getApacheLogfile(path):
    """
    Read apache log file
    """
    with open(os.path.join(path, "apache.log"), "r") as fid:
        lines = [l.strip() for l in fid.readlines()]
        #print(lines)
    # check only last 10000 lines
    lines = lines[-10000:]
    all_response_times = []
    for line in lines:
        response_time = parseApachelog(line)
        all_response_times.append(response_time)
    statsOfApacheLog(all_response_times)



if __name__ == "__main__":
    path = os.getcwd()
    getApacheLogfile(path)
