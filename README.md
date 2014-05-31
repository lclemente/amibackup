AMIBACKUP  
Author: Luigi Clemente  
Email: luigi@luigiclemente.com   
=========
Python script to automate AMI backup of AWS EC2 instances.  
The script will create an AMI backup image of each server in the config file, no reboot.  
For each server will deregister all images (and relative snapshots) older than the threshold set in the config file.  
Access to AWS accounts will use access key and secret, as set in the Boto config file profiles.  

Requirements
------

Python 2.7 (version I used, it might work on others)  
AWS SDK for Python: Boto (http://aws.amazon.com/sdkforpython/)  

Install
------
Install Python and Boto  
Configure boto.config credentials to access your AWS accounts (see boto_config.sample)  
Clone amibackup git repository to a local folder  
Copy and rename ami_backup_config.py.sample to ami_backup_config.py  
Edit the ami_backup_config.py file  
Set up a cron task to run the script ami_backup.py  


