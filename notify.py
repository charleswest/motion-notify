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
    logger.info("Motion Notify script started")
    if len(sys.argv) < 2:
        logger.info('no config-file-path')
        print('''Motion Notify - sends email 
                when network presence indicates nobody is home\n
                Usage: notfy.py {config-file-path}
                ''')
    cfg_path = sys.argv[1]
    print 'cfg path', cfg_path
if not os.path.exists(cfg_path):
    logger.info ('Config file does not exist [%s]' % cfg_path)
    


    # motion-notify.cfg on Git   this will require config                

MotionNotify(cfg_path,True) 
print('Start event triggered')
logger.info('Motion Notify done\n')
