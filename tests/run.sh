#!/bin/bash
env_file='./develop/compose.env'
cov_report_dir='./tests/cov-report'

if ! test -f $env_file; then
    echo "The env file ${env_file} is not found."
    exit 1
fi

if ! test -d $cov_report_dir; then
    echo "Cov report dir "${cov_report_dir}" is not exist."
    exit 1
fi

source $env_file 
export $(eval "echo \"$(cat $env_file)\"")

$PYTEST_EXE ./tests/*.py -vvv --cov ./src --cov-report term --cov-report html:${cov_report_dir}
if test -f /usr/bin/open; then
    /usr/bin/open ${cov_report_dir}/index.html
fi
