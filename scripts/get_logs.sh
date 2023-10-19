#!/usr/bin/env bash

filename="$HOME/.pm2/logs/$2-$3.log"
num_lines=50

lines=$("$1" -n "$num_lines" "$filename")
echo "$lines"
echo "$1 - $2 - $3"