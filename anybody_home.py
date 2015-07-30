#!/usr/bin/python2
'''
module to determine if anybody is home based on lists of mac addresses in Config
Created on 17 July 2015
@author: Charles West
'''
#from datetime import datetime
#import os.path
import sys,re,os
import subprocess, time
import ConfigParser
from cw_logs import logit 
def anybody_home(config_file_path,logger):
     '''
     presenceMacs are a list of comma, space seperated macs
     x1:x2:x2:x4:x5:x6, y1:y2:y3:y4:y5:y6  etc  see main for real
     examples   fC:c2:de:55:d8:ec   good arp  00:03:4f:08:a1:29  dsc
     note -- lowcase hex
     If we find a mac in the arp cache we ping it to confirm presence of the device
     '''
     config = ConfigParser.ConfigParser()
     config.read(config_file_path)
     logger.info("Config file read")
     
     presenceMacs = []
     try:
        presenceMacs = config.get( 'LAN', 'presence_macs' ).lower().split(', ')
#        net  = config.get( 'LAN', 'network' )
#        x,y = net.split(',')
#        x = int(x); y = int(y)
#        network = [x,y]
     except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
        pass
     logger.info("anybody home has  config options set")
     
     #presenceMacs = 'FC:C2:DE:55:D8:EC, FC:C2:DE:C6:DC:76, F0:7B:CB:8A:A7:7A'.lower().split(', ') 
 
     print 'macs   ',presenceMacs
     if  not presenceMacs:
          return False

     logger.info("Checkingfor presence via MAC address")
     if sys.platform == 'win32':
          lines = os.popen('arp -a')                    
          for i,lr in enumerate(lines):
               a = lr.split()
               if len(a) == 3 and a[2] == 'dynamic':
                    mac = a[1].replace('-',':')         # parse win32 arp output
                    #print mac
                    if mac in presenceMacs:
                         logger.info('win Found a mobile mac somebody is home rtn True')
                         ipaddress = a[0]
                         return(anybody_home_ip(ipaddress,logger))
                                            #  we found a mac in our list
                                             #  ping it to see for sure 
               
     else:
          logger.info("sys.platform is " + sys.platform)
          print 'looking for ', presenceMacs
          linefil = os.popen('ip n show ')
          lines = linefil.read() 
         
          print ' arp cache output ' , lines 
          lines = lines.split('\n')              
          for i,lr in enumerate(lines):
               #print i,lr
               a = lr.split()
               #print a[4], len(a)
               if len(a) == 6 :
                    mac = a[4] # linux  ip show
                    logger.info(mac +' in arp cache') 
                    print mac , ' is mac from results' 
                    if mac in presenceMacs:
                         logger.info('Linus Found a mobile mac somebody is home rtn True')
                         ipaddress = a[0]
                         if a[5] == 'REACHABLE':
                             logger.info( 'found Reachable '+a[0])
                             return True
                         else:
                             return (anybody_home_ip(ipaddress,logger))   #  we found a mac in our list 
     logger.info('arp nobody found - return False')
     return False

def anybody_home_ip(address,logger):
    '''module returns true if an ip addresses can be pinged
       uses sys.platform to make it work on both windows and linux
    '''
    logger.info("Checking for presence via IP address")

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
    global logger
    if sys.platform == 'win32':
        cfg_path = 'motion-notify.cfg'
        print 'windows' , cfg_path
    else:    
        cfg_path = sys.argv[1]            # notify.cfg 
    print ' active module regression Test ArpFix'
    logger = logit(cfg_path)
    print  [anybody_home(cfg_path,logger) , 'parms from config']

    
