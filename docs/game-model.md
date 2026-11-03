# Game Model

The Game Model maintains the current state of the game.

## Score

Tracks the score for each player.

## Player

Tracks the active player and player-specific progress.

## Ball

Tracks the current ball.

Examples:

- Current ball
- Balls remaining
- Ball in play

## Level

Represents the current game level.

Levels may enable or disable missions, challenges and targets.

## Mission

A mission is a larger objective that may span multiple targets, groups or sequences.

A mission can be:

- Inactive
- Active
- Completed
- Failed

## Challenge

A challenge is a temporary objective that can modify scoring and gameplay.

A challenge can be:

- Inactive
- Active
- Completed
- Failed

## Target Types

### Solo Target

A target that can be completed independently.

Properties:

- Target ID
- Score Value
- Repeatable

### Group Target

A collection of targets that must all be completed.

Order does not matter.

Properties:

- Group ID
- Member Targets
- Completion State
- Reset Rules

### Sequence Target

A collection of targets that must be completed in a specific order.

Incorrect activation causes the sequence to fail.

Properties:

- Sequence ID
- Ordered Targets
- Current Position
- Completion State
- Reset Rules

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

## Effects

Successful completion of targets, groups and sequences may trigger:

- Score Changes
- Audio Effects
- Display Effects
- Lighting Effects
- Mission Progress
- Challenge Progress
- Arduino Commands
