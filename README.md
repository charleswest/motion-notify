motion-notify
=============

Motion Notify is a notification system for Linux Motion that sends  email notificaiton when you're not home.
This carries out the following:

-Sends an email when motion detection event starts

-Detects whether you're at home by looking for certain mac addresses on your local network and doesn't send alerts if you're home
-Allows you to specify hours when you want to receive alerts even if you're at home

On a ubuntu system the arp command runs as a regular user.  Mac addresses provide a much more conistent means of identification in the presence of DHCP the ip returned from the arp is used to verify that the device is live. 

Specify either a comma separated list of MAC addresses. 

Note that mobile phones often don't retain a constant connection to the wireless network even though they show that they are connected. They will be shown as dhcp clients of the router but will not have a mac in the arp cache of the motion server unless they have connected to it.  Looking at the video feed on the 192.168 subnet is sufficient.

Installation
There's no automated installation yet so this is the current process  --  

Create a directory:       #    this may not be best practice for linux -- 
mkdir notify              #   this will be in your home directory 
cd to notify
git clone https://github.com/charleswest/motion-notify.git

Create the log file and set the permissions
sudo touch /var/tmp/notify.log

sudo chown motion.motion /var/tmp/notify.log
sudo chmod 664 /var/tmp/notify.log

Edit the config file and enter the following:

-Email address to send alerts to
- Server and port for your smtp mail server  -   smtp.yourdomain.com    

-The hours that you always want to recieve email alerts even when you're home
-Either enter MAC addresses which will be active when you're at home

Change the permissions
sudo chown motion.motion notify/notify.py
sudo chown motion.motion notify/notify.cfg
sudo chmod 744 motion.motion notify/notify.py
sudo chmod 600 motion.motion notify/notify.cfg

Create the entry in the Motion conf file to trigger the motion-notify script when there is an alert
This is easily done from the motion control panel using your browser.  
typical entry will be
/home/you/notify/notify.py /home/you/notify.cfg Force  --   force is a binary that will force send mail if True


Motion will now send alerts to you when you're devices aren't present on the network
