#!/bin/bash -x

check_file () {
    if ! test -f $1; then
        echo "The file $1 is not found!"
        exit 1
    fi
}

env_file='./develop/compose.env'
check_file $env_file
source $env_file 
export $(eval "echo \"$(cat $env_file)\"")

basename=$(basename $0)

if test "$basename" = "upload-test.sh"; then
    pypi_rc='./.pypirc-test.ini'
elif test "$basename" = "upload-prod.sh"; then
    pypi_rc='./.pypirc-prod.ini'
else
    echo "Do not run upload.sh!"
    exit 1
fi

check_file $pypi_rc

$PYTHON_EXE -m build && \
$PYTHON_EXE -m twine upload --config-file $pypi_rc --repository testpypi dist/*