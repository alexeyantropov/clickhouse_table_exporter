#!/bin/bash -x -e

# Common variables.
env_file='./develop/compose.env'
compose_file='./develop/compose.yaml'
compose_common_arg="--file $compose_file --env-file $env_file"

# Preflight checks.
if ! test -f $env_file; then
    echo "The env file ${env_file} is not found."
    exit 1
fi

export $(eval "echo \"$(cat $env_file)\"")
source $env_file 

if ! test -f $compose_file; then
    echo "The docker compose config is not found."
    exit 1
fi

# Exit functions that stops containers by Ctrl+C call.
trap ctrl_c INT 
ctrl_c () {
    docker compose $compose_common_arg down
}

# Run them!
docker compose $compose_common_arg up --wait --force-recreate --renew-anon-volumes 

# Wait for the startup process. Don't use sleep() here! Only pooling!
set +x
echo -n "Starting env ..."
while true; do
    ret=$(curl -s ${CLICKHOUSE_ADDR}:${CLICKH_PORT_HTTP}/ | fgrep 'Ok.' | wc -l)
    test $ret -ge 1 && break
    sleep 1
    echo -n "."
done
echo -e "\nDone!\n"

docker ps

# The command waits for Ctrl+C but Ctrl+C makes is trapped.
echo -e "\nPress Ctrl+C to exit and stop container(s)."
sleep $((2**30))
