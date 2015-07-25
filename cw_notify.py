#!/usr/bin/python2.7
'''
Created on 17 July 2015

@author: Charles West 

Motion Notify v0.2 - no longer uploads images and video to Google Drive.
Sends notification via email using my isp -  this needs a config entry.

and or maybe Dropbox in future.


- - - - - - - - - -----------------------------------------------------------
Detects whether someone is home by checking the local network for an IP address or MAC address and only sends email if nobody is home.
Allows hours to be defined when the system will be active regardless of network presence.

Sends an email to the user at that start of an event 
Files are deleted once they are uploaded.

Based on the Google Drive uploader developed by
Jeremy Blythe (http://jeremyblythe.blogspot.com) and
pypymotion (https://github.com/7AC/pypymotion) by Wayne Dyck
and on Motion-Notify by  Andrew Dean
'''
# This file is part of Motion Notify.
#
# Motion Notify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Motion Notify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Motion Notify.  If not, see <http://www.gnu.org/licenses/>.

import smtplib
from datetime import datetime

import os.path
import sys
import subprocess, time
import ConfigParser
from cw_logs import logit 
#global logger
from cw_anybody_home import anybody_home
def MotionNotify(config_file_path,notify):
    config = ConfigParser.ConfigParser()
    config.read(config_file_path)
    logfile = config.get('log', 'logfile')
    logger = logit(logfile)
    logger.info("Config file read - log initialized ")
    # mail account credentials
    username = config.get('mail', 'user')
    password = config.get('mail', 'password')
    from_name = config.get('mail', 'name')
    sender = config.get('mail', 'sender')
    mailServ = config.get('mail','server')
    smtp =     config.get('mail', 'port')
    print 'config read'
    # Recipient email address (could be same as from_addr)
    recipient = config.get('mail', 'recipient')

    # Subject line for email
    subject = config.get('mail', 'subject')

    # First line of email message
    message = config.get('mail', 'message')

    # Folder (or collection) in Docs where you want the media to go
    folder = config.get('docs', 'folder')

    # Options
    delete_files = config.getboolean('options', 'delete-files')
    send_email = config.getboolean('options', 'send-email')
    event_started_message = config.get('mail', 'event_started_message')
    
    presenceMacs = []
    network = None
    
    ip_addresses = None
    

    
    try:
        forceOnStart = config.getint( 'activate-system', 'force_on_start' )
        forceOnEnd = config.getint( 'activate-system', 'force_on_end' )
    except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
        pass
    
    logger.info("All config options set")
        
    def send_email(msg):
        '''Send an email using the SMTP server account.'''
        senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
        m="Date: %s\r\nFrom: %s <%s>\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (senddate, from_name, sender, recipient, subject)
        print username, sender
 #       server = smtplib.SMTP('smtp.westrc.com:2525')
        logger.info( 'sending mail  via '+mailServ+':'+smtp)
        server = smtplib.SMTP(mailServ+':'+smtp)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, m+msg)
        server.quit()    
    
    def system_active():
 #       global logger
        now = datetime.now()
        # Ignore presence if force_on specified
        print now.hour , forceOnStart
        if forceOnStart and forceOnEnd and \
            now.hour >= forceOnStart and now.hour < forceOnEnd:
            logger.info( 'System is forced active at the current time - ignoring network presence' )
            return True
        
        else:
            active = not anybody_home(config_file_path,logger)            
            logger.info( 'Based on network presence should the email be sent %s', active )
            return active
    
    
##   Thats all she wrote ...     
    if  notify or system_active() :
        msg = event_started_message
        send_email(msg)
        logger.info('msg sent')
    else:
        logger.info('somebody home')


if __name__ == '__main__':
    if sys.platform == 'win32':
        cwcfg = r'/Users/charles/data/cwtest/motion/notify/motion-notify.cfg'
        print cwcfg
        sys.argv = ['cw_notify.py', cwcfg, 1]
        logger = logit('notify.log')
       
    cfg_path = sys.argv[1]   # motion-notify on Git
    notify = True    
    if not os.path.exists(cfg_path):
        print('Config file does not exist [%s]' % cfg_path)
    MotionNotify(cfg_path,notify) 
    logger.info('main cw-notify done\n')



