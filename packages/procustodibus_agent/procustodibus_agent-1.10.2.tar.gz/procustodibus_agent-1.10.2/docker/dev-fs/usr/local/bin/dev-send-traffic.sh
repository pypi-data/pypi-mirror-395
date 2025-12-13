#!/bin/sh
# sends traffic to TRAFFIC_HOSTS via netcat port 1234
# if a random number 0-1 is less than TRAFFIC_ODDS
# looping every TRAFFIC_LOOP seconds

# odds of sending traffic to a host
odds=${TRAFFIC_ODDS:-0.1}
# seconds to sleep before looping
loop=${TRAFFIC_LOOP:-53}
# list of hosts to send traffic to
# (each host optionally may be prefixed with host-specific odds)
hosts=${TRAFFIC_HOSTS:-10.0.0.1 0.05/10.0.0.2}
# port to send traffic to
port=${TRAFFIC_PORT:-1234}

# Outputs "1" if random number 0-1 is less than the first argument.
#
# $1 - Odds.
#
# Examples
#
#   > maybe 0.1
#
#   > maybe 0.1
#
#   > maybe 0.1
#   1
maybe() {
    awk -vo=$1 -vs=$RANDOM 'BEGIN { srand(s); print(rand() < o ? "1" : "") }'
}

# Sends traffic to the specified host on port 1234.
#
# $1 - Hostname.
#
# Examples
#
#   > traffic 10.0.0.1
traffic() {
    dd if=/dev/zero bs=1K count=$RANDOM | nc -q0 $1 $port
}

# Randomly sends traffic to the specified hosts.
#
# $1 - Odds of sending traffic to a host.
# $* - Hosts.
#
# Examples
#
#   > run 0.1 10.0.0.1 0.05/10.0.0.2
run() {
    local odds host_odds host
    odds=$1; shift
    while [ $# -gt 0 ]; do
        host=$(basename $1)
        host_odds=$(dirname $1)
        test "$host_odds" = "." && host_odds=$odds
        test "$(maybe $host_odds)" && traffic $host
        shift
    done
}

run $odds $hosts

while [ "$loop" -gt 1 ]; do
    sleep $loop
    run $odds $hosts
done
