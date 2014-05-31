#!/usr/bin/python
# Filename: ami_backup_config.py

# example of config file
# time in minutes AMI images will be kept for
backup_retention =  10080 #7 days
# file to save the script logs
logfile = "path-to-log-file"
# servers to be backed up
servers = [
    dict(
        name = "Server one", #server description
        profile = "profile_one", #account authentication profile name as set in the boto config file
        region = "eu-west-1", #ec2 server region
        pattern = "server_name_tag_one" #name tag of the server to backup
    ),
    dict(
        name = "Server two",
        profile = "profile_two",
        region = "eu-west-1",
        pattern = "server_name_tag_two"
    )
]