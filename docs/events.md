#Events
An event represents something that happened in the system.

Every subsystem communicates using events.

Input Processing
Input processing uses lockout debounce.

The first valid state change is accepted immediately.

After an accepted state change, the switch enters a lockout period.

Additional transitions during the lockout period are ignored.

Default lockout duration:

20 ms
This strategy provides immediate response while preventing contact bounce from generating multiple events.

Debounce State Machine
A switch can be in one of two logical states:

ACTIVE
INACTIVE
When a valid state transition is detected:

The event is generated immediately.
The switch enters lockout mode.
Additional transitions are ignored during the lockout period.
After the lockout expires, transition detection resumes.
Example:

INACTIVE ↓ ACTIVE ↓ SWITCH_PRESSED ↓ 20 ms lockout ↓ ACTIVE

ACTIVE ↓ INACTIVE ↓ SWITCH_RELEASED ↓ 20 ms lockout ↓ INACTIVE

Input Events
SWITCH_PRESSED
Generated when an inactive switch becomes active and the transition is accepted by the debounce system.

Properties:

switch_id
timestamp
After the event is generated the switch enters the debounce lockout period.

SWITCH_RELEASED
Generated when an active switch becomes inactive and the transition is accepted by the debounce system.

Properties:

switch_id
timestamp
After the event is generated the switch enters the debounce lockout period.

SWITCH_HELD
Generated when a switch remains active for a configured duration.

Properties:

switch_id
timestamp
duration_ms
Example durations:

1000 ms
3000 ms
5000 ms
A switch may generate:

SWITCH_PRESSED ↓ SWITCH_HELD ↓ SWITCH_RELEASED

SWITCH_REPEAT
Generated repeatedly while a switch remains active.

Typical use cases:

High score entry
Menu navigation
Service menus
Volume control
Value selection
Properties:

switch_id
timestamp
repeat_count
Typical sequence:

SWITCH_PRESSED ↓ 500 ms initial delay ↓ SWITCH_REPEAT ↓ SWITCH_REPEAT ↓ SWITCH_REPEAT ↓ SWITCH_RELEASED

Default values:

Initial delay: 500 ms
Repeat interval: 100 ms
Repeat behavior shall be configurable per switch.

System Events
SYSTEM_START
Generated when the application starts.

SYSTEM_SHUTDOWN
Generated when the application stops.

Audio Events
AUDIO_STARTED
Generated when audio playback begins.

AUDIO_FINISHED
Generated when audio playback ends.

Display Events
VIDEO_FINISHED
Generated when a video reaches its end.

ANIMATION_FINISHED
Generated when an animation reaches its end.
