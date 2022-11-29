#!/usr/bin/env bash

if [ "$#" -lt "3" ]; then
    echo "Illegal number of arguments"
else
    for i in "${@:3}"
    do  
        scp "$1/$i" $2
        # echo COPIED "$1/$i" TO $2
    done
fi