# Switch Definitions
A switch definition describes the behavior and properties of a physical switch.
Every physical switch has a unique switch_id.
Switches are atomic input devices.
Gameplay relationships are owned by structures within the Game Model.

## Common Properties
- Switch ID
- Name
- Category
- Enabled

## Categories

### Control Switch
A switch that may directly control hardware outputs.

Examples:
- Left Flipper Button
- Right Flipper Button
- Start Button
- Service Button
- Coin Button

Control switches may trigger relay outputs directly.
Control switches may also generate gameplay events.

### Game Switch
A switch used primarily for gameplay.
Examples:
- Target Switches
- Orbit Switches
- Ramp Switches
- Lane Switches
- Pop Bumper Switches
- Slingshot Switches
Game switches generate events for the Game Model.

## Direct Actions
A switch may define one or more direct actions.
Direct actions bypass the RuleEngine.
Examples:
Switch Pressed
↓
Activate Relay

Switch Released
↓
Deactivate Relay

Direct actions are intended for latency-sensitive functions.
Examples:
- Flippers
- Coil Power
- Autoplungers

## Hold Support

A switch may generate HOLD events.
Properties:
- Hold Enabled
- Hold Threshold

Example:
Hold Threshold = 500 ms
The interpretation of HOLD events is handled by the RuleEngine.

## Scoring
A switch may optionally provide a default score value.
The Game Model may override scoring based on:
- Level
- Mission
- Challenge
- Special Modes

Examples:
- 100 points
- 1000 points
- 10000 points

## Output Control

A switch may directly control outputs.
Examples:
- Relays
- Main Power Relay
Direct output control must not depend on:
- RuleEngine evaluation
- Arduino communication
- Network communication

## Example Definitions

### Left Flipper Button
Switch ID:
1
Category:
Control Switch
Direct Actions:
SWITCH_PRESSED
→ LEFT_FLIPPER_RELAY ON
SWITCH_RELEASED
→ LEFT_FLIPPER_RELAY OFF
Hold Enabled:
Yes
Hold Threshold:
500 ms

### Right Flipper Button
Switch ID:
2
Category:
Control Switch
Direct Actions:
SWITCH_PRESSED
→ RIGHT_FLIPPER_RELAY ON
SWITCH_RELEASED
→ RIGHT_FLIPPER_RELAY OFF
Hold Enabled:
Yes
Hold Threshold:
500 ms

### Ramp Entry
Switch ID:
21
Category:
Game Switch
Direct Actions:
None
Hold Enabled:
No
Notes:
This switch may participate in one or more structures.
Examples:
- LEFT_RAMP_SEQUENCE
- RAMP_RETURN_SEQUENCE
- MISSION_ALPHA
Structure membership is defined by the Game Model and not by the switch definition itself.

## Safety
Direct output activation shall support safety mechanisms.
Examples:
- Maximum activation time
- Emergency shutdown
- Main Power Relay disable

Loss of communication with AudioManager, DisplayManager or ArduinoManager must never prevent a control switch from operating its direct outputs.
