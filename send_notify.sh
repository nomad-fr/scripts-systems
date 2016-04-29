#!/bin/bash

# send_notify.sh : a script to notify user with notify-send 
# nomad-fr : https://github.com/nomad-fr/scripts-systems

usage()
{
    if [ ! -z $1 ]; then echo $1; fi
    echo $0' : [OPTION]'
    echo '   -u user'
    echo '   -t title'
    echo '   -m message'
    echo '   -i icon     : to disable icon : none ' 
    exit 0
}

notify() # send notify
{
    export DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION
    
    if [ "$USER" = 'root' ]; then
	su -c "$NOTIFY_SEND_BIN \"$title\" \"$message\"" $user
    fi
    if [ "$USER" = "$user" ]; then
	$(sudo -u $user $NOTIFY_SEND_BIN "$title" "$message")
    fi
}

find_user_dbuss_address()
{
    # process to determine DBUS_SESSION_BUS_ADDRESS
    USER_DBUS_PROCESS_NAME="gconfd-2"
    # get pid of user dbus process
    DBUS_PID=`ps ax | grep $USER_DBUS_PROCESS_NAME | grep -v grep | /usr/bin/awk '{ print $1 }' | head -n 1`
    # get DBUS_SESSION_BUS_ADDRESS variable
    DBUS_SESSION=`grep -z DBUS_SESSION_BUS_ADDRESS /proc/$DBUS_PID/environ | sed -e s/DBUS_SESSION_BUS_ADDRESS=//`
}

while getopts "u:m:t:hi:" o; do
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
	i)
	    icon=${OPTARG}
	    ;;
    esac    
done

EXPIRE_TIME=30000 # in millisecond : 30000ms = 30s
if [ -z "$icon" ]; then icon=/usr/share/icons/elementary-xfce/status/128/info.png; fi
NOTIFY_SEND_BIN="/usr/bin/notify-send -t $EXPIRE_TIME -i "$icon
if [ -z "$title" ]; then title='Title of message'; fi
if [ -z "$message" ]; then message='message test'; fi
if [ -z "$user" ]; then user=$USER; fi

find_user_dbuss_address
notify

