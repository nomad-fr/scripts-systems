#!/bin/bash

# send_notify.sh : a script to notify user with notify-send 
# nomad-fr : https://github.com/nomad-fr/scripts-systems

usage() {
    if [ ! -z $1 ]; then echo $1; fi
    echo $0' : [OPTION]'
    echo '   -u user'
    echo '   -t title'
    echo '   -m message'
    echo '   -i icon     : to disable icon : none or a wrong path' 
    exit 0 }

notify() {
    export DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION
    export DISPLAY=:0
    $(sudo -u $user $NOTIFY_SEND_BIN "$title" "$message") }

find_user_dbuss_address() {
    # get pid of user dbus process
    DBUS_PID=`ps ax | grep $USER_DBUS_PROCESS_NAME | grep -v grep | /usr/bin/awk '{ print $1 }' | head -n 1`
    # get DBUS_SESSION_BUS_ADDRESS variable
    DBUS_SESSION=`grep -z DBUS_SESSION_BUS_ADDRESS /proc/$DBUS_PID/environ | sed -e s/DBUS_SESSION_BUS_ADDRESS=//`
}

checkopt() {
    if [ -z "$icon" ]; then icon=/usr/share/icons/elementary-xfce/status/128/info.png; fi
    if [ -z "$title" ]; then title='Title of message'; fi
    if [ -z "$message" ]; then message='message test'; fi
    if [ -z "$user" ]; then user=$USER; fi }

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

USER_DBUS_PROCESS_NAME="gconfd-2"     # process to determine DBUS_SESSION_BUS_ADDRESS
EXPIRE_TIME=30000 # in millisecond : 30000ms = 30s
NOTIFY_SEND_BIN="/usr/bin/notify-send -t $EXPIRE_TIME -i "$icon

checkopt
find_user_dbuss_address
notify

