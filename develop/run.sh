#!/bin/bash
env_file='./develop/compose.env'

if ! test -f $env_file; then
    echo "The env file ${env_file} is not found."
    exit 1
fi

source $env_file 
export $(eval "echo \"$(cat $env_file)\"")

$PYTHON_EXE ./src/exporter.py
