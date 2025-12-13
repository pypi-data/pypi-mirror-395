FROM procustodibus/agent:latest

ARG \
    AGENT_TAR=dist/agent.tar.gz \
    AGENT_TMP=/tmp/agent.tar.gz \
    INSTALL_VENV=/opt/venvs/procustodibus-agent

RUN apk add --no-cache \
    netcat-openbsd

COPY $AGENT_TAR $AGENT_TMP
RUN source $INSTALL_VENV/bin/activate && \
    python3 -m pip install $AGENT_TMP && rm $AGENT_TMP && \
    for file in $INSTALL_VENV/bin/procustodibus-*; do ln -fs $file /usr/local/bin; done

COPY docker/dev-fs /
RUN \
    rc-update add dev-custom-cacerts default && \
    rc-update add dev-custom-hosts default && \
    rc-update add dev-down-up default && \
    rc-update add dev-receive-traffic default && \
    rc-update add dev-send-traffic default

ARG \
    AGENT_REVISION \
    IMAGE_BUILD=dev \
    IMAGE_CREATED \
    IMAGE_VERSION

LABEL \
    com.procustodibus.image.build=$IMAGE_BUILD \
    org.opencontainers.image.authors=support@procustodibus.com \
    org.opencontainers.image.base.name=docker.io/procustodibus/agent:latest \
    org.opencontainers.image.description='Runs development version of the Pro Custodibus Agent' \
    org.opencontainers.image.created=$IMAGE_CREATED \
    org.opencontainers.image.documentation=https://docs.procustodibus.com/guide/agents/container/ \
    org.opencontainers.image.licenses=MIT \
    org.opencontainers.image.revision=$AGENT_REVISION \
    org.opencontainers.image.source=https://git.sr.ht/~arx10/procustodibus-agent \
    org.opencontainers.image.title='Pro Custodibus Agent Development' \
    org.opencontainers.image.url=https://www.procustodibus.com/ \
    org.opencontainers.image.vendor='Pro Custodibus' \
    org.opencontainers.image.version=$IMAGE_VERSION
