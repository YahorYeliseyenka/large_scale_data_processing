#!/usr/bin/env bash

file="pids.txt"
tpid=""

while IFS= read -r line || [[ -n "$line" ]]; do
    command="$(ps -o cmd "$line")"
    if [[ $command == *"$@"* ]]
    then
        tpid="$line"
        kill "$line"
        break
    fi
done < "$file"

if [ ! -z $tpid ]
then
    grep -v $tpid $file > temp && mv temp $file
    echo "Process killed"
else
    echo "There is no such command running in background"
fi
