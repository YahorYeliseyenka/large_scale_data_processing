#!/usr/bin/env bash

cat /dev/urandom | tr -dc '0-9' | fold -w 150 | head -n $1
