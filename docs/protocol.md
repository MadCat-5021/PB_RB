# Protocol

## Raspberry Pi ↔ Arduino

Communication uses JSON messages over a serial connection.

## Design Goals

- Human readable
- Easy to debug
- Extensible
- Versionable

## Example Messages

Activate output:

{
  "command": "output_on",
  "id": 1
}

Deactivate output:

{
  "command": "output_off",
  "id": 1
}

Play light effect:

{
  "command": "light_effect",
  "effect": "strobe"
}

Heartbeat:

{
  "command": "heartbeat"
}

Status reply:

{
  "status": "ok"
}
