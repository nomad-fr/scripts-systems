#!/bin/bash

# check-not-vc.sh : a script to check a that everything in a Version Control
#                   folder is under Version Control
# nomad-fr : 28.04.2016

usage() {
    echo $1
    echo $0' "repository folder path"'
    exit 0
}

check-svn() {
    echo 'Untracked files:'
    svn status $(svn info $path | head -2 | tail -1 | awk -F':' '{print $2}') | grep ^\?
}

check-git() {
    git status
}

check-vc() {
    svn info $path &>/dev/null
    if [ "$?" = 0 ]
    then
	check-svn
    else
	cd $path
	git log &>/dev/null
	if [ "$?" = 0 ]
	then
	    check-git
	else
	    usage "$path : is not a repository folder path"
	fi
    fi
}

if [ "$#" -ne 1 ]; then usage; fi
path=$1

check-vc
