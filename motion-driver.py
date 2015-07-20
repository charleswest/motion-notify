
import os.path
from cw_logs import logit,logger
global logger
#from cw_anybody_home import anybody_home
from cw_notify import MotionNotify
if __name__ == '__main__':
    logger.info("Motion Notify script started")     
    cfg_path = "C:\\Users\\charles\\Data\\cwtest\\motion\\notify\\motion-notify.cfg"   # motion-notify on Git                  
    notify = True    
    if not os.path.exists(cfg_path):
        print('Config file does not exist [%s]' % cfg_path)
    
    MotionNotify(cfg_path,notify) 
    print('Start event triggered')
    logger.info('main cw-notify done\n\n')
