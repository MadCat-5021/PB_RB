# Game Model

The Game Model maintains the current state of the game.

## Score

Tracks the score for each player.

Properties:

- Current Score
- Bonus Score
- Multiplier

Scores and bonuses belong to individual players and are maintained by the
PlayerManager. The ScoreManager calculates awards and applies them to the
active player's totals.

## Player

Tracks the active player and player-specific progress.

Properties:

- Player Number
- Current Score
- Current Ball
- Balls Played
- Completed Missions
- Completed Challenges

Players take turns playing the same ball number in order. A turn that ends
without shoot-again or an extra ball advances to the next player; after all
players complete a ball, the ball number advances. `BALLS_PER_GAME` sets the
last ball number for each player. Mission and challenge progress is stored
separately for each player.

## Ball

Tracks the current ball state.

Properties:

- Ball In Play
- Balls Remaining
- Ball Save Active

## Level

Represents the current game level.

Levels may enable or disable missions, challenges and structures.

Properties:

- Level ID
- Level Name
- Completion State

## Mission

A mission is a larger objective that may span multiple structures.

States:

- Inactive
- Active
- Completed
- Failed

Properties:

- Mission ID
- Mission Name
- Mission State
- Mission Progress

## Challenge

A challenge is a temporary objective that can modify scoring and gameplay.

States:

- Inactive
- Active
- Completed
- Failed

Properties:

- Challenge ID
- Challenge Name
- Challenge State
- Challenge Progress

## Switches

Switches are atomic input devices.

Switches do not own gameplay relationships.

A switch may participate in any number of gameplay structures.

Examples:

- Orbit Switch
- Ramp Switch
- Lane Switch
- Target Switch
- Pop Bumper Switch
- Slingshot Switch

## Structures

Structures define gameplay relationships between switches.

Examples:

- Solo Targets
- Groups
- Sequences
- Missions
- Challenges

A structure owns the relationship between switches.

A switch may participate in multiple structures simultaneously.

Example:

Orbit Left Entry

May participate in:

- LEFT_ORBIT_SEQUENCE
- RAMP_RETURN_SEQUENCE
- UPPER_PLAYFIELD_GROUP
- MISSION_ALPHA

## Solo Target

A structure consisting of a single switch.

Properties:

- Structure ID
- Structure Name
- Score Value
- Repeatable
- Completion State

Rules:

- A non-repeatable target can only be completed once.
- Additional hits are ignored until a reset occurs.

## Group Target

A structure consisting of multiple switches.

Order does not matter.

Properties:

- Structure ID
- Structure Name
- Member Switches
- Completion State

Rules:

- Any member switch may be activated in any order.
- A group is completed when all member switches have been activated.
- Completion generates a GROUP_COMPLETED event.

Example:

A
B
C

Valid:

A
C
B

Result:

GROUP_COMPLETED

## Sequence Target

A structure consisting of multiple switches that must be activated in a specific order.

Properties:

- Structure ID
- Structure Name
- Ordered Switches
- Current Position
- Completion State

Rules:

- The next expected switch must be activated.
- Any unexpected switch immediately resets the sequence.
- Re-triggering a previously completed sequence switch immediately resets the sequence.
- Completion generates a SEQUENCE_COMPLETED event.

Example:

A → B → C

Valid:

A
B
C

Result:

SEQUENCE_COMPLETED

Invalid:

A
A

Result:

SEQUENCE_RESET

Invalid:

A
C

Result:

SEQUENCE_RESET

Invalid:

A
B
A

Result:

SEQUENCE_RESET

Example:

Ramp Entry
↓
Orbit Left Entry
↓
Orbit Left Exit

A switch may simultaneously participate in other sequences, groups, missions or challenges.

## Reset Conditions

Structures can be reset by:

- New Ball
- New Player
- New Level
- Mission Start
- Mission End
- Challenge Start
- Challenge End
- Manual Reset

The applicable reset conditions are configurable.

## Effects

Successful completion of structures may trigger:

- Score Changes
- Audio Effects
- Display Effects
- Lighting Effects
- Mission Progress
- Challenge Progress
- Arduino Commands

## Derived Events

The Game Model may generate higher-level events.

Examples:

- GROUP_COMPLETED
- SEQUENCE_COMPLETED
- MISSION_COMPLETED
- CHALLENGE_COMPLETED
- LEVEL_COMPLETED

These events can be consumed by the RuleEngine in the same way as physical switch events.
