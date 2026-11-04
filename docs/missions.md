# Missions

## Doel
Missions vormen de hoofdprogressie van het spel.
Elke game start bij Mission 1.
Missions worden in vaste volgorde gespeeld.

## Flow
MISSION_1
↓
MISSION_2
↓
MISSION_3
↓
...
↓
FINAL_MISSION

## State
Tijdens een actieve missie:
MISSION_ACTIVE
Er is altijd exact één actieve missie.

## Eigenaarschap
Een mission bezit:
- Groups
- Sequences
- Mission Rules
Missions verwijzen naar bestaande Groups en Sequences.
Missions bezitten geen switches rechtstreeks.

## Activatie
Bij het starten van een spel wordt Mission 1 geactiveerd.
Generate:
- MISSION_STARTED

## Progressie
Mission voortgang wordt bijgewerkt door:
- GROUP_COMPLETED
- SEQUENCE_COMPLETED
- Mission specifieke events
Generate:
- MISSION_PROGRESS_UPDATED

## Voltooiing
Wanneer alle mission requirements zijn behaald:
Generate:
- MISSION_COMPLETED
De volgende missie wordt automatisch gestart.
Generate:
- MISSION_STARTED

## Mislukken
Missions kunnen niet mislukken.

Mission voortgang blijft actief totdat de missie voltooid is.

## Challenge Activatie
Een missie mag een challenge starten.
State Flow:
MISSION_ACTIVE
↓
CHALLENGE_ACTIVE

## Challenge Return
Bij voltooiing van een challenge:
MISSION_ACTIVE
↓
CHALLENGE_ACTIVE
↓
MISSION_ACTIVE
Bij mislukking van een challenge:
MISSION_ACTIVE
↓
CHALLENGE_ACTIVE
↓
MISSION_ACTIVE
Mission voortgang blijft behouden.

## Bonus Multiplier
Bij het voltooien van meerdere missies tijdens dezelfde bal wordt de Bonus Multiplier verhoogd.
Bonus Levels:
1>2>3>5>8>10
Na level 10 blijft de multiplier op 10.
Generate:
- BONUS_MULTIPLIER_CHANGED

## Multiplier Reset
Bij:
- BALL_DRAINED
Wordt de Bonus Multiplier teruggezet naar:
1
Generate:
- BONUS_MULTIPLIER_CHANGED

## Bonus Example
Start Ball:
Multiplier = 1
MISSION_1_COMPLETED
Multiplier = 2
MISSION_2_COMPLETED
Multiplier = 3
MISSION_3_COMPLETED
Multiplier = 5
MISSION_4_COMPLETED
Multiplier = 8
MISSION_5_COMPLETED
Multiplier = 10
BALL_DRAINED
Multiplier = 1

## Mission Examples

### MISSION_1
Requirements:
- LEFT_ORBIT_SEQUENCE

Completion:
- MISSION_COMPLETED
- MISSION_STARTED(MISSION_2)

### MISSION_2
Requirements:
- RAMP_RIGHT

Completion:
- MISSION_COMPLETED
- MISSION_STARTED(MISSION_3)

## Final Mission
Na voltooiing van de laatste missie:

Generate:
- MISSION_COMPLETED
- GAME_COMPLETED
