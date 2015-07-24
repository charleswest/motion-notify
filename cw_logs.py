#!/usr/bin/python2.7
'''
provide logging services -- see main for invocation
'''
import sys
import logging.handlers, traceback
import ConfigParser
global logger
def logit(cfg_path):
    config = ConfigParser.ConfigParser()
    config.read(cfg_path)
    logfile  = config.get( 'log', 'logfile' )

    
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
    logger.info('Log file initialized to '+ logfile) 
    return(logger)
if  __name__ == '__main__':
    print ' log module regression Test'
    cfg_path = ' '
    if sys.platform == 'win32':
        cfg_path = 'motion-notify.cfg'
        print 'windows' , cfg_path
    else:    
        cfg_path = sys.argv[1]            # notify.cfg
    logger = logit(cfg_path)
    logger.info("logger regression test-info") #  try other options if needed
