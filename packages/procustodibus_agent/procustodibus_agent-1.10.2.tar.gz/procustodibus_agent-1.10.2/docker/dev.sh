#!/bin/sh -e

build=${BUILD:-$(date +%y%m%d.%H%M)}
hostname=$(uname -n)
tar=${TAR:-$(ls -1t dist/*.tar.gz | head -n1)}
version=${1:-$hostname}

docker build \
    --build-arg AGENT_TAR=$tar \
    --build-arg AGENT_REVISION=$(git rev-parse --short HEAD) \
    --build-arg IMAGE_BUILD=$build \
    --build-arg IMAGE_CREATED=$(date -Iseconds) \
    --build-arg IMAGE_VERSION=$version \
    --tag procustodibus-agent:$version \
    --tag procustodibus-agent:$version-i$build \
    --file docker/dev.dockerfile \
    .
