#!/bin/bash

# ssh-multi
# D.Kovalov
# Based on http://linuxpixies.blogspot.jp/2011/06/tmux-copy-mode-and-how-to-control.html

# a script to ssh multiple servers over multiple tmux panes

usage() {
    echo 'ssh-multi.sh : [OPTION]'
    echo '   -u user                           : user use for ssh connection'
    echo '   -d "serv0 serv1 serv2 ... servN"  : list serv to connect to'
    echo
    echo '   Bonus:'
    echo '   -d "$(echo 'serv'{0..3})" <-> -d "serv0 serv1 serv2 serv3"'
    echo '   -d "$(anotherscript)" to call a script that give you a list of host"'
    exit 0
}

starttmux() {

    if [ -z "$HOSTS" ]; then
           echo -n "Please provide of list of hosts separated by spaces [ENTER]: "
           read HOSTS
    fi

    local hosts=( $HOSTS )
    local target="ssh-multi ${host[0]}"
    
    tmux new-window -n "${target}" ssh $user@${hosts[0]}
    unset hosts[0];
    
    for i in "${hosts[@]}"
    do

        tmux split-window -t :"${target}" -h "ssh $user@$i"
        tmux select-layout -t :"${target}" tiled > /dev/null
	
    done
    tmux select-pane -t 0
    tmux set-window-option -t :"${target}"  synchronize-panes on > /dev/null
}

user=$USER
HOSTS=''

while getopts "u:d:h" o; do
        case "${o}" in
	    h)
		usage
		;;
	    u)
                user=${OPTARG}
                ;;
            d)
                HOSTS=${OPTARG}
                ;;
	    # p)
	    #	PROTOCOL=${OPTARG}
        esac
done

if [ ! -z "$TMUX" ]
then
    starttmux
else
    echo 'ssh-multi.sh : Must be run inside a tmux session !'
fi
