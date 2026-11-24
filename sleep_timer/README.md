# Sleep Timer

Shut the computer down after a set time, for falling asleep to music or a video. Set the
time with the mouse wheel on a small bar dial, drag a knob around a big dial in a panel,
or type hours and minutes. The bar widget, the panel and the Control Center tile always
show the same timer.

## Plugin

| Field | Value |
| --- | --- |
| ID | `nid25/sleep_timer` |
| Entries | Bar widget: `sleep_timer`; panel: `panel`; shortcut: `tile` |

## Requirements

- `shutdown` from systemd. The timer is a regular `shutdown -h +N`, so the system must
  let your user schedule a shutdown without a password, which is the default on most
  desktop setups with logind and polkit.
- `python3` (3.9 or newer, standard library only) on Noctalia's `PATH`. It runs
  `companion.py`, which lets the panel's dial knob be dragged. Without it the panel still
  works through the hour and minute fields.

## Usage

### Bar widget

Add the **Sleep Timer** widget to a bar in **Settings → Bar**. It shows the chosen time in
minutes inside a small dial.

- **Scroll** to change the time in 15-minute steps.
- **Left click** to start the timer.
- **Right click** to cancel a running timer.
- **Middle click** to open the panel.

While the timer runs, the dial counts down the remaining minutes in the accent color.

### Panel

Open it with a middle click on the bar widget, with the Control Center tile, or with:

```sh
noctalia msg panel-toggle nid25/sleep_timer:panel
```

- **Drag the knob** around the ring to change the time minute by minute. The knob grows
  while you hold it. Going past 12 o'clock adds or removes an hour.
- **Press anywhere on the ring** to move the knob there and keep dragging.
- **Scroll over the dial** to change the time in 15-minute steps.
- **Type hours and minutes** in the fields inside the dial, then press Enter or **Start**.
- **Cancel shutdown** stops a running timer.

The top row shows the current time and the time the computer will shut down.

### Control Center tile

Add **Sleep Timer** in **Settings → Control Center → Shortcuts**. Click it to open the
panel; right click starts the timer with the chosen time or cancels a running one. The
tile is highlighted and shows the remaining time while the timer runs.

### How the dials fill

Each lap of the ring is one hour. The first hour fills in the neutral color over dimmed
marks; the second hour fills in the theme's accent color over the first; the third in
the neutral color again, and so on. 2 h 30 min is two full laps plus half of a third.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `font_family` | `string` | `""` | Font for the numbers drawn on the bar and panel dials. Empty uses the shell font (`shell.font_family`), then `sans-serif`. |

## Notes

- **Commands:** `shutdown -h +N` to start and `shutdown -c` to cancel. A shutdown
  scheduled from a terminal shows up in the plugin too: it reads logind's schedule from
  `/run/systemd/shutdown/scheduled`.
- **Files:** the chosen minutes and the generated dial images (SVG) are written to the
  plugin's data directory. Old dial images are removed when the widget or panel loads.
- **Process:** opening the panel starts `python3 companion.py <data dir>/dial.sock`. It
  serves a single transparent pixel through Noctalia's pixel stream protocol, because a
  pixel stream is the only panel control that reports pointer press, drag and release.
  It exits about five seconds after the panel closes. It does not use the network.
- **Network:** none.
- **Limits:** the timer runs from 1 minute to 23 h 59 min.
