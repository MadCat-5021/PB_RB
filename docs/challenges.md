# Challenges

## Doel
Challenges zijn optionele gameplaydoelen.
Challenges kunnen extra punten, rewards of voordelen opleveren.
Challenges zijn niet vereist voor het voltooien van een missie.

## Activatie
Challenges worden gestart door specifieke events.
Voorbeelden:
- GROUP_COMPLETED
- SEQUENCE_COMPLETED
Een challenge mag:
- Altijd beschikbaar zijn
- Alleen beschikbaar zijn tijdens specifieke missies

## State
Bij activatie:
MISSION_ACTIVE
↓
CHALLENGE_ACTIVE
Generate:
- CHALLENGE_STARTED

## Voltooiing
Bij behalen van alle challenge requirements:
Generate:
- CHALLENGE_COMPLETED
State:
CHALLENGE_ACTIVE
↓
MISSION_ACTIVE

## Mislukken
Bij niet behalen van de challenge requirements:
Generate:
- CHALLENGE_FAILED
State:
CHALLENGE_ACTIVE
↓
MISSION_ACTIVE
Mission voortgang blijft behouden.

## Challenge Types

### Single Target
Raak één target.

Voorbeeld:
- TIRE_1

## Group Challenge
Voltooi een group.
Voorbeeld:
- TOP_LANES_GROUP

## Sequence Challenge
Voltooi een sequence.
Voorbeeld:
- LEFT_ORBIT_SEQUENCE

## Repeat Challenge
Raak een target meerdere keren.
Voorbeeld:
LEFT_RAMP
Requirement:
10 Hits

## Timed Repeat Challenge
Raak een target meerdere keren binnen een tijdslimiet.
Voorbeeld:
POP_BUMPER
Requirement:
25 Hits
Time Limit:
20 Seconds

## Mixed Challenge
Combination van verschillende requirements.
Voorbeeld:
- LEFT_RAMP
- TOP_LANES_GROUP
- RIGHT_ORBIT_SEQUENCE

## Timed Challenges
Een challenge mag een tijdslimiet hebben.
Voorbeelden:
- 10 Seconds
- 30 Seconds
- 60 Seconds
Generate:
- CHALLENGE_TIMER_STARTED
- CHALLENGE_TIMER_EXPIRED

## Non-Timed Challenges
Een challenge mag zonder timer uitgevoerd worden.
De challenge blijft actief totdat:
- CHALLENGE_COMPLETED
- BALL_DRAINED

## Rewards
Challenges kunnen rewards geven.
Voorbeelden:
- Score Bonus
- Extra Ball
- Mission Progress
- Multiball Start
- Special Award

## Examples

### Quick Orbit
Trigger:
LEFT_RAMP_GROUP_COMPLETED
Requirement:
LEFT_ORBIT
Time Limit:
5 Seconds
Result:
CHALLENGE_COMPLETED

### Ramp Master
Trigger:
MISSION_3_ACTIVE
Requirement:
LEFT_RAMP
Hits Required:
10
Time Limit:
30 Seconds
Result:
CHALLENGE_COMPLETED

### Combo Challenge
Trigger:
RIGHT_ORBIT_SEQUENCE_COMPLETED
Requirement:
- LEFT_RAMP
- CENTER_RAMP
- RIGHT_RAMP
Result:
CHALLENGE_COMPLETED
