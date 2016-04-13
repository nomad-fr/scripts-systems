#!/bin/bash

# query-promox-vm.sh : a script to query all declared VM on a Proxmox cluster
# nomad-fr 

usage() {
    echo $1
    echo 'query-proxmox-vm.sh : [OPTION]'
    echo ' -d ProxmoxServer'
    echo ' -t type : qemu openvz : default all'
    echo ' -u up : seulement les machines up'
    exit 0
}

checkopt() {
    if [ -z "$serv" ]
    then usage "Please provide a host with -d option."
    else
	ssh root@$serv "pvecm status" > /dev/null
	if [ "$?" != 0 ]
	then usage "please give a Proxmox host"; fi
    fi
    if [ -z "$type" ]; then type=ALL
    else
	if [[ "$type" != "openvz" ]] && [[ "$type" != "qemu" ]]
	then usage 'type must be openvz or qemu'; fi
    fi
}

getvm() {
    if [[ $type = "openvz" ]] || [[ $type = "ALL" ]]
    then
	lsta=$(ssh root@$serv cat /etc/pve/nodes/*/openvz/*.conf | grep HOSTNAME | awk -F'.' '{print $1}' | awk -F'"' '{print $2}')
    fi
    if [[ $type = "qemu" ]] || [[ $type = "ALL" ]]
    then
	lstb=$(ssh root@$serv cat /etc/pve/nodes/*/qemu-server/*.conf | grep name | awk -F' ' '{print $2}')
    fi
}

showthem() {
	if [ "$up" = 1 ]
	then
	
	    for h in $(echo $lsta' '$lstb)
	    do
		nslookup $h > /dev/null
		if [ "$?" = 0 ]
		then
		    ping -W 1 -c 1 $h > /dev/null
		    if [ "$?" = 0 ]
		    then echo -n $h' '; fi
		fi
	    done
	else
	    for h in $(echo $lsta' '$lstb); do echo -n $h' '; done
	fi
	echo    
}

while getopts "hut:d:" o; do
        case "${o}" in
	    h)
		usage
		;;
	    t)
                type=${OPTARG}
                ;;
	    d)
                serv=${OPTARG}
                ;;
	    u)
		up=1
		;;
        esac
done

checkopt
getvm
showthem
