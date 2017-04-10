#!/usr/bin/env bash
#
# Deletes all kernels packages and headers except those concerning current 
# running one
#
# C. Guinet
#

RUNNING_KERNEL=$(uname -r | cut -d'-' -f1,2)
LAST_INSTALLED=$(dpkg -l | grep "linux-image" \
               | egrep -v 'linux-image-generic|extra|lts' | cut -d"-" -f 4 \
               | tail -n 1)

TOREMOVE=$(dpkg -l | egrep 'linux-headers|linux-image' \
        | egrep -v "linux-headers-generic|linux-image-generic|${LAST_INSTALLED}|${RUNNING_KERNEL}" \
        | awk '{print $2}')

echo "You're about to delete all these packages :"
echo
echo "${TOREMOVE}"
echo
echo "Are you sure you want to proceed (y/n)?"
read RESP

if [[ ${RESP} =~ ^(y|Y)$ ]]; then
    sudo apt-get purge ${TOREMOVE}
else
    exit 1
fi

