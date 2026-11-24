# Sleep Timer for Noctalia

A [Noctalia](https://github.com/noctalia-dev/noctalia) plugin that shuts the computer down
after a set time. It has a bar dial, a panel with a draggable dial and a Control Center
tile. See [sleep_timer/README.md](sleep_timer/README.md) for usage.

## Install from this repository

```sh
noctalia msg plugins source add sleep-timer git https://github.com/Hal-Otacon-Emmerich/noctalia-sleep-timer
noctalia msg plugins enable nid25/sleep_timer
```

## Layout

The repository follows the layout of a Noctalia plugin source: one directory per plugin,
named after the part of the id after the `/`, and a `catalog.toml` at the root.

```
catalog.toml          # index for this repo as a plugin source
sleep_timer/
  plugin.toml         # manifest
  widget.luau         # bar widget
  panel.luau          # dial panel
  shortcut.luau       # Control Center tile
  timer.luau          # shared timer logic
  companion.py        # pointer layer for dragging the dial knob
  translations/en.json
  README.md           # plugin page
  thumbnail.webp      # store card, 960x540
```

To submit the plugin to the store, copy `sleep_timer/` into a fork of
[community-plugins](https://github.com/noctalia-dev/community-plugins) and open a pull
request. Do not copy `catalog.toml`; that repository generates its own.

## License

MIT, see [LICENSE](LICENSE).
