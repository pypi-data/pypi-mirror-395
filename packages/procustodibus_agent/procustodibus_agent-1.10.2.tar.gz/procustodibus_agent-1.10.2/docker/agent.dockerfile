FROM procustodibus/wireguard:latest

ARG \
    AGENT_TAR=dist/agent.tar.gz \
    AGENT_TMP=/tmp/agent.tar.gz \
    AGENT_VERSION=latest \
    IMAGE_BUILD=dev \
    INSTALL_VENV=/opt/venvs/procustodibus-agent

LABEL \
    com.procustodibus.image.build=$IMAGE_BUILD \
    org.opencontainers.image.authors=support@procustodibus.com \
    org.opencontainers.image.base.name=docker.io/procustodibus/wireguard:latest \
    org.opencontainers.image.description='Runs WireGuard and the Pro Custodibus Agent' \
    org.opencontainers.image.documentation=https://docs.procustodibus.com/guide/agents/container/ \
    org.opencontainers.image.licenses=MIT \
    org.opencontainers.image.source=https://git.sr.ht/~arx10/procustodibus-agent \
    org.opencontainers.image.title='Pro Custodibus Agent' \
    org.opencontainers.image.url=https://www.procustodibus.com/ \
    org.opencontainers.image.vendor='Pro Custodibus' \
    org.opencontainers.image.version=$AGENT_VERSION

RUN apk add --no-cache \
    gcc \
    libffi-dev \
    libsodium \
    make \
    musl-dev \
    python3-dev && \
    python3 -m venv $INSTALL_VENV && \
    source $INSTALL_VENV/bin/activate && \
    python3 -m pip install --upgrade pip setuptools && \
    echo 'pre-install pynacl, as it can take a long time to build' && \
    python3 -m pip install pynacl

COPY $AGENT_TAR $AGENT_TMP
RUN source $INSTALL_VENV/bin/activate && \
    python3 -m pip install $AGENT_TMP && rm $AGENT_TMP && \
    for file in $INSTALL_VENV/bin/procustodibus-*; do ln -fs $file /usr/local/bin; done

COPY scripts/linux /usr/local/lib/procustodibus/agent/scripts
COPY docker/agent-fs /
RUN rc-update add procustodibus-agent default
