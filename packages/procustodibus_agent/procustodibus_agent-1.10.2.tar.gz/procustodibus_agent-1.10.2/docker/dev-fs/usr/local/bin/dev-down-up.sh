#!/bin/sh
# toggles up/down each wireguard interface configured for the host
# if a random number 0-1 is less than DOWN_UP_ODDS
# looping every DOWN_UP_LOOP seconds

# odds of starting up or shutting down an interface
odds=${DOWN_UP_ODDS:-0.001}
# seconds to sleep before looping
loop=${DOWN_UP_LOOP:-50}

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

# Toggles the specified interface up or down.
#
# $1 - Interface name.
#
# Examples
#
#   > toggle wg0
#   [#] ip link delete dev wg0
toggle() {
    wg show $1 >/dev/null 2>&1 && wg-quick down $1 || wg-quick up $1
}

# Lists available wireguard config files.
#
# Examples
#
#   > config_files
#   /etc/wireguard/wg0.conf
#   /etc/wireguard/wg1.conf
config_files() {
    grep '\[Interface\]' /etc/wireguard/*.conf -l 2>/dev/null
}

# Randomly toggles wireguard interfaces up or down.
#
# $1 - Odds of toggling each interface.
#
# Examples
#
#   > run 0.9
#   [#] ip link delete dev wg0
#   [#] ip link add wg1 type wireguard
#   [#] wg setconf wg1 /dev/fd/63
#   [#] ip -4 address add 10.0.0.1/32 dev wg1
#   [#] ip link set mtu 1420 up dev wg1
#   [#] ip -4 route add 10.0.0.2/32 dev wg1
run() {
    for file in $(config_files); do
        interface=$(basename $file .conf)
        test "$(maybe $1)" && toggle $interface
    done
}

run $odds

while [ "$loop" -gt 1 ]; do
    sleep $loop
    run $odds
done
