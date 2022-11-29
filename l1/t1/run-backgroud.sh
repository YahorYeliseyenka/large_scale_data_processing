#!/usr/bin/env bash

file="pids.txt"

$@ &

echo $! >> $file
