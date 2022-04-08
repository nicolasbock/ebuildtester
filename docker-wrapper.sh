#!/bin/bash -e

# make sure pre-req interfaces are connected
if ! snapctl is-connected docker-executables; then
    echo "the docker-executables content interface must be connected first!"
    echo "please run \"snap connect $SNAP_NAME:docker-executables docker:docker-executables\""
    exit 1
fi

if ! snapctl is-connected docker; then
    echo "the docker socket interface must be connected first!"
    echo "please run \"snap connect $SNAP_NAME:docker docker:docker-daemon\""
    exit 1
fi

# docker executables will be in $SNAP/docker-snap after the content interface is
# connected
$SNAP/docker-snap/bin/docker "$@"
