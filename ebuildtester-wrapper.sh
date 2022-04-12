#!/bin/bash

set -e -u

/app/usr/bin/ebuildtester --docker-command "flatpak-spawn --host docker" "$@"
