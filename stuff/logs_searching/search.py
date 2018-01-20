#!/usr/bin/python -tt

import urllib
import time 
import re
import termcolor

#To read the file while it is getting updated
def follow(logfile):
    logfile.seek(0,2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

#Search for sqli pattern in the URL
def checksqli(line):
    match=re.search('%27|"|sleep%28|benchmark%28|%3B|--|%23|%2F|%5C',line) 
    """
        URL encoding
        %27 '
        %28 (
        %3B ;
        %23 #
        %2F /
        %5C \
    """
    try:
        return match.group()
    except :
        return 0

#Get the attacker's ip address
def get_ip(line):
    match=re.search('\d+.\d+.\d+.\d+',line)
    try:
        return match.group()
    except:
        return 0

#Get the query used for sqli
def get_query(line):
    match=re.search('email=.+1\.1',line)
    try:
        return match.group()[:match.group().find('HTTP')] #query - unnecessary
    except:
        return 0

def main():

    logfile = open('/var/log/apache2/access.log','r')
    loglines = follow(logfile)
    for line in loglines:
        try:
            query = get_query(line)
            sqli=checksqli(query)
            print query
            if sqli:
                print termcolor.colored('SQL INJECTION ATTEMPT'.center(50,'*'),'green')
                print 'Details :\nFrom : '+get_ip(line)+'\nQuery : '+urllib.unquote(query)
                print termcolor.colored(''.center(50,'*')+'\n','green')
                print "\a"
        except:
            pass


if __name__ == '__main__':
    main()
