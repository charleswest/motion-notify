#!/usr/bin/python2
'''
module to determine if anybody is home based on lists of IP and mac addresses in Config
Created on 17 July 2015
@author: Charles West
'''
#from datetime import datetime
#import os.path
import sys,re
import subprocess, time
import ConfigParser
from cw_logs import logit,logger
from cw_anybody_home_arp import anybody_home_arp 
global logger
def anybody_home(config_file_path):
     '''
     Simple approach is just to or the results.  If mac lst is present they
     may provide better confirmation.
     '''
     global logger

     config = ConfigParser.ConfigParser()
     config.read(config_file_path)
     logger.info("Config file read")
     
     presenceMacs = []
     network = []

     ip_addresses = []

     try:
        presenceMacs = config.get( 'LAN', 'presence_macs' ).lower().split(', ')
        net  = config.get( 'LAN', 'network' )
        x,y = net.split(',')
        x = int(x); y = int(y)
        network = [x,y]
     except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
        pass

     try:
        ip_addresses = config.get( 'LAN', 'ip_addresses' ).split(', ')
     except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
        pass
     logger.info("anybody home has  config options set")
     print 'ip     ',ip_addresses
     print 'macs   ',presenceMacs
     print 'network', network
     
     
     return( anybody_home_arp(network,presenceMacs) or anybody_home_ip(ip_addresses))  

def anybody_home_ip(ip_addresses):
    '''module returns true if any one of a list of ip addresses can be pinged
       uses sys.platform to make it work on both windows and linux
    '''
    global logger
    if not ip_addresses:
        logger.info("No IP addresses configured - skipping IP check")
        return False
    logger.info("Checking for presence via IP address")
    addresses = ip_addresses 
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
       
  #      for line in results:
        inactive = str(results).find('nreachable')
        print '\ninactive', inactive ,  results
        if not (inactive >0) :
            logger.info( 'Active IP address  someobody home  ' + str(address))
            return True
        
        
        
    logger.info( 'IP inactive - nobody is home ' )
    return False     #  anybody home  - nope

if  __name__ == '__main__':
     
    print ' active module regression Test'
    cfg_path = sys.argv[1]   # motion-notify on Git                  
    print  [anybody_home(cfg_path) , 'parms from config']
    
##    print  [anybody_home_ip(['192.168.1.127']), 'False - system 127 should fail']
##    print  [anybody_home_ip([]),              'False no ips in list\n\n']
     
 #   ips = '192.168.1.106, 192.168.1.119, 192.168.1.114'.split(', ')
 #   print  [anybody_home_ip(ips),'True - one good addr 114']
    
