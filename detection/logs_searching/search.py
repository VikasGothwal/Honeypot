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

#To clear the IPs list after 1000
if len(ips)>1000:
    ips=[]

def checkxss(line):
    match=re.search('%3Cscript',line) #%3C - <
    try:
        return match.group()
    except:
        return 0

def get_link(line):
    match=re.search('/project/.+HTTP',line)
    try:
        return ('http://192.168.110.135'+match.group())[:-5]
    except:
        return 0

def status(link):
    op=urllib.urlopen(link)
    return op.code


def main():

    logfile = open('/var/log/apache2/access.log','r')
    loglines = follow(logfile)

    for line in loglines:
        try:
            query = get_query(line)
            sqli = checksqli(query) 
            brute = checkbrute(get_ip(line))
            xss = checkxss(query)

            if xss:
                print termcolor.colored('XSS ATTEMPT'.center(50,'*'),'yellow')
                print termcolor.colored('Details :\nFrom : '+get_ip(line)+'\nCode : '+urllib.unquote(query),'yellow')
                print termcolor.colored(''.center(50,'*')+'\n','yellow')
                beep()

            if sqli:
                print termcolor.colored('SQL INJECTION ATTEMPT'.center(50,'*'),'white')
                print termcolor.colored('Details :\nFrom : '+get_ip(line)+'\nQuery : '+urllib.unquote(query),'white')
                print termcolor.colored(''.center(50,'*')+'\n','white')
                beep()

                link=get_link(line)
                code=status(link)
                #if code==200:
                #    print 'Success'
            
            if brute:
                print termcolor.colored('BRUTE FORCE ATTEMPT'.center(50,'*'),'green')
                print termcolor.colored('Details :\nFrom : '+get_ip(line)+'\nCheck logs for more info.','green')
                print termcolor.colored(''.center(50,'*')+'\n','green')
                beep()


        except:
            pass


if __name__ == '__main__':
    main()
