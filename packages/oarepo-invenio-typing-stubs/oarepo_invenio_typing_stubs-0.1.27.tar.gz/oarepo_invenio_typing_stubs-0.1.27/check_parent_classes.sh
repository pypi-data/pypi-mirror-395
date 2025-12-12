#!/usr/bin/env bash

stubs=$1
venv_dir=$2

stubs=$(realpath $stubs)
venv_dir=$(realpath $venv_dir)

cd $stubs

find . -name '*.pyi' | while read -r file; do
    impl_file="${file%.pyi}.py"
    cat $venv_dir/$impl_file | egrep '^class ' | sed 's/(object)//' | sed 's/\.\.\.//g' | tr -d ' ' | sort > /tmp/impl_classes.txt
    cat $file | egrep '^class ' | sed 's/(object)//' | sed 's/\.\.\.//g' | tr -d ' ' | sort > /tmp/stub_classes.txt
    if ! diff -u /tmp/impl_classes.txt /tmp/stub_classes.txt &>/dev/null; then
        echo "Parent class mismatch in $stubs/$file"
        diff -u /tmp/impl_classes.txt /tmp/stub_classes.txt 
    fi
done