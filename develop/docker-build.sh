#!/bin/bash -x

check_file () {
    if ! test -f $1; then
        echo "The file $1 is not found!"
        exit 1
    fi
}

pyproject_toml='./pyproject.toml'

check_file Dockerfile
check_file $pyproject_toml
PACKAGE_VERSION=$(egrep '^version' $pyproject_toml | awk -F '=' '{print $NF}'  | sed s'/"//'g | xargs)
PACKAGE_NAME='clickhouse-table-exporter'

docker build --build-arg="PACKAGE_VERSION=$PACKAGE_VERSION" --platform linux/amd64 --tag ${PACKAGE_NAME} .
docker tag $PACKAGE_NAME:latest $PACKAGE_NAME:$PACKAGE_VERSION

# Upload to docker hub
docker tag $PACKAGE_NAME:latest alexeyantropov/${PACKAGE_NAME}:${PACKAGE_VERSION}
docker tag $PACKAGE_NAME:latest alexeyantropov/${PACKAGE_NAME}:latest
docker push alexeyantropov/${PACKAGE_NAME}:${PACKAGE_VERSION}
docker push alexeyantropov/${PACKAGE_NAME}:latest
