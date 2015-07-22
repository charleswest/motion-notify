motion-notify
=============

Motion Notify is a notification system for Linux Motion that sends  email notificaiton when you're not home.
This carries out the following:

-Sends an email when motion detection event starts

-Sends an email when the event ends with a link to the video
-Detects whether you're at home by looking for certain mac addresses on your local network and doesn't send alerts if you're home
-Allows you to specify hours when you want to receive alerts even if you're at home

On a ubuntu system the arp command runs perfectly well as a regular user.  Mac addresses provide a much 
more conistent means of identification in the presence of DHCP.  We do need a ping scan to prime the arp cache.

IP detection uses ping so will run as a regular user.
Specify either a comma separated list of IP addresses or a comma separated list of MAC addresses. 

Note that mobile phones often don't retain a constant connection to the wireless network even though they show that they are connected. They tend to sleep but they wake up if you ping them.
It's highly recommended not to configure your devices to use static IP's since mac addresses do not  change.

Installation
There's no automated installation yet so this is the current process

Install Python Libraries
sudo apt-get update
sudo apt-get install python-pip
sudo pip install -U gdata

Create a directory:
sudo mkdir /etc/motion-notify

Copy motion-notify.cfg, motion-notify.py and create-motion-conf-entries.txt to the directory you created

Create the log file and set the permissions
sudo touch /var/tmp/motion-notify.log
sudo chown motion.motion /var/tmp/motion-notify.log
sudo chmod 664 /var/tmp/motion-notify.log


Edit the config file and enter the following:

-Email address to send alerts to

-The hours that you always want to recieve email alerts even when you're home
-Either enter IP addresses or MAC addresses (avoid using MAC addresses) which will be active when you're at home

Change the permissions
sudo chown motion.motion /etc/motion-notify/motion-notify.py
sudo chown motion.motion /etc/motion-notify/motion-notify.cfg
sudo chmod 744 motion.motion /etc/motion-notify/motion-notify.py
sudo chmod 600 motion.motion /etc/motion-notify/motion-notify.cfg

Create the entry in the Motion conf file to trigger the motion-notify script when there is an alert
sudo cat /etc/motion-notify/create-motion-conf-entries.txt >> /etc/motion/motion.conf
rm /etc/motion-notify/create-motion-conf-entries.txt


Motion will now send alerts to you when you're devices aren't present on the network
