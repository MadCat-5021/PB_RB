# Architecture

## Threads

### InputScanner

Tasks:

- Read 48 switches
- Apply lockout debounce
- Generate input events

Events:

- SWITCH_PRESSED
- SWITCH_RELEASED
- SWITCH_HELD

### RuleEngine

Evaluates events within the current game context.

The RuleEngine updates the Game Model and generates commands for output managers.

### AudioManager

Tasks:

- Background music
- Sound effects
- Multiple simultaneous audio channels

### DisplayManager

Tasks:

- Animated backgrounds
- Foreground masks
- Images
- Videos
- GIFs
- Text layers

### ArduinoManager

Tasks:

- Send JSON messages
- Receive status information

## Event Flow

InputScanner
↓
InputQueue
↓
RuleEngine
↓
AudioQueue
DisplayQueue
ArduinoQueue
↓
Managers

# Design Philosophy

The system is event-driven.

Hardware inputs generate events.

Events are evaluated by the RuleEngine.

The RuleEngine updates the Game Model.

The RuleEngine never directly controls hardware.

The RuleEngine generates commands for specialized managers:

- AudioManager
- DisplayManager
- ArduinoManager

Managers execute commands asynchronously.

Communication between subsystems uses queues.
