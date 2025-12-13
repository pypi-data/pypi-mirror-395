#!/bin/sh -eu
# builds prod agent docker image
# eg `docker/agent.sh 1.2.3`
# eg `PUSH=1 docker/agent.sh latest`
push=${PUSH:-}
build=${BUILD:-$(date -u +%y%m%d$(test "$push" || echo "-%H%M%S"))}
git_version=$(bin/print-version.awk)
version=${1:-$git_version}
tar=${TAR:-}
image=procustodibus/agent

tags=''
if [ "$version" = latest -o "$version" = edge ]; then
    tag=$version
    version="${git_version%-*}"
    latest_version=$version
    while [ "$latest_version" != "${latest_version%.*}" ]; do
        latest_version=${latest_version%.*}
        tags="--tag $image:$latest_version $tags"
    done
    tags="--tag $image:$tag $tags"
fi

if [ ! "$tar" ]; then
    uv build --sdist
    tar=$(ls -1t dist/*.tar.gz | head -n1)
fi

build_args="
    --build-arg AGENT_TAR=$tar
    --build-arg AGENT_VERSION=$version
    --build-arg IMAGE_BUILD=$build
    $tags
    --tag $image:$version
    --tag $image:$version-i$build
    --file docker/agent.dockerfile
"

if [ "$push" ]; then
    docker buildx build $build_args \
        --annotation org.opencontainers.image.title='Pro Custodibus Agent' \
        --annotation org.opencontainers.image.description='Runs WireGuard and the Pro Custodibus Agent' \
        --platform linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6 \
        --provenance true --sbom true \
        --push \
        .
else
    docker build $build_args .
fi
