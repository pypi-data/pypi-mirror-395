#!/usr/bin/env bash

module=$1

find -L $module -name "*.pyi" | while read -r file; do
    absolufy-imports $file
done
