# Hardware

## Planned Hardware

- Raspberry Pi 4B
- 3x CD74HC4067 Multiplexer
- 48+ Switch Inputs
- Arduino Giga
- Display
- Audio System

## Raspberry Pi

Responsibilities:

- Input scanning
- Game engine
- Audio control
- Display control
- Arduino communication

## Input System

Three CD74HC4067 multiplexers provide 48 switch inputs.

Switches use lockout debounce.

Default lockout period:

- 20 ms

## Arduino Giga

Responsibilities:

- Lighting control
- Solenoid control
- Other real-time hardware outputs

Communication with the Raspberry Pi uses JSON messages.
