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
    e=$(svn status $(svn info $1 | head -2 | tail -1 | awk -F':' '{print $2}') | grep ^\?)
    if [ ! -z "$e" ]; then echo 'Untracked files in repo : '$1; echo $e; fi
}

check-git() {
    e=$(git ls-files . --exclude-standard --others)
    if [ ! -z "$e" ]; then echo 'Untracked files in repo : '$1; echo $e; fi
}

check-vc() {
    svn info $path &>/dev/null
    if [ "$?" = 0 ]
    then
	check-svn $path
    else
	cd $path
	git log &>/dev/null
	if [ "$?" = 0 ]
	then
	    check-git $path
	else
	    usage "$path : is not a repository folder path"
	fi
    fi
}

if [ "$#" -ne 1 ]; then usage; fi
path=$1
check-vc
