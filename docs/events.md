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
