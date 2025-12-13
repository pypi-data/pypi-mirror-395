# slidgnal

A
[feature-rich](https://slidge.im/docs/slidgnal/main/user/features.html)
[Signal](https://signal.org) to
[XMPP](https://xmpp.org/) puppeteering
[gateway](https://xmpp.org/extensions/xep-0100.html), based on
[slidge](https://slidge.im) and
[signalmeow](https://github.com/mautrix/signal/tree/main/pkg/signalmeow).

[![CI pipeline status](https://ci.codeberg.org/api/badges/14065/status.svg)](https://ci.codeberg.org/repos/14065)
[![Chat](https://rooms.slidge.im:5281/muc_badge/support@rooms.slidge.im)](https://slidge.im/xmpp-web/#/guest?join=support@rooms.slidge.im)
[![PyPI package version](https://badge.fury.io/py/slidgnal.svg)](https://pypi.org/project/slidgnal/)




slidgnal lets you chat with users of Signal without leaving your favorite XMPP client.

## Quickstart

```sh
docker run codeberg.org/slidge/slidgnal \  # works with podman too
    --jid signal.example.org \  # can be whatever you want it to be
    --secret some-secret \  # must match your XMPP server config
    --home-dir /somewhere/writeable  # for data persistence
```

Use the `:latest-amd64` tag for the latest release, `:vX.X.X-amd64` for release X.X.X, and `:main-amd64`
for the bleeding edge.`-arm64` images are also available.

If you do not like containers, other installation methods are detailed
[in the docs](https://slidge.im/docs/slidgnal/main/admin/install.html).

## Documentation

Hosted on [codeberg pages](https://slidge.im/docs/slidgnal/main/).

## Contributing

Contributions are **very** welcome, and we tried our best to make it easy
to start hacking on slidgnal. See [CONTRIBUTING.md](./CONTRIBUTING.md).
