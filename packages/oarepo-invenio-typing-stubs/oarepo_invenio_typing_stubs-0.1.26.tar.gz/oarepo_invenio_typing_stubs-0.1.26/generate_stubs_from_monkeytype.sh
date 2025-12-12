#! /usr/bin/env bash

# Generate stubs from monkeytype
# arguments:
# $1 - package name to match
# $2 - output directory

PACKAGE_NAME=$1
OUTPUT_DIR=$2

monkeytype list-modules | egrep "^${PACKAGE_NAME}\." | while read ; do
    echo "Processing $REPLY"
    output_path="$OUTPUT_DIR/$(echo $REPLY | tr '.' '/')"
    # get parent directory of the output path
    parent_dir="$(dirname "$output_path")"
    mkdir -p "$parent_dir"
    monkeytype -v stub $REPLY >"${output_path}.pyi"
done