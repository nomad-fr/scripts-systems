#!/bin/bash

# synergy-relaunch.sh : a scrtip to relaunch synergy
# clients & servers base on synergy config file

# note : you must use the same user on each hosts

## CONFIG
SYNERGY_CONFIG_FILE=~/config/synergy/synergy_ipgp.conf
## CONFIG

## get current IP from where I launch synergys
## if more than one IP take first one
SYNERGYS_IP=$(ip a | grep 'state UP' -A2 | grep inet | awk -F' ' '{print substr($2, 1, length($2)-3)}' | head -n1)
## you can also set it up like this
#SYNERGYS_IP=192.168.0.1

## get client list from synergy config file
CLIENTS=$(grep :$ $SYNERGY_CONFIG_FILE | awk -F':' '{sub(/ +/,"",$1); sub(/\t+/,"",$1); print}' | sort | uniq)

## get pid of running synergy*
SYNERGY_PIDS=$(ps aux | grep synergy | grep -v grep | grep -v $(basename $0) | awk -F ' ' '{print $2}')

for p in $SYNERGY_PIDS
do kill -9 "$p"; done
synergys -d ERROR -c ~/config/synergy/synergy_ipgp.conf

for c in $CLIENTS
do
    echo -n $c' : '
    ssh -o ConnectTimeout=2 $c echo ok 2>&1
    if [ $? -eq 0 ]
    then
	for p in $(ssh $c "ps aux | grep synergy | grep -v grep" | awk -F' ' '{print $2}')
	do ssh $c "kill -9 $p"; done
	ssh $c "synergyc $SYNERGYS_IP"
    fi
done
