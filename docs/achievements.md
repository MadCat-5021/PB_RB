# achievements.md

## Doel
Achievements zijn langetermijndoelen.
Achievements staan los van:
- States
- Missions
- Challenges
- Current Game
Voortgang blijft behouden tijdens een spel.

## Trigger Types

### Switch Counter
Telt het totaal aantal hits op een switch.
Voorbeeld:
POP_BUMPER_100
Requirement:
100 hits op POP_BUMPER
Result:
ACHIEVEMENT_COMPLETED

### Group Counter
Telt het totaal aantal voltooide groups.
Voorbeeld:
UPPER_PLAYFIELD_MASTER
Requirement:
50x UPPER_PLAYFIELD_GROUP voltooid
Result:
ACHIEVEMENT_COMPLETED

### Sequence Counter
Telt het totaal aantal voltooide sequences.
Voorbeeld:
LEFT_ORBIT_MASTER
Requirement:
25x LEFT_ORBIT_SEQUENCE voltooid
Result:
ACHIEVEMENT_COMPLETED

### Ordered Target Sequence
Specifieke volgorde van targets.
Voorbeeld:
SKILL_SHOT_CHAIN
Requirement:
TOP_LANE
↓
RAMP_ENTRY
↓
LEFT_ORBIT
Result:
ACHIEVEMENT_COMPLETED
Bij een foutieve stap:
ACHIEVEMENT_RESET

### Lifetime Counter
Telt gebeurtenissen over meerdere spellen.
Voorbeeld:
POP_BUMPER_1000
Requirement:
1000 POP_BUMPER hits
Result:
ACHIEVEMENT_COMPLETED

## Events
Generated:
- ACHIEVEMENT_PROGRESS_UPDATED
- ACHIEVEMENT_COMPLETED
- ACHIEVEMENT_RESET

## Ownership Model
Achievements bezitten hun eigen requirements.
Requirements verwijzen naar:
- Switches
- Groups
- Sequences
Switches kennen geen Achievements.
Groups kennen geen Achievements.
Sequences kennen geen Achievements.

## Examples
BEGINNER_POPS
Requirement:
100x POP_BUMPER

ORBIT_MASTER
Requirement:
50x LEFT_ORBIT_SEQUENCE

UPPER_PLAYFIELD_EXPERT
Requirement:
25x UPPER_PLAYFIELD_GROUP

COMBO_HUNTER
Requirement:
LEFT_ORBIT_ENTRY
↓
RAMP_ENTRY
↓
TOP_TARGET
Completion Result:
ACHIEVEMENT_COMPLETED
