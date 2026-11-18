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

## Content

`content/challenges.py` bevat `CHALLENGES`. Iedere challenge heeft:

- `name`, `display_name` en `description`
- `missions`: missie-IDs waarin de challenge beschikbaar is; een lege lijst
  betekent dat de challenge in iedere missie beschikbaar is
- `trigger`: de startconditie:
  - `target_hit_multiple`: start bij iedere `every`-de hit op `target`;
    `chance` is de kans (0.0-1.0) dat de challenge dan start
  - `random`: trek bij ieder `target_hit` een kans (`chance`, 0.0-1.0)
- `requirements`: doelen die allemaal voltooid moeten worden. `targets` mogen
  strings zijn voor één hit, of objecten zoals
  `{"name": "ORBIT_LEFT_REAR", "hits": 5}` voor herhaalde hits. `groups` en
  `sequences` verwijzen naar bestaande content-IDs
- `time_limit_seconds`: positieve tijdslimiet in seconden, of `None` voor geen
  timer
- `score`: scorebonus bij succesvolle voltooiing
- `assets`: `image`, `sound` en `background_track`; `None` betekent dat er
  momenteel geen asset is ingesteld. De achtergrondtrack is bedoeld als
  tijdelijke override en hoort na afloop van de challenge te worden hersteld.

De twee entries in `CHALLENGES` zijn voorbeelden met instelbare kansen,
requirements, tijden en bonussen. Deze configuratie legt parameters vast; de
challenge-runtime die triggers, timers en assets uitvoert is nog niet
geïmplementeerd.

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
