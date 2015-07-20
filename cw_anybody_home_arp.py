#!/usr/bin/python2
'''
module to determine if system is active based on the arp cache
Created on 17 July 2015
@author: Charles West
since the server will only cache a mac address for clients that
talk to it we need to look at the local client table on the router 
for the expected ip range and the mac of  anyone connected
config needs to specify the range eg 192.168.1,100-120
then we need to ping the range and last we arp for macs that
we know belong to portable devices.
'''
#from datetime import datetime
#import os.path
import sys,re,os
import subprocess, time
#import ConfigParser
from cw_logs import logit,logger
global logger
def anybody_home(ipa):
     global logger
     return(anybody_home_ip(ipa) )   #  later add or mac


def anybody_home_arp(network,presenceMacs):
     '''
     first ping the network to prime the arp cache
     next  check if any network address has an arp we like
     for the moment we shall only allow 192.168.1.x to 192.168.1.y
     so network is a tuple [x,y]   presenceMacs are a list of macs
     x1:x2:x2:x4:x5:x6,y1:y2:y3:y4:y5:y6  etc  see main for real
     examples   fC:c2:de:55:d8:ec   good arp  00:03:4f:08:a1:29  dsc
     note -- lowcase hex 
     '''
     if not network or not presenceMacs:
          return False
     logger.info("Checkingfor presence via MAC address")
     x = network[0]; y = network[1]
     print 'ping start', x , 'ping end',y

##               ptuple = ['ping', '-c1', address]  #  ok on linux
##               
##          subprocess.Popen( ptuple)     
##          time.sleep(.1)
     if sys.platform == 'win32':
          for adr in range (x,y):
               address = '192.168.1.'+str(adr)
               lines = os.popen('ping -n 1 '+address)
               time.sleep(.1)
          
          lines = os.popen('arp -a')                    
          for i,lr in enumerate(lines):
               a = lr.split()
               if len(a) == 3 and a[2] == 'dynamic':
                    mac = a[1].replace('-',':')         # parse win32 arp output
                    #print mac
                    if mac in presenceMacs:
                         logger.info('Found a mobile mac somebody is home rtn True')
                         return True                    #  we found a mac in our list 
               
     else:
          logger.info("sys.platform == 'linux':")
  #        for adr in range (x,y):
  #             address = '192.168.1.'+str(adr)
  #             lines = os.popen('ping -c1 '+address)
  #             time.sleep(.1)
          
          linefil = os.popen('arp -a')
          lines = linefil.read() 
          #print ' arp output ' , lines 
          lines = lines.split('\n')              
          for i,lr in enumerate(lines):
               #print i,lr
               a = lr.split()
               #print a[4], len(a)
               if len(a) == 7 and a[4] == '[ether]':
                    mac = a[3] # linux  arp output
                    #print mac
                    if mac in presenceMacs:
                         logger.info('Found a mobile mac somebody is home rtn True')
                         return True                    #  we found a mac in our list 
     logger.info('nobody found - return False')
     return False

if  __name__ == '__main__':
##    print ' arp anybody home  Test'
    print [anybody_home_arp([100,114],['00:25:9c:53:01:2a','00:03:4f:08:a1:29','fc:x2:de:55:d8:ec']), 'True ']
    print [anybody_home_arp([100,114],['00:95:9z:53:01:2z']), 'False no such arp']

##    print  [anybody_home('192.168.1.114') , 'True  - anybody home DSC']    
