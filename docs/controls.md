# Controls
Control switches are machine control interfaces.
Unlike game switches, control switches primarily affect machine operation, game flow or administration.

## Credit Button
Functions:
- Add Credit
- Wake machine from PASSIVE
Allowed States:
- PASSIVE
- ATTRACT
Ignored States:
- SERVICE_MENU

## Start Button
Functions:
- Start Game
- Add Player
Allowed States:
- ATTRACT
- GAME_START
Ignored States:
- GAME_ACTIVE
- MISSION_ACTIVE
- CHALLENGE_ACTIVE

Notes:
- Adds additional players before the first ball of the first player is drained
- Starts a game when sufficient credits are available
- May be used to confirm selections in menus

## Left Flipper Button
Functions:
- Control Left Flipper
- Menu Navigation
- Character Selection
- Information Display
Direct Actions:
- SWITCH_PRESSED → LEFT_FLIPPER_RELAY ON
- SWITCH_RELEASED → LEFT_FLIPPER_RELAY OFF
Possible Behaviors:
ATTRACT:
- Navigate Menus
HIGH_SCORE_ENTRY:
- Previous Character
GAME_ACTIVE:
- Operate Flipper
MISSION_ACTIVE:
- Operate Flipper
- Mission Specific Functions
CHALLENGE_ACTIVE:
- Operate Flipper
- Challenge Specific Functions
SWITCH_HELD:
- Show Status Information
- Show Mission Progress
- Show Challenge Progress

## Right Flipper Button
Functions:
- Control Right Flipper
- Menu Navigation
- Character Selection
- Information Display
Direct Actions:
- SWITCH_PRESSED → RIGHT_FLIPPER_RELAY ON
- SWITCH_RELEASED → RIGHT_FLIPPER_RELAY OFF
Possible Behaviors:
ATTRACT:
- Navigate Menus
HIGH_SCORE_ENTRY:
- Next Character
GAME_ACTIVE:
- Operate Flipper
MISSION_ACTIVE:
- Operate Flipper
- Mission Specific Functions
CHALLENGE_ACTIVE:
- Operate Flipper
- Challenge Specific Functions
SWITCH_HELD:
- Show Status Information
- Show Mission Progress
- Show Challenge Progress

## Admin Switch
Internal cabinet switch.
Functions:
- Enable Coil Power
- Disable Coil Power
- Enable Debug Functions
- Enable Service Features
Allowed States:
- SERVICE_MENU
Actions:
- ADMIN_ON → Enable Coil Power
- ADMIN_OFF → Disable Coil Power
Notes:
- Not accessible to players
- Intended for testing, diagnostics and maintenance

## Main Power Relay
Functions:
- Enable Coil Power
- Disable Coil Power
When Disabled:
- Flippers Disabled
- Slingshots Disabled
- Pop Bumpers Disabled
- Autoplungers Disabled
- All Coil Outputs Disabled
Notes:
- Primary coil safety mechanism
- Controlled directly by Raspberry Pi
- Independent of Arduino communication

## Tilt Switch
Functions:
- Generate TILT Event
Actions:
- SWITCH_PRESSED → TILT
Results:
- Disable Scoring
- Disable Mission Progression
- Disable Challenge Progression
- Disable coil power
- Preserve Ball Tracking
- Wait For Ball Drain

## Service Controls
Available only in SERVICE_MENU.
Functions:
- Switch Test
- Coil Test
- Audio Test
- Display Test
- Configuration
- Diagnostics
Available Inputs:
- Left Flipper Button
- Right Flipper Button
- Start Button
- Credit Button

## Control Philosophy
Control switches may:
- Directly control hardware
- Generate events
- Change machine states
- Change game states
Control switches are not targets.
Control switches do not belong to:
- Solo Targets
- Groups
- Sequences
Control switches may behave differently depending on the current state.
Example:
Left Flipper Button
ATTRACT:
- Navigate Menus
HIGH_SCORE_ENTRY:
- Previous Character
GAME_ACTIVE:
- Flipper Control
SERVICE_MENU:
- Test Navigation

## Direct Hardware Control
Certain controls require immediate response.
These controls bypass the RuleEngine for their primary function.
Examples:
- Left Flipper Button
- Right Flipper Button
- Main Power Relay
A control may simultaneously:
- Perform a direct hardware action
- Generate an event
Example:
Left Flipper Button
↓
LEFT_FLIPPER_RELAY ON
↓
SWITCH_PRESSED Event
The hardware action must not depend on:
- RuleEngine execution
- AudioManager execution
- DisplayManager execution
- Arduino communication
