#!/bin/sh -eu
# checkconfig: 2345 80 20
# PROVIDE: procustodibus-agent
# REQUIRE: DAEMON
### BEGIN INIT INFO
# Provides: procustodibus-agent
# Required-Start: $local-fs $network
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Pro Custodibus Agent
# Description: Synchronizes your WireGuard settings with Pro Custodibus.
### END INIT INFO

command=/opt/venvs/procustodibus-agent/bin/procustodibus-agent
command_args="--loop=120 --verbosity=INFO"
description="Pro Custodibus Agent"
path=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
pidfile=/var/run/procustodibus-agent.pid
logfile=/var/log/procustodibus-agent.log

test -f $pidfile && pid=$(<$pidfile) || pid=""
test "$pid" -a "$(readlink -f /proc/$pid/exe)" = $command || pid=""

status() {
    test "$pid" && echo "started" || echo "stopped"
}

start() {
    if [ "$pid" ]; then
        echo "already running!"
        exit 1
    fi

    touch $logfile && date >>$logfile
    echo "starting $description ..." | tee -a $logfile

    PATH=$path nohup $command $command_args >>$logfile 2>&1 &
    echo "$!" >$pidfile

    echo "... started $description" | tee -a $logfile
}

stop() {
    if [ ! "$pid" ]; then
        echo "not running!"
        exit 1
    fi

    touch $logfile && date >>$logfile
    echo "stopping $description ..." | tee -a $logfile

    kill $pid
    rm $pidfile

    echo "... stopped $description" | tee -a $logfile
}

case "${1-}" in
    status) status ;;
    start) start ;;
    restart) test ! "$pid" || stop; start ;;
    stop) stop ;;
    *) echo "usage: $0 {status|start|restart|stop}" ;;
esac
