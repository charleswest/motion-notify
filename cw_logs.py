'''
provide logging services -- see main for invocation
'''

import sys
import logging.handlers, traceback
global db
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
    print ' log module regression Test'
    logfile = 'notify.log'                     # '/var/tmp/motion-notify.log',
    logger = logit(logfile)                    # contructor 
    logger.info("logger regression test-info") #  try other options if needed
