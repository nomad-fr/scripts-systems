#!/usr/bin/env bash

######################################
# backup-laptop-sismo.sh
# For : This script rsync a SRC folder to a DST
#       then launch a remote snapshot on DST
# Usage: ./backup-laptop-sismo.sh
# Author: Michel Le Cocq <lecocq@ipgp.fr>
# Update: 23.10.2017
######################################

###################################
## USER ENV SETTING TO be ADJUST ##
###################################
    
# source dir to backup ~ is users home
SRC=~

# backup key to use
CLEF=~/.ssh/id_rsa_backup-gobt

# destination volume
VOL=houyo

# list of exluded files
EXCLUDE_FILE="/home/nomad/bin/exclude-backup-laptop"   
# EXCLUDE_FILE : Specifies a FILE that contains exclude patterns (one per line).
#                Blank lines in the file and lines starting with ';' or '#' are ignored.

# install autofs
# add this to /etc/auto.master
# /media/backup-Sismo                         /etc/auto.backup --ghost,--timeout=60
# add this to /etc/auto.backup
# Backup-houyo	 -fstype=nfs,ro,intr    192.168.0.7:/snob/backup/laptop/houyo

BACKUP_FOLDER=/media/gobt/Backup-houyo

###################################
##    NOTHING TO CHANGE BELOW    ##
###################################

US=marty
HOST=192.168.0.7
PORT=22
USHOST=$US@$HOST
DST=$USHOST:/snob/backup/laptop

if [ ! -e $EXCLUDE_FILE ]
then EXCLUDE_FILE=""
fi

help()
{
    printf 'rsync command shoud be like :\n'
    printf 'rsync -av -e "ssh -i "$CLEF --delete $SRC $DST/$VOL --exclude-from=$EXCLUDE_FILE --delete-excluded\n'
}

ping -c 1 $HOST -W1 > /dev/null
testping=$?

if [ $testping -eq 0 ]
then
    printf quit | telnet $HOST $PORT 2>/dev/null | grep Connected > /dev/null
    testssh=$?
    if [ $testssh -eq 0 ]
    then
	if [ $# -eq 1 ]
	then
	    if [ "$1" = "last" ]
	    then
		ssh -i $CLEF $USHOST '/home/marty/getlastsnap.sh '$VOL
		exit 0
	    elif [ "$1" = "host" ]
	    then
		 printf $HOST'\n'
		 exit 0
	    elif [ "$1" = "backup_folder" ]
	    then
		printf $BACKUP_FOLDER'\n'
		exit 0

	    else
		exit 1				
	    fi
	fi
	run=$(ps -fe -o ppid -o cmd | grep $USHOST | grep -v grep | awk '{print $1}')
	if [ -z "$run" ]
	then
	    rsync -av --rsync-path="sudo rsync" -e "ssh -p $PORT -i "$CLEF --delete $SRC $DST/$VOL --exclude-from=$EXCLUDE_FILE --delete-excluded
	    if [ $? -eq 0 ]; then
		printf '\n['$0'] : rsync done now snapshot it\n'
		ssh -p $PORT -i $CLEF $USHOST "/home/marty/snap-vol.sh $VOL";
		printf 'snapshost Done :  backup finish\n'
	    else
		printf '\n['$0'] : rsync trouble no snapshot\n';
		/home/nomad/bin/send_notify.sh -t 'backup NeuronFarm' -m 'rsync trouble : no snapshot'
		help;
	    fi
	else
	    printf 'backup script already running : pid %s\n' $run
	    exit 1
	fi
    fi
else
    printf $HOST' not accessible\n';
    exit 1
fi
