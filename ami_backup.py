#!/usr/bin/python
# AmiBackup
# Author: Luigi Clemente
# Version: 1.0

import boto.ec2
import datetime
import time
import sys
from time import mktime
import ami_backup_config #configuration file in same directory
import logging

logger = logging.getLogger('AMIBackup')
hdlr = logging.FileHandler(ami_backup_config.logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
signature = "_bkp_"


print "Backup started\n"
# read server info from config file
servers = ami_backup_config.servers
backup_retention = ami_backup_config.backup_retention

for server in servers :
    server_name = server['name']
    account_profile = server['profile']
    server_pattern = server['pattern']
    server_region = server['region']

    # create ec2 connection using boto config profiles
    ec2 = boto.ec2.connect_to_region(server_region, profile_name = account_profile)
    if ( ec2 is None  ):
        print "ERROR - " + server_name + ": unable to connect"
        logger.error( server_name + ": unable to connect to region " + server_region + " with profile " + account_profile )
        continue
    # filter instances by tag name
    reservations = ec2.get_all_reservations(filters = {'tag:Name':server_pattern, 'instance-state-name':'*'})
    if ( len(reservations) == 0 ):
        print "ERROR - " + server_name + ": unable to find server " + server_pattern
        logger.error( server_name + ": unable to find server " + server_pattern )
        continue
    # loop through reservations and instances
    for reservation in reservations:
        for instance in reservation.instances:
            #print instance.__dict__.keys()
            instance_name = instance.tags['Name']
            instance_id = instance.id
            print "\n" + server_name + ": " + instance_name + " (" + instance_id + ")"
            current_datetime = datetime.datetime.now()
            date_stamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
            ami_name = instance_name + signature + date_stamp
            try:
                ami_id = instance.create_image(ami_name, description='Created by AMIBackup', no_reboot=True, dry_run=False)
            except Exception, e:
                logger.error("Backup " + server_name + ": " + e.message)
                continue
            logger.info("Backup " + server_name + ": " + ami_name)
            print "AMI creation started"
            print "AMI name: " + ami_name
            images = ec2.get_all_images(image_ids = ami_id)
            image = images[0]
            image.add_tag("Name", ami_name)

            # deregister old images
            print "Deletion of old AMIs"
            images = ec2.get_all_images(filters = {'tag:Name':server_pattern + signature + '*'})
            for image in images:
                image_name = image.tags['Name']
                image_id = image.id
                image_stamp = image_name.replace(server_pattern + signature, "")
                image_timestamp = mktime(time.strptime(image_stamp, "%Y-%m-%d_%H-%M-%S"))
                current_timestamp = mktime(current_datetime.timetuple())
                diff_minutes = (current_timestamp - image_timestamp) / 60
                if ( diff_minutes > backup_retention ):
                    image.deregister(delete_snapshot=True, dry_run=False)
                    print image_name + " deleted"
                    logger.info("Deleted AMI " + image_name )
                else:
                    print image_name + " kept"
                    logger.info("Kept AMI " + image_name )
# end servers loop
print "\nBackup completed"

        

    
