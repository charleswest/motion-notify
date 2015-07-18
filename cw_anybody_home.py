#!/usr/bin/python2
'''
module to determine if system is active
Created on 17 July 2015
@author: Charles West
 

'''
#from datetime import datetime
#import os.path
import sys,re
import subprocess, time
#import ConfigParser
from cw_logs import logit
def anybody_home_ip(ip_addresses):
    '''module returns true if any one of a list of ip addresses can be pinged
       uses sys.platform to make it work on both windows and linux
    '''
    if not ip_addresses:
        logger.info("No IP addresses configured - skipping IP check")
        return False
    logger.info("Checking for presence via IP address")
    addresses = ip_addresses.split(',')
    print addresses
    for address in addresses :   #  if any  ips are discovered return TRUE
        results = ' '
        print 'trying address>' ,address,'<'
        if sys.platform == 'win32':
            ptuple = ['ping',  address ]    #    '-c1' needs admin on windows
        else:
            ptuple = ['ping', '-c1', address]  #   ok on linux
            
        results = subprocess.Popen( ptuple,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT
                                    ).stdout.readlines()
        for line in results:
            #print line
            if 'time' in line:
                logger.info( 'Active address  somebody home' + str(address))
                return True

        
    logger.info( 'IP inactive - nobody is home ' )
    return False     #  anybody home  - nope

if  __name__ == '__main__':
    print ' active module regression Test'
    logfile = 'notify.log'                     # '/var/tmp/motion-notify.log',
    logger = logit(logfile)
    logger.info('Test for Anybody_home')
##    print  [anybody_home_ip('192.168.1.127'), 'False - system 127 should fail']
##    print  [anybody_home_ip(''),              'False no ips in list\n\n']
##    print  [anybody_home_ip('192.168.1.110'), 'True system 110 should be active\n\n'] 
##    print  [anybody_home_ip('192.168.1.127,192.168.1.128,192.168.1.129'), 'False - bad list\n\n']
    print  [anybody_home_ip('192.168.1.106,192.168.1.119,192.168.1.110'), 'True - one good addr 110']
    
