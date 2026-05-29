# Palette and Live Workflow

This document describes how to evolve the add-in from chat-in-Codex plus rebuild button into an in-Fusion panel.

## What A Palette Is

A Fusion palette is a persistent HTML panel. It is different from a command dialog:

- It can stay open while the user works.
- It is built with HTML/CSS/JavaScript.
- It is not tied to one command lifecycle.
- It can send messages to Python.
- Python can send messages back to JavaScript.

## Critical Limitation

Palette JavaScript cannot call the Fusion API directly.

Correct architecture:

```text
HTML/JavaScript
  -> adsk.fusionSendData(action, jsonString)
Python add-in
  -> palette.incomingFromHTML handler
  -> validate request
  -> update design_spec.json or call model_builder
  -> return status to HTML
Fusion API
  -> creates/updates geometry
```

## Current Project State

Fusion's template generated palette sample folders:

```text
commands/paletteShow/
commands/paletteSend/
```

They are inactive because `commands/__init__.py` only registers the rebuild command.

Agents can reuse those folders later, but should first design the message contract.

## Suggested Message Contract

From HTML to Python:

```json
{
  "action": "update_spec",
  "payload": {
    "length_mm": 120,
    "width_mm": 50
  }
}
```

Other actions:

- `rebuild`
- `get_spec`
- `set_spec`
- `update_spec`
- `validate_spec`
- `reset_spec`
- `export`

From Python to HTML:

```json
{
  "ok": true,
  "message": "Rebuilt Fusion Live Model",
  "spec": {}
}
```

For errors:

```json
{
  "ok": false,
  "message": "fillet_radius_mm is too large",
  "traceback": "..."
}
```

## UI Controls Worth Adding

Useful controls for Finn:

- Length, width, height inputs.
- Fillet radius input.
- Color picker.
- Rebuild button.
- Reset button.
- Export button.
- Status/log area.
- JSON editor for advanced mode.
- Preset dropdown for common shapes.

## Safety

- Validate JSON before writing it.
- Keep backups before replacing `design_spec.json`.
- Never run arbitrary Python from palette messages.
- Treat palette messages as data, not code.
- Return clear error messages.

## When To Build This

Do not build a palette just because the user asks for one more model change. Build it when the workflow becomes repetitive enough that in-Fusion controls save time.

Current reliable workflow remains:

1. Agent edits files.
2. Finn clicks `Rebuild Live Model`.

## References

- Autodesk, Using Palettes and Browser Command Inputs: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Palettes_UM.htm
- Autodesk, Palette.incomingFromHTML: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Palette_incomingFromHTML.htm

