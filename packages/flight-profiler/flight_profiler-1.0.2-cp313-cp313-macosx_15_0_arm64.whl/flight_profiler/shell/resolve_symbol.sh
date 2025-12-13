#!/bin/sh
pid=$1
symbol=$2


[ "$pid" = "" ] && \
	exit 1

if [ -z "$symbol" ]; then
    exit 1
fi

shell_bin_dir="$(dirname "$0")"
symbol_bin_path=$(sh $shell_bin_dir/resolve_bin_path.sh $pid)
line=$(nm $symbol_bin_path| grep $symbol| head -n 1)
if [ -z "$line" ]; then
    exit 1
fi
echo $line|awk -F ' ' '{print $1}'
