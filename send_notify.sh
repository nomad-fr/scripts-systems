#!/bin/bash

# send_notify.sh : a script to notify user with notify-send 
# nomad-fr : https://github.com/nomad-fr/scripts-systems

EXPIRE_TIME=30000 # in millisecond : 30000ms = 30s
ICON=/usr/share/icons/elementary-xfce/status/128/info.png
NOTIFY_SEND_BIN="/usr/bin/notify-send -t $EXPIRE_TIME -i $ICON"
title='Title of message'
message='message test'
user=$USER

usage()
{
    if [ ! -z $1 ]; then echo $1; fi
    echo $0' : [OPTION]'
    echo '   -u user'
    echo '   -t title'
    echo '   -m message'
    exit 0
}

notify() # send notify
{
    if [ "$USER" = 'root' ]; then
	DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION su -c "$NOTIFY_SEND_BIN \"$title\" \"$message\"" $user
    fi

    if [ "$USER" = "$user" ]; then
	DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION $($NOTIFY_SEND_BIN "$title" "$message")
    fi
}

find_user_dbuss_address()
{
    # process to determine DBUS_SESSION_BUS_ADDRESS
    USER_DBUS_PROCESS_NAME="gconfd-2"
    # get pid of user dbus process
    DBUS_PID=`ps ax | grep $USER_DBUS_PROCESS_NAME | grep -v grep | awk '{ print $1 }' | head -n 1`
    # get DBUS_SESSION_BUS_ADDRESS variable
    DBUS_SESSION=`grep -z DBUS_SESSION_BUS_ADDRESS /proc/$DBUS_PID/environ | sed -e s/DBUS_SESSION_BUS_ADDRESS=//`
}

while getopts "u:m:t:h" o; do
    case "${o}" in
	h)
	    usage
	    ;;
	u)
	    user=${OPTARG}
	    ;;
	m)
	    message=${OPTARG}
	    ;;
	t)
	    title=${OPTARG}
	    ;;
    esac
done

find_user_dbuss_address
notify

