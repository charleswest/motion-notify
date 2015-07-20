#!/usr/bin/python2.7
'''
This is a wrapper that passes ARGS to MotionNotify
Created on 17 July 2015
@author: Charles West
'''
import os.path
import sys
from cw_logs import logit,logger
global logger
from cw_notify import MotionNotify
if __name__ == '__main__':
    logger.info("Motion Notify script started")
    if len(sys.argv) < 2:
        logger.info('no config-file-path')
        exit('''Motion Notify - sends email 
                when network presence indicates nobody is home\n
                Usage: notfy.py {config-file-path}
                ''')
    cfg_path = sys.argv[1]
if not os.path.exists(cfg_path):
    exit('Config file does not exist [%s]' % cfg_path)
    
##    cfg_path = "C:\\Users\\charles\\Data\\cwtest\\motion\\notify\\motion-notify.cfg"
    # motion-notify.cfg on Git   this will require config                
    MotionNotify(cfg_path,True) 
    print('Start event triggered')
    logger.info('Motion Notify done\n')
