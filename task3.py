import re
import os
import numpy as np
from random import randrange
from tzlocal import get_localzone
import time
import random
import datetime

REGEX = r'([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (\d+)'

def parseApachelog(line):
    """
    watch each log line for slow requests
    """
    match = re.search(REGEX, line)
    if match is None:
        print("Warning: log line is not parsed!!!")
        return 
    return int(match.group(8))

def generateLog():
    """
    To simulate apache logs
    """
    f = open('generatedapache.log','w')
    local = get_localzone()
    otime = datetime.datetime.now()
    resp = "200"
    meth = "GET"
    ip = "136.159.240.75"
    byt = "32"
    uri = "http://www.telegraph.co.uk/sport/rugbyunion/"
    referer = "https://telegraph.co.uk"
    useragent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1;Trident/4.0; InfoPath.1; InfoPath.2; .NET CLR 2.0.50727;.NET CLR 3.0.04506.648;.NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
    line = 0
    while (line < 100):
        dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
        tz = datetime.datetime.now(local).strftime('%z')
        resp_time = random.randint(50, 10000)
        f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s" %s\n' % (ip,dt,tz,meth,uri,resp,byt,referer,useragent,resp_time))
        line += 1

def statsOfApacheLog(response_times):
    """
    Compute stats of apache log
    """
    avg_res_times = sum(response_times) // len(response_times)
    min_res_time = min(response_times)
    max_res_time = max(response_times)
    print('Average response time {}ms'.format(avg_res_times))
    print('Minimum response time is {}ms'.format(min_res_time))
    print('Maximum response time is {}ms'.format(max_res_time))

def getApacheLogfile(path):
    """
    Read apache log file
    """
    with open(os.path.join(path, "generatedapache.log"), "r") as fid:
        lines = [l.strip() for l in fid.readlines()]
    all_response_times = []
    for line in lines:
        response_time = parseApachelog(line)
        all_response_times.append(response_time)
    statsOfApacheLog(all_response_times)

if __name__ == "__main__":
    path = os.getcwd()
    generateLog()
    getApacheLogfile(path)