# Game Model

The Game Model maintains the current state of the game.

## Score

Tracks the score for each player.

Properties:

- Current Score
- Bonus Score
- Multiplier

## Player

Tracks the active player and player-specific progress.

Properties:

- Player Number
- Current Score
- Current Ball
- Completed Missions
- Completed Challenges

## Ball

Tracks the current ball state.

Properties:

- Ball In Play
- Balls Remaining
- Ball Save Active

## Level

Represents the current game level.

Levels may enable or disable missions, challenges, targets, groups and sequences.

Properties:

- Level ID
- Level Name
- Completion State

## Mission

A mission is a larger objective that may span multiple targets, groups or sequences.

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

## Target Types

### Solo Target

A target that can be completed independently.

Properties:

- Target ID
- Target Name
- Score Value
- Repeatable
- Completed

Rules:

- A non-repeatable target can only be completed once.
- Additional hits are ignored until a reset occurs.

### Group Target

A collection of targets that must all be completed.

Order does not matter.

Properties:

- Group ID
- Group Name
- Member Targets
- Completion State

Rules:

- Any member target may be completed in any order.
- A group is completed when all member targets are completed.
- Completion generates a GROUP_COMPLETED event.

Example:

Targets:

A
B
C

Valid:

A
C
B

Result:

GROUP_COMPLETED

### Sequence Target

A collection of targets that must be completed in a specific order.

Properties:

- Sequence ID
- Sequence Name
- Ordered Targets
- Current Position
- Completion State

Rules:

- The next expected target must be activated.
- Any unexpected target immediately resets the sequence.
- Re-triggering a previously completed sequence target immediately resets the sequence.
- Completion generates a SEQUENCE_COMPLETED event.

Example Sequence:

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

A practical example is a ramp where the ball rolls back before reaching the final switch.

## Reset Conditions

Targets, groups and sequences can be reset by:

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

Successful completion of targets, groups and sequences may trigger:

- Score Changes
- Audio Effects
- Display Effects
- Lighting Effects
- Mission Progress
- Challenge Progress
- Arduino Commands

## Derived Events

The Game Model may generate higher-level events based on player progress.

Examples:

- GROUP_COMPLETED
- SEQUENCE_COMPLETED
- MISSION_COMPLETED
- CHALLENGE_COMPLETED
- LEVEL_COMPLETED

These events can be consumed by the Rule Engine in the same way as physical switch events.
