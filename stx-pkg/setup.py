#!/bin/bash

set -o errexit
set -o nounset

for repo in "fault" "metal" "config" "ha" "nfv" "clients"; do
    echo "Downloading $repo..."
    curl -L -o "stx-$repo-master.tar.gz" https://opendev.org/starlingx/$repo/archive/master.tar.gz 
done
