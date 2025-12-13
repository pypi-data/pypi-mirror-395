#!/bin/bash

server_pid=$1
py_path=$2

if [ "$server_pid" = "" ]; then
    exit 0
fi

if [ "$py_path" = "" ]; then
    exit 0
fi
py_bin_path=$(realpath "$py_path")

USER=$(ps -o user= -p "$server_pid" 2>/dev/null)

if [ "$USER" == "root" ] && [ "$EUID" -ne 0 ]; then
    echo "Target process is owned by root, try flight profiler by sudo flight_profiler ${server_pid}"
    exit 1
fi

server_bin_path=$(lsof -p "$server_pid" 2>/dev/null | grep "txt.*python" | awk '{print $9}' | head -1)
if [ -z "$server_bin_path" ]; then
    echo "Can't locate $server_pid executable path via lsof -p $server_pid, maybe process_pid $server_pid not exists!"
    exit 1
fi

if [ -L "$server_bin_path" ]; then
    server_bin_path=$(realpath "$server_bin_path")
fi

if [ "$py_bin_path" != "$server_bin_path" ]; then
    echo "flight_profiler and target process are not in the same python environment!"
    exit 1
fi

base_start_addr=$(otool -l "$py_bin_path" | grep -A 4 "segname __TEXT" | grep vmaddr | awk '{print $2}' | head -1)
if [ -z "$base_start_addr" ]; then
    echo "flight_profiler can't locate python executable base addr by otool -l!"
    exit 1
fi

base_addr=$(vmmap "$server_pid" 2>/dev/null | grep -A 5 "__TEXT.*python" | grep -E "^__TEXT" | awk '{print $2}' | cut -d'-' -f1 | head -1)

if [[ ! "$base_start_addr" =~ ^0x ]]; then
    base_start_addr="0x$base_start_addr"
fi
if [[ ! "$base_addr" =~ ^0x ]]; then
    base_addr="0x$base_addr"
fi

if [ -n "$base_addr" ]; then
   offset=$((base_addr - base_start_addr))
   printf "%x\n" $offset
fi
