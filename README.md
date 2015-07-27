motion-notify
=============

Motion Notify is a notification system for Linux Motion that sends  email notificaiton when you're not home.
This carries out the following:

-Sends an email when motion detection event starts

-Detects whether you're at home by looking for certain mac addresses on your local network and doesn't send alerts if you're home
-Allows you to specify hours when you want to receive alerts even if you're at home

On a ubuntu system the arp command runs as a regular user but apparently it needs sudo on Debian.  Fortunately the command ' ip n show'  will display the arp cache on either system without sudo.  Mac addresses provide a much more conistent means of identification in the presence of DHCP.  The ip returned from the arp cache is used to verify that the device is live if the ip n show status returns anything other than REACHABLE.  

Specify a comma separated list of MAC addresses. 

Note that mobile phones often don't retain a constant connection to the motion server even though they show that they are connected. They will be shown as dhcp clients of the router but will not have a mac in the arp cache of the motion server unless they have connected to it.  Looking at the video feed or using motion control on the 192.168 subnet is sufficient to let notify know you are at home.

Installation
There's no automated installation yet so this is the current process  --  

in your home directory run:

        git clone https://github.com/charleswest/motion-notify.git notify

   This will create a notify directory will all     permisions set up to run.
   You may need to run apt-get install git in order to have the clone work
   This will create a git repository with everything you could ever want to backup your changes
   
cd notify     to   change to your new directory

nano motion-notify.cfg     to edit  your name and pasword
     and your email server. 
     
-Email address to send alerts to
- Server and port for your smtp mail server  -   smtp.yourdomain.com    

-The hours that you always want to recieve email alerts even when you're home
-Enter MAC addresses that will be active when you're at home
   
you should now be able to run each of the scripts from the command line

./cw_logs.py   ...   will create logger and write a test line

./notify.py  notify.cfg  1    will send mail if your cfg is ok

look in /var/tmp/notify.log   for problems

as soon as everything seems ok run:

git status       to see what you have changed 

git add          for everything you would like to keep    --  just notify.cfg for now

git commit -m 'working installation'

if you want to change things and don't want to lose what you already have working

git branch   will list branches   --- only master at this point

git branch  newstuff    --  will create a sandbox you can hack about in

git checkout newstuff   --   changes your working directory ie notify to the sandbox

      ***   this is a safe place to play
      
git checkout  master    --   changes back to your original working copy  **  be  careful

when newsstuff seems to work

git checkout master   -- to get the working code

git merge newstuff    -- will update master with your changes

git branch -d newstuff  will discard the sandbox

If all that is just too much

     rm -rf notify   --  will kill the whole shebang and you can start over fresh at git clone
  
Create the entry in the Motion conf file to trigger the motion-notify script when there is an alert
This is easily done from the motion control panel using your browser.  
typical entry will be

/home/you/notify/notify.py /home/you/notify.cfg Force  --   force is a binary that will force send mail if True

Motion will now send alerts to you when you're devices aren't present on the network

My recent clean install on Debian did not appear to require the following:
  I'll leave it here just  in case.

Change the permissions
sudo chown motion.motion notify/notify.py
sudo chown motion.motion notify/notify.cfg
sudo chmod 744 motion.motion notify/notify.py
sudo chmod 600 motion.motion notify/notify.cfg
