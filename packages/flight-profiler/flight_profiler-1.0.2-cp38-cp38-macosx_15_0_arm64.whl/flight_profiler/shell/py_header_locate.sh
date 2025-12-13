#!/bin/sh

if [ "$PYTHON_HEADER_PATH" != "" ]; then
    echo "$PYTHON_HEADER_PATH"
    exit 0
fi

py_path=$(which python3)
if [ "$py_path" = "" ]; then
    exit 0
fi

py_version=$($py_path --version|awk -F ' ' '{print $2}')
py_majar_version=$(echo $py_version|awk -F '.' '{print $1}')
py_minor_version=$(echo $py_version|awk -F '.' '{print $2}')

py_bin_dir=$(dirname "$py_path")

py_include_parent_dir="${py_bin_dir}/../include"
py_include_sub_dir=$(ls ${py_include_parent_dir} |grep "python${py_majar_version}.${py_minor_version}")



if [ "$py_include_sub_dir" != "" ]; then
    echo "${py_include_parent_dir}/${py_include_sub_dir}"
    exit 0
fi
