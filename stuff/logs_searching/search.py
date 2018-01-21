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

#To alert admin when attack is detected
def beep():
    print '\a'
 

#Check if an IP address is brute forcing 
ips=[]
def checkbrute(ip):
    ips.append(ip)    
    if ips.count(ip)>50:
        while ip in ips:
            ips.remove(ip)
        return 1
    else:
        return 0

if len(ips)>1000:
    ips=[]

def main():

    logfile = open('/var/log/apache2/access.log','r')
    loglines = follow(logfile)

    for line in loglines:
        try:
            query = get_query(line)
            sqli = checksqli(query)
            if sqli:
                print termcolor.colored('SQL INJECTION ATTEMPT'.center(50,'*'),'green')
                print 'Details :\nFrom : '+get_ip(line)+'\nQuery : '+urllib.unquote(query)
                print termcolor.colored(''.center(50,'*')+'\n','green')
                beep()
            brute = checkbrute(get_ip(line))
            if brute:
                print termcolor.colored('BRUTE FORCE ATTEMPT'.center(50,'*'),'red')
                print 'Details :\nFrom : '+get_ip(line)+'\nCheck logs for more info.'
                print termcolor.colored(''.center(50,'*')+'\n','red')
                beep()

        except:
            pass


if __name__ == '__main__':
    main()
