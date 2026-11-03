Events
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
Generated when a switch remains active longer than the configured hold threshold.

Properties:

switch_id
timestamp
Default hold threshold:

500 ms
A switch may generate:

SWITCH_PRESSED ↓ SWITCH_HELD ↓ SWITCH_RELEASED

The meaning of a SWITCH_HELD event is determined by the current application context.

Examples:

Gameplay:

SWITCH_PRESSED ↓ SWITCH_HELD ↓ Show game status information ↓ SWITCH_RELEASED ↓ Hide information

High Score Entry:

SWITCH_PRESSED ↓ Select next character ↓ SWITCH_HELD ↓ Start automatic character scrolling ↓ SWITCH_RELEASED ↓ Stop automatic character scrolling

Menu Navigation:

SWITCH_PRESSED ↓ Select next menu item ↓ SWITCH_HELD ↓ Start automatic menu scrolling ↓ SWITCH_RELEASED ↓ Stop automatic menu scrolling

The InputScanner only reports that a switch has been held.

The InputScanner does not determine the meaning of the hold action.

Interpretation of held events is the responsibility of the RuleEngine.

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
