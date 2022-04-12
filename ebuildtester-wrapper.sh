#!/bin/bash

set -e -u

ebuildtester --docker-command "flatpak-spawn --host docker" "$@"
