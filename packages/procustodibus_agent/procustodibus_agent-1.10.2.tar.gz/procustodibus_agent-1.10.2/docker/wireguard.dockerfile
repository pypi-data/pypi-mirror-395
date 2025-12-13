FROM alpine:latest

ARG \
    IMAGE_BUILD=dev \
    WIREGUARD_VERSION

LABEL \
    com.procustodibus.image.build=$IMAGE_BUILD \
    org.opencontainers.image.authors=support@procustodibus.com \
    org.opencontainers.image.base.name=docker.io/alpine:latest \
    org.opencontainers.image.description='Runs wg-quick under OpenRC' \
    org.opencontainers.image.documentation=https://docs.procustodibus.com/guide/wireguard/container/ \
    org.opencontainers.image.licenses=GPL-2.0 \
    org.opencontainers.image.source=https://git.sr.ht/~arx10/procustodibus-agent \
    org.opencontainers.image.title='WireGuard' \
    org.opencontainers.image.url=https://www.procustodibus.com/blog/2021/11/wireguard-containers/ \
    org.opencontainers.image.vendor='Pro Custodibus' \
    org.opencontainers.image.version=$WIREGUARD_VERSION

RUN apk add --no-cache \
    iptables \
    nftables \
    openrc \
    wireguard-tools

COPY docker/wireguard-fs /
RUN \
    sed -i 's/^\(tty\d\:\:\)/#\1/' /etc/inittab && \
    sed -i \
        -e 's/^#\?rc_env_allow=.*/rc_env_allow="\*"/' \
        -e 's/^#\?rc_sys=.*/rc_sys="docker"/' \
        /etc/rc.conf && \
    sed -i \
        -e 's/VSERVER/DOCKER/' \
        -e 's/checkpath -d "$RC_SVCDIR"/mkdir "$RC_SVCDIR"/' \
        /usr/libexec/rc/sh/init.sh && \
    rm \
        /etc/init.d/hwdrivers \
        /etc/init.d/machine-id && \
    sed -i 's/cmd sysctl -q \(.*\?\)=\(.*\)/[[ "$(sysctl -n \1)" != "\2" ]] \&\& \0/' /usr/bin/wg-quick && \
    rc-update add wg-quick default

VOLUME ["/sys/fs/cgroup"]
CMD ["/sbin/init"]
