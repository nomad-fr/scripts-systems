#!/bin/bash                                                                                                                                                                                                                                 
# ssh-multi                                                                                                                                                                                                                                 
# D.Kovalov                                                                                                                                                                                                                                 
# Based on http://linuxpixies.blogspot.jp/2011/06/tmux-copy-mode-and-how-to-control.html                                                                                                                                                    

# a script to ssh multiple servers over multiple tmux panes                                                                                                                                                                                 

testssh() {
    echo quit | telnet $1 22 2>/dev/null | grep Connected
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
        tmux split-window -t :"${target}" -h  "ssh $user@$i"
        tmux select-layout -t :"${target}" tiled > /dev/null
    done
    tmux select-pane -t 0
    tmux set-window-option -t :"${target}"  synchronize-panes on > /dev/null
}

user=$USER
HOSTS=''

while getopts "u:h:" o; do
        case "${o}" in
            u)
                user=${OPTARG}
                ;;
            h)
                HOSTS=${OPTARG}
                ;;
        esac
done

if [ ! -z "$TMUX" ]
then
    starttmux
else
    echo 'Must be run in a tmux session !'
fi
