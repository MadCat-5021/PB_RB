# Hardware

## Planned Hardware

- Raspberry Pi 4B
- 4x CD74HC4067 Multiplexer
- Up to 64 Switch Inputs
- Relay Outputs
- Main Power Relay
- Arduino Giga
- Display
- Audio System

## Raspberry Pi

Responsibilities:

- Input scanning
- Game engine
- Audio control
- Display control
- Direct relay control
- Main power control
- Arduino communication

## Input System

Four CD74HC4067 multiplexers provide a maximum of 64 switch inputs.

The fourth multiplexer is included from the initial design to allow future expansion without architectural changes.

Switches use lockout debounce.

Default lockout period:

- 20 ms

## Switch Categories

### Control Switches

Control switches may directly control hardware outputs.

Examples:

- Left Flipper
- Right Flipper
- Slingshots
- Pop Bumpers
- Autoplunger

These functions bypass the RuleEngine to minimize latency.

Control switches may still generate events for gameplay logic.

Example:

Flipper Button
├── Direct Coil Activation
└── SWITCH_PRESSED Event

### Game Switches

Game switches are evaluated by the Game Model and RuleEngine.

Examples:

- Targets
- Rollover Lanes
- Ramp Sensors
- Mission Targets
- Challenge Targets

## Coil Control

Certain switches may directly control relays.

These actions bypass the RuleEngine.

This prevents latency introduced by event processing or communication delays.

Example:

Switch
↓
Direct Relay Activation

## Main Power Relay

A dedicated main power relay controls the power feed to all coil relays.

When disabled:

- All coils become inactive
- Relay power is removed

The Raspberry Pi controls the main power relay directly.

This relay acts as the primary coil safety mechanism.

## Flipper Coils

Flipper coils use dual windings:

- Power winding
- Hold winding

An EOS (End Of Stroke) switch disconnects the power winding when the flipper reaches its end position.

The hold winding remains energized while the flipper button is held.

This reduces power consumption and coil heating.

Flipper activation is handled directly by the Raspberry Pi without RuleEngine involvement.

## Arduino Giga

Responsibilities:

- Lighting effects
- LED patterns
- Auxiliary outputs
- Non-critical effects

Loss of communication with the Arduino must never affect:

- Flippers
- Pop Bumpers
- Slingshots
- Coil Power
- Safety Functions

Communication with the Raspberry Pi uses JSON messages.
