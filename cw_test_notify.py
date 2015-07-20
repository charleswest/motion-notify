#!/usr/bin/python2
''' this routine is used to ensure that all the sub modules are present and
accounted for
'''
from cw_logs import logit,logger
global logger
from cw_anybody_home import anybody_home
def maintest():
    
   logger.info( 'test harnesss started internal')
   print  [anybody_home('192.168.1.114') , 'True  - internal anybody home DSC'] 

if __name__ == '__main__':
    maintest()
    logger.info("Test harness script started main")
    print  [anybody_home('192.168.1.114') , 'True  - anybody home DSC']    

    print 'tst notify done'
