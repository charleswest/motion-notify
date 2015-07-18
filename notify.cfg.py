#  Since config parser cant find the section gmail just make this std python and include it 
#[gmail]
# GMail account credentials
mail = {
    name  :     'Your Name',
    user :    'youremail@gmail.com',
    password : 'yourpassword',
    sender :  'youremail@gmail.com'
}
### Recipient email address (could be same as from_addr)
##recipient = 'youremail@provider.com'
##
### Subject line for email
##subject = 'Motion detected'
##
### First line of email message
##message = 'Video uploaded'
##event_started_message ='An event has been detected and is being captured. '
###[docs]
### Folder (or collection) in Docs where you want the videos to go
##folder = 'CCTV'
##
###[options]
### Delete the local video file after the upload
##delete-files = 1
##
### Send an email after the upload
##send-email = 1
##
###[activate-system]
### Force on between these hours, i.e, ignore presence info
##force_on_start = 1
##force_on_end = 7
##
###[LAN]
### Network to monitor (used by MAC address detection)
##network = '192.168.1.0:255.255.255.0'
##
### MAC addresses (comma separated) of the devices to detect home presence and disable emails (e.g., phones) - these will be ignored if you specify IP addresses below
##presence_macs = 'XX:XX:XX:XX:XX,YY:YY:YY:YY:YY'
##
###Space separated list of IP addresses for detection. If these are present on the network the system is inactive. Setup a static IP on your router to keep your IP constant
###The MAC address above will be ignored if you configure an IP here 
##ip_addresses = '192.168.1.100,192.168.1.101,192.168.3.102'

