#!/usr/bin/python2.7
'''
provide logging services -- see main for invocation
'''

import sys
import logging.handlers, traceback
print sys.platform
   
def logit(logfile):
    logger = logging.getLogger( 'MotionNotify' )
    hdlr = logging.handlers.RotatingFileHandler(logfile,
                                 maxBytes=1048576,
                                 backupCount=3 )
    formatter = logging.Formatter( '%(asctime)s %(levelname)s %(message)s' )
    hdlr.setFormatter( formatter )
    logger.addHandler( hdlr ) 
    logger.setLevel( logging.INFO )

    def loggerExceptHook( t, v, tb ):
        logger.error( traceback.format_exception( t, v, tb ) )

    sys.excepthook = loggerExceptHook

    return(logger)

if  __name__ == '__main__':

    if sys.platform == 'win32':
        logfile= 'notify.log'
    else:
        logfile = '/var/tmp/notify.log'
    print ' log module regression Test'
                 # contructor 
    logger = logit(logfile)
    logger.info("logger regression test-info") #  try other options if needed
