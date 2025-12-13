#!/bin/sh

server_pid=$1
py_path=$2

if [ "$server_pid" = "" ]; then
    exit 0
fi

if [ "$py_path" = "" ]; then
    exit 0
fi
py_bin_path=$(realpath "$py_path")
USER=$(ps -o user= -p "$server_pid")
server_bin_path=`readlink  /proc/${server_pid}/exe`

if [ "$USER" == "root" ] && [ "$EUID" -ne 0 ]; then
    echo "Target process is owned by root, try flight profiler by sudo flight_profiler ${server_pid}"
    exit 1
fi

if [ -z "$server_bin_path" ]; then
    echo "Target process_pid $server_pid not exists!"
	  exit 1
fi

if [ "$py_bin_path" != "$server_bin_path" ]; then
    exit 0
fi

base_addr=$(cat "/proc/${server_pid}/maps" | grep "$py_bin_path" | head -n 1 |awk -F '-' '{print $1}')
if [ "$base_addr" != "" ]; then
    echo $base_addr
fi
