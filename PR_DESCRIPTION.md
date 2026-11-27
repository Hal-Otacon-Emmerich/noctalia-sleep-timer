<!-- noctalia-pr-template:v1 -->

## Plugin

- **Id:** `nid25/sleep_timer`
- [x] New plugin (version 2.3.2)
- [ ] Update to an existing plugin (version bumped in `plugin.toml`)

## What it does

Shuts the computer down after a set time, for falling asleep to music or a video. It has three entries that always show the same timer:

- **Bar widget** (`sleep_timer`): a small dial. Scroll changes the time in 15-minute steps, left click starts, right click cancels, middle click opens the panel.
- **Panel** (`panel`): a large dial with a draggable knob, hour and minute fields, and the shutdown time. Open it with `noctalia msg panel-toggle nid25/sleep_timer:panel`.
- **Control Center tile** (`tile`): opens the panel; right click starts or cancels the timer and shows the remaining time.

The timer is a transient systemd user timer owned by the plugin (`noctalia-sleep-timer.timer`), and that unit is the source of truth for the countdown. Until systemd has answered, the timer state is "unknown", never idle: the bar dial and the tile show `?`, the panel shows both Start and Cancel, and the tile's right click cancels. A status answer sent before a Start or Cancel began or ended is discarded. The plugin never reads, replaces or cancels logind's shutdown schedule: a shutdown or reboot scheduled with `shutdown` or by any other program is left alone and is no longer displayed in the plugin.

## External dependencies

- `systemd-run` and `systemctl` (systemd, with a user manager running): start, stop and read the plugin's own user timer, which runs `systemctl poweroff`.
- `python3` (3.9+, standard library only): runs `companion.py` while the panel is open. It serves one transparent pixel over the pixel stream protocol, because a pixel stream is the only panel control that reports pointer press, drag and release. Without it the panel still works through the hour and minute fields.

Everything the plugin does outside Luau:

- **Processes** (all argv form, systemctl calls with a 10 s timeout):
  - start: `systemd-run --user --unit=noctalia-sleep-timer --collect --on-active=<N>s --timer-property=AccuracySec=1s --timer-property=RemainAfterElapse=no systemctl poweroff`
  - cancel: `systemctl --user stop noctalia-sleep-timer.timer`
  - status: `systemctl --user list-timers --all --no-pager --output=json noctalia-sleep-timer.timer`, when the bar widget or tile loads, when the panel opens, and every 30 s while a timer runs or its state is unknown (one check shared by all entries). Nothing is polled once systemd has confirmed that no timer runs.
  - `python3 companion.py <data dir>/dial.sock` when the panel opens. The companion holds a lock file so only one copy serves the socket (a second copy waits up to ~6 s for the first to exit, then gives up), and exits about 5 seconds after the panel closes.
- **Files written**, all in `noctalia.pluginDataDir()`: `minutes` (the chosen time), `deadline` (the timer's last known end time and boot id, a cache for drawing the countdown that is synced from systemd), dial images `dial-*.svg` / `panel-*.svg` (at most two per entry, all removed on load), `dial.sock` and `dial.sock.lock`.
- **Network:** none.

## Testing

Tested on NixOS with Niri. Added the bar widget, opened the panel and the Control Center tile; started and cancelled the timer from each and from a terminal, checked `systemctl --user list-timers`; dragged the knob across 12 o'clock, scrolled, typed times including over 23:59; typed invalid input such as `00`; checked that a scheduled `shutdown -r` is left alone; let the timer power the machine off; changed the `font_family` and `dial_size` settings. Validated with `validate-plugins.py --profile community` at the commit pinned in CI.

- [x] Tested on Niri
- [ ] Tested on Hyprland
- [ ] Tested on Sway
- [ ] Tested on another compositor:
- **Noctalia version tested against:** 5.6.0
- **Plugin API level:** 52

## Screenshots / Videos

<!-- Drag the bar widget, panel and Control Center tile screenshots here -->

## Checklist

- [x] The directory name matches the part of `id` after the `/` in `plugin.toml` exactly.
- [x] It ships `plugin.toml`, `README.md`, `thumbnail.webp`, and `translations/en.json`.
- [x] `README.md` follows the [README template](https://github.com/noctalia-dev/community-plugins/blob/main/README_TEMPLATE.md), documents every entry id and dependency, and includes exact panel IPC commands and launcher prefixes where applicable.
- [x] `thumbnail.webp` is present and relevant; for a new plugin I created it with the [thumbnail generator](https://assets.noctalia.dev/plugins/thumbnail-generator.html), and for an update I regenerated it with the generator if the visual identity or user-facing appearance changed.
- [x] `version` follows semver and is bumped in this PR; `plugin_api` is the oldest API level this plugin requires.
- [x] Every non-English translation in this PR uses a locale supported by Noctalia core, and I can read, write, and understand that language well enough to review and maintain it (no unreviewed machine/LLM translations).
- [x] I did not edit `catalog.toml`; CI generates it.
- [x] This PR touches exactly one plugin directory.

## Code review attestation

- [x] The code is readable and not obfuscated, minified, or generated.
- [x] Code identifiers and code comments are in English.
- [x] It does not download and execute remote code.
- [x] Every network call, filesystem write, and spawned process is something the description above accounts for.
- [x] I have the right to publish this code under the `license` declared in `plugin.toml`.
