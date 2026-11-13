# Events

An event represents something that happened in the system.

Every subsystem communicates using events.

## Input Processing

Input processing uses lockout debounce.

The first valid state change is accepted immediately.

After an accepted state change, the switch enters a lockout period.

Additional transitions during the lockout period are ignored.

Default lockout duration:

- 20 ms

This strategy provides immediate response while preventing contact bounce from generating multiple events.

## Debounce State Machine

A switch can be in one of two logical states:

- ACTIVE
- INACTIVE

When a valid state transition is detected:

1. The event is generated immediately.
2. The switch enters lockout mode.
3. Additional transitions are ignored during the lockout period.
4. After the lockout expires, transition detection resumes.

## Input Events

### SWITCH_PRESSED

Generated when an inactive switch becomes active and the transition is accepted by the debounce system.

Properties:

- switch_id
- timestamp

### SWITCH_RELEASED

Generated when an active switch becomes inactive and the transition is accepted by the debounce system.

Properties:

- switch_id
- timestamp

### SWITCH_HELD

Generated when a switch remains active longer than the configured hold threshold.

Properties:

- switch_id
- timestamp

Default hold threshold:

- 500 ms

A switch may generate:

SWITCH_PRESSED
↓
SWITCH_HELD
↓
SWITCH_RELEASED

The meaning of a SWITCH_HELD event is determined by the current application context.

Examples:

Gameplay:

SWITCH_HELD
↓
Show game status information

High Score Entry:

SWITCH_HELD
↓
Start automatic character scrolling

Menu Navigation:

SWITCH_HELD
↓
Start automatic menu scrolling

The InputScanner only reports that a switch has been held.

The InputScanner does not determine the meaning of the hold action.

Interpretation of held events is the responsibility of the RuleEngine.

## Gameplay Events

### BALL_LAUNCHED

Signals that the ball has left the plunger. During development, the console
accepts `LAUNCHED` as a manual signal. A `PLUNGER` switch release and launch
sequence completion also publish this event.

The Game accepts this event only while waiting for the current ball to launch,
then publishes `BALL_STARTED`.

### BALL_DRAINED

Generated when the `DRAIN` switch is pressed for the active ball. If
shoot-again is active, the game deactivates it and supplies another ball.
Otherwise, a pending extra-ball award is consumed to supply another ball. If
neither applies, the game publishes `TURN_ENDED`.

### SHOOT_AGAIN_STARTED

Generated after the first ball of a turn is launched. The shoot-again window
becomes active for `SHOOT_AGAIN_TIMEOUT` seconds.

### EXTRA_BALL_AWARDED

Generated when gameplay awards an extra ball. This is separate from
`SHOOT_AGAIN_STARTED` so the display can show the appropriate message. It also
activates or refreshes the shoot-again window.

### SHOOT_AGAIN_EXPIRED

Generated when the shoot-again window ends, by timeout or when a drained ball
uses the active shoot-again.

### TURN_ENDED

Generated when a drained ball has neither active shoot-again nor a pending
extra-ball award.

If other players still need to play the current ball, the next player's turn
starts. Otherwise the next ball round starts. When all players have completed
`BALLS_PER_GAME`, the game publishes `GAME_ENDED`.

Each `PRE_TURN` prints the active player number, ball number, score, bonus, and
counts of completed missions and challenges to the console.

### GAME_ENDED

Generated after every player has completed the configured number of balls.

Properties:

- players
- balls_per_game
- balls_played
- results (per-player scores, bonuses, balls played, missions, and challenges)

When received, the game prints final scores and waits two seconds, enters
`HIGHSCORE`, and publishes `HIGHSCORES` with the final results. It prints
`HIGHSCORE SCREEN`, waits two more seconds, then returns to `ACTIVE`.

### HIGHSCORES

Generated after the game-over pause to provide final player results to the
high-score screen or future high-score manager.

Properties:

- results

### LAUNCH_COUNTDOWN_TICK

Generated for each launch countdown value from 5 through 1.

Properties:

- count

### LAUNCH_ZERO

Generated when the randomized pause after 1 ends and the bonus reaction window
begins.

### LAUNCH_BONUS_AWARDED

Generated when the ball launches during the five-second reaction window.
The awarded points are tracked as bonus, separately from regular score.
The launch manager also prints the reaction result: the bonus message, or
`Start infringement` for a launch before zero, or `Too slow` for a launch more
than five seconds after zero. No result is shown if no launch sequence was
started.

Properties:

- points
- reaction_time

## System Events

### SYSTEM_START

Generated when the application starts.

### SYSTEM_SHUTDOWN

Generated when the application stops.

## Audio Events

### AUDIO_STARTED

Generated when audio playback begins.

### AUDIO_FINISHED

Generated when audio playback ends.

## Display Events

### VIDEO_FINISHED

Generated when a video reaches its end.

### ANIMATION_FINISHED

Generated when an animation reaches its end.
