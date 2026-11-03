# States
The machine always operates in exactly one primary state.
State transitions are controlled by the Game Model and RuleEngine.

## BOOT
System startup.
Allowed Actions:
- Hardware initialization
- Display initialization
- Audio initialization

## PASSIVE
Idle mode
The machine is waiting on input
Examples:
- Slides
- slow light effects
- almost no sound

Possible Transitions:
- ACTIVE
- ATTRACT

## ACTIVE
Attentive mode
The machine is activated by either buttons or credits and waiting on input
Examples:
- Invitations to play
- Flashy light effects
- Alluring sounds

Possible Transitions:
- ATTRACT
- GAME_START
- SERVICE_MENU

## ATTRACT
Idle mode.
The machine is waiting for a player.
Examples:
- Attract video
- Lighting effects
- Intense audio

Possible Transitions:
- START_GAME
- ACTIVE

## GAME_START
Prepare a new game.
Examples:
- Reset score
- Reset structures
- Initialize player

Possible Transitions:
- BALL_START

## BALL_START
Prepare a new ball.
Examples:
- Enable playfield
- Reset ball-specific progress

Possible Transitions:
- PLAYING

## GAME_ACTIVE
Normal gameplay.
Examples:
- Score targets
- Progress missions
- Progress challenges

Possible Transitions:
- MISSION_ACTIVE
- CHALLENGE_ACTIVE
- BALL_END
- TILT

## MISSION_ACTIVE
A mission is currently active.

Possible Transitions:
- GAME_ACTIVE
- BALL_END
- TILT

## CHALLENGE_ACTIVE
A challenge is currently active.

Possible Transitions:
- GAME_ACTIVE
- BALL_END
- TILT

## BALL_END
Current ball completed.
Examples:
- Bonus calculation
- Bonus display

Possible Transitions:
- BALL_START
- GAME_OVER

## GAME_OVER
Game finished.
Examples:
- Final score
- High score evaluation

Possible Transitions:
- HIGH_SCORE_ENTRY
- ATTRACT

## HIGH_SCORE_ENTRY
Player enters initials.
Examples:
- Character selection
- Character scrolling

Possible Transitions:
- ATTRACT

## SERVICE_MENU
Maintenance and diagnostics.
Examples:
- Switch test
- Coil test
- Audio test

Possible Transitions:
- ATTRACT

## TILT
Safety state.
Examples:
- Disable scoring
- Disable gameplay

Possible Transitions:
- BALL_END
