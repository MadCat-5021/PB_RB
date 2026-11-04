# Rules

## Doel
Rules vertalen events naar gameplaygedrag.
Rules bevatten geen hardwarelogica.
Rules verwerken uitsluitend events.

## Verantwoordelijkheden
- Score verwerking
- Group verwerking
- Sequence verwerking
- Mission verwerking
- Challenge verwerking
- Achievement verwerking
- Ball verwerking
- Player verwerking
- State transitions
- Audio triggers
- Display triggers

## Input
Ontvangt events uit het Event System.
Voorbeelden:
- SWITCH_PRESSED
- SWITCH_RELEASED
- SWITCH_HELD
- GROUP_COMPLETED
- SEQUENCE_COMPLETED
- BALL_DRAINED
- AUDIO_FINISHED
- VIDEO_FINISHED

## Output
Genereert nieuwe events.
Voorbeelden:
- SCORE_AWARDED
- GROUP_COMPLETED
- SEQUENCE_COMPLETED
- MISSION_STARTED
- MISSION_COMPLETED
- CHALLENGE_STARTED
- CHALLENGE_COMPLETED
- ACHIEVEMENT_COMPLETED
- BALL_STARTED
- BALL_ENDED

## Event Queue
Events worden FIFO verwerkt.
Event handlers mogen nieuwe events genereren.
Nieuwe events worden achteraan de queue toegevoegd.

## State Awareness
Rules zijn state-aware.
Voorbeelden:
- GAME_ACTIVE
- MISSION_ACTIVE
- CHALLENGE_ACTIVE
- BALL_DRAINED
- GAME_OVER
Rules mogen verschillend reageren afhankelijk van de actieve state.

## Group Rules
Bij een geldige group:
Generate:
- GROUP_COMPLETED
Groepen bezitten switches.
Switches bezitten geen groepen.

## Sequence Rules
Voor sequence:
A → B → C
Geldig:
A
B
C
Generate:
- SEQUENCE_COMPLETED
Ongeldig:
A
A
Generate:
- SEQUENCE_RESET
Ongeldig:
A
C
Generate:
- SEQUENCE_RESET
Ongeldig:
A
B
A
Generate:
- SEQUENCE_RESET

## Mission Rules
Mission regels zijn alleen actief tijdens:
MISSION_ACTIVE
Generate:
- MISSION_PROGRESS_UPDATED
- MISSION_COMPLETED
- MISSION_FAILED

## Challenge Rules
Challenge regels zijn alleen actief tijdens:
CHALLENGE_ACTIVE
Generate:
- CHALLENGE_COMPLETED
- CHALLENGE_FAILED
State Flow:
MISSION_ACTIVE
↓
CHALLENGE_ACTIVE
↓
MISSION_ACTIVE
Challenge voltooiing of mislukking beëindigt nooit de missie.
Na afloop keert de state terug naar:
MISSION_ACTIVE

## Achievement Rules
Achievements zijn onafhankelijk van states.
Achievements blijven actief tijdens alle speltoestanden.
Achievements mogen gebaseerd zijn op:
- Switch hits
- Group completions
- Sequence completions
- Ordered target sequences
Voorbeelden:
- 100x POP_BUMPER
- 50x LEFT_ORBIT_SEQUENCE
- 25x UPPER_PLAYFIELD_GROUP
Achievement voortgang blijft behouden tussen spellen.
Generate:
- ACHIEVEMENT_PROGRESS_UPDATED
- ACHIEVEMENT_COMPLETED
- ACHIEVEMENT_RESET

## Isolation
Rules kennen geen:
- GPIO
- Multiplexers
- Relays
- Arduino
- Hardware details
Rules verwerken uitsluitend events.
