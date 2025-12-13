# Decky Remote

Development tool for Decky plugins.

## Installation

Run directly with `uvx` (no installation required):
```bash
uvx decky-remote ssh utilities/ping
```

Or install with `pipx` for persistent access:
```bash
pipx install decky-remote
```

Or install from local repository:
```bash
# Using uvx
uvx --from /path/to/decky-remote decky-remote --help

# Using pipx
pipx install /path/to/decky-remote
```

## Features

 1. Tail logs: `decky-remote plugin logs "Example Plugin"`
 2. Call Decky websocket methods:
    * Reload plugin: `decky-remote ssh loader/reload_plugin "Example Plugin"`
    * Call plugin function: `decky-remote ssh loader/call_plugin_method "Example Plugin" start_timer`
    * (See [the Decky Loader source](https://github.com/search?q=repo%3ASteamDeckHomebrew%2Fdecky-loader%20ws.add_route&type=code) for available routes.)

⚠️ This is a development tool that can break at any point. It is not part of Decky.
