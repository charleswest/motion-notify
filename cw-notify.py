#!/usr/bin/python2
'''
Created on 17 July 2015

@author: Charles West 

Motion Notify v0.2 - no longer uploads images and video to Google Drive.
Sends notification via email using my isp -  this needs a config entry.

and or maybe Dropbox in future.


- - - - - - - - - -----------------------------------------------------------
Detects whether someone is home by checking the local network for an IP address or MAC address and only sends email if nobody is home.
Allows hours to be defined when the system will be active regardless of network presence.

Sends an email to the user at that start of an event and uploads images throughout the event.
At the end of an event the video is uploaded to Google Drive and a link is emailed to the user.
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
from cw_logs import logit,logger
global logger
from cw_anybody_home import anybody_home

logger.info("Motion Notify script started")     
cfg_path = "C:\\Users\\charles\\Data\\cwtest\\motion\\notify\\motion-notify.cfg"   # motion-notify on Git                  
notify = True  

class MotionNotify:
    
    def __init__(self, config_file_path):
        global logger
        logger.info("Loading config")
        # Load config
        config = ConfigParser.ConfigParser()
        config.read(config_file_path)
        logger.info("Config file read")
        # mail account credentials
        self.username = config.get('mail', 'user')
        self.password = config.get('mail', 'password')
        self.from_name = config.get('mail', 'name')
        self.sender = config.get('mail', 'sender')
        print 'config read'
        # Recipient email address (could be same as from_addr)
        self.recipient = config.get('mail', 'recipient')

        # Subject line for email
        self.subject = config.get('mail', 'subject')

        # First line of email message
        self.message = config.get('mail', 'message')

        # Folder (or collection) in Docs where you want the media to go
        self.folder = config.get('docs', 'folder')

        # Options
        self.delete_files = config.getboolean('options', 'delete-files')
        self.send_email = config.getboolean('options', 'send-email')
        self.event_started_message = config.get('mail', 'event_started_message')
        
        self.presenceMacs = []
        self.network = None
        
        self.ip_addresses = None
        
        try:
            self.presenceMacs = config.get( 'LAN', 'presence_macs' ).split( ',' )
            self.network = config.get( 'LAN', 'network' )
        except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
            pass
        
        try:
            self.ip_addresses = config.get( 'LAN', 'ip_addresses' )
        except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
            pass
        
        try:
            self.forceOnStart = config.getint( 'activate-system', 'force_on_start' )
            self.forceOnEnd = config.getint( 'activate-system', 'force_on_end' )
        except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
            pass
        
        logger.info("All config options set")
        
    def _send_email(self,msg):
        '''Send an email using the SMTP server account.'''
        senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
        m="Date: %s\r\nFrom: %s <%s>\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (senddate, self.from_name, self.sender, self.recipient, self.subject)
        print self.username, self.sender, self.password
        server = smtplib.SMTP('smtp.westrc.com:2525')
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, self.recipient, m+msg)
        server.quit()    
    
    def _system_active(self):
        global logger
        now = datetime.now()
        system_active = True
        # Ignore presence if force_on specified
        if self.forceOnStart and self.forceOnEnd and \
            now.hour >= self.forceOnStart and now.hour < self.forceOnEnd:
            logger.info( 'System is forced active at the current time - ignoring network presence' )
            return True
        else:
            if self.ip_addresses :
                system_active = not anybody_home(self.ip_addresses)
            else :
                if self.network and self.presenceMacs:
                    system_active = self._system_active_arp_based()
            logger.info( 'Based on network presence should the email be sent %s', system_active )
        return system_active
    
    def _email_required(self, notify):
        logger.info('Checking if email required')
        if not self.send_email or not notify :
            logger.info( 'Either email is disabled globally or is disabled for this task via command line parameters' )
            return False
        logger.info( 'Email required for this task')
        return True

    def _system_active_arp_based(self):
        if not self.network or not self.presenceMacs:
            return None
        logger.info("Checking for presence via MAC address")
        result = subprocess.Popen( [ 'sudo', 'arp-scan', self.network ], stdout=subprocess.PIPE,stderr=subprocess.STDOUT ).stdout.readlines()
        logger.info("result %s", result)
        for addr in result:
            for i in self.presenceMacs:
                if i.lower() in addr.lower():
                    logger.info( 'ARP entry found - someone is home' )
                    return False
        logger.info( 'No ARP entry found - nobody is home - system is active' )
        return True
    
    
    

    def send_start_event_email(self, notify) :
        """Send an email showing that the event has started"""
        if self._email_required(notify) and self._system_active() :
            msg = self.event_started_message
       #     msg += '\n\n' + self.google_drive_folder_link
            self._send_email(msg)


if __name__ == '__main__':
      
    if not os.path.exists(cfg_path):
        print('Config file does not exist [%s]' % cfg_path)
    
    MotionNotify(cfg_path).send_start_event_email(notify)
    print('Start event triggered')
    logger.info('main cw-notify done')



