#!/usr/bin/python2.7  
'''
This is a wrapper that passes ARGS to MotionNotify
Created on 20 July 2015
@author: Charles West
'''
import os.path
import sys
from cw_logs import logit,logger
global logger
from cw_notify import MotionNotify
if __name__ == '__main__':

    if sys.platform == 'win32':
        cwcfg = r'/Users/charles/data/cwtest/motion/notify/motion-notify.cfg'
        print cwcfg
        sys.argv = ['notify.py', cwcfg, 1]
        
    if len(sys.argv) < 2:
        logger.info('no config-file-path')
        print('''Motion Notify - sends email 
                when network presence indicates nobody is home\n
                Usage: notfy.py {config-file-path[,forceMail]}
                ''')
    cfg_path = sys.argv[1]
    forceMail = False
    if len(sys.argv) == 3:
        forceMail = sys.argv[2]     # optional last parm force send mail 
    print 'cfg path', cfg_path
if not os.path.exists(cfg_path):
    logger.info ('Config file does not exist [%s]' % cfg_path)
 
MotionNotify(cfg_path,forceMail)   #   use True to force an email 
print('Start event triggered')
logger.info('Motion Notify done\n')
