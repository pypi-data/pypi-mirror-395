#!/bin/sh -e

docker pull alpine:latest

build=${BUILD:-$(date +%y%m%d)}
version=$(
    docker run --rm alpine:latest \
    sh -c 'apk add --quiet --no-cache wireguard-tools && wg --version' |
    awk '{ print $2 }'
)

subversion=$version
tags=""
while [ "$subversion" != "${subversion%.*}" ]; do
    subversion=${subversion%.*}
    tags="--tag procustodibus/wireguard:$subversion $tags"
done

if [ "$PUSH" ]; then
    build_cmd="buildx build --push --platform linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6"
else
    build_cmd=build
fi

docker $build_cmd \
    --pull \
    --build-arg IMAGE_BUILD=$build \
    --build-arg WIREGUARD_VERSION=$version \
    --tag procustodibus/wireguard:latest \
    $tags \
    --tag procustodibus/wireguard:$version \
    --tag procustodibus/wireguard:$version-i$build \
    --file docker/wireguard.dockerfile \
    .
