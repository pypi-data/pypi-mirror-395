Pro Custodibus Agent
====================

[Pro Custodibus](https://www.procustodibus.com/) is a service that makes [WireGuard](https://www.wireguard.com/) networks easy to deploy and manage. You run the Pro Custodibus agent on each WireGuard host you want to manage, and the agent monitors and synchronizes the hosts' WireGuard settings with the remote Pro Custodibus service.


Installing
----------

Requires python 3.8 or newer and libsodium. Installer script can install requirements, plus the agent itself, on most linuxes, FreeBSD, OpenBSD, and macOS (if macOS has [Homebrew](https://brew.sh/)). Install from source like the following:
```
./install.sh --install
```

Or run it like the following to see more options:
```
./install.sh --help
```

See the [Installer Documentation](https://docs.procustodibus.com/guide/agents/install/) for full details (or to download the pre-built Windows installer).


Docker
------

The [docker/wireguard.dockerfile](https://git.sr.ht/~arx10/procustodibus-agent/tree/main/item/docker/wireguard.dockerfile) is built weekly and pushed to the [docker.io/procustodibus/wireguard](https://hub.docker.com/r/procustodibus/wireguard) repository. It produces a base WireGuard image without the agent.

The [docker/agent.dockerfile](https://git.sr.ht/~arx10/procustodibus-agent/tree/main/item/docker/agent.dockerfile) is built weekly and pushed to the [docker.io/procustodibus/agent](https://hub.docker.com/r/procustodibus/agent) repository. It produces a Docker image with WireGuard and the latest agent installed together.

Run either image by placing your WireGuard or Pro Custodibus configuration files in a host directory like `/srv/containers/wireguard/conf`, and then running the image like the following:
```
docker run \
    --cap-add NET_ADMIN \
    --publish 51820:51820/udp \
    --name wireguard \
    --rm \
    --volume /srv/containers/wireguard/conf:/etc/wireguard \
    procustodibus/agent
```

See the [Container Documentation](https://docs.procustodibus.com/guide/agents/container/) for full details.


Development
-----------

### Set up dev env

Install [uv](https://docs.astral.sh/uv/), and from this project root run:
```
uv python install
uv sync
```

### Dev tasks

Run unit tests:
```
uv run pytest
```

Run unit tests in watch mode:
```
uv run ptw .
```

Run unit tests with coverage report:
```
uv run pytest --cov
```

Run linter and auto-fix where possible:
```
uv run ruff check --fix
```

Run formatter:
```
uv run ruff format
```

Build and run docker dev image (with `*.conf` files in `/srv/containers/wireguard/conf`):
```
docker/dev.sh dev
docker run \
    --cap-add NET_ADMIN \
    --publish 51820:51820/udp \
    --name wireguard \
    --rm \
    --volume /srv/containers/wireguard/conf:/etc/wireguard \
    procustodibus-agent:dev
```

Run all (docker-based) installer tests:
```
docker compose -f test_install/docker-compose.yml build --pull
uv run pytest test_install
```

### Build Windows MSI

Install [uv](https://docs.astral.sh/uv/), and from this project root run:
```
uv run --python 3.12 --group freeze cx_freeze_setup.py bdist_msi
```


Contributing
------------

* [Code of Conduct](https://docs.procustodibus.com/community/conduct/)
* [File a Bug](https://docs.procustodibus.com/guide/community/bugs/)
* [Report a Vulnerability](https://docs.procustodibus.com/guide/community/vulns/)
* [Submit a Patch](https://docs.procustodibus.com/guide/community/code/)


Resources
---------

* Home page: https://www.procustodibus.com/
* Documentation: https://docs.procustodibus.com/guide/agents/run/
* Changelog: https://docs.procustodibus.com/guide/agents/download/#changelog
* Issue tracker: https://todo.sr.ht/~arx10/procustodibus
* Mailing list: https://lists.sr.ht/~arx10/procustodibus
* Source code: https://git.sr.ht/~arx10/procustodibus-agent


License
-------

[The MIT License](https://git.sr.ht/~arx10/procustodibus-agent/tree/main/LICENSE)
