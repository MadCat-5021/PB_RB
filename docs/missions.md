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
- Requirements die verwijzen naar Targets, Groups en Sequences
- Mission Rules
Missions verwijzen naar bestaande content; targets, groups en sequences blijven
zelf eigenaar van hun switches.

## Content

`content/missions.py` bevat de lijst `MISSIONS`. De volgorde in deze lijst is de
vaste speelvolgorde. Elke missie heeft:

- `name`: unieke interne ID, bijvoorbeeld `MISSION_1`
- `working_title`: tijdelijke/tentatieve missienaam
- `description`: omschrijving voor ontwerp en later eventueel de speler
- `requirements`: lijsten met `targets`, `groups` en `sequences`; alle opgegeven
  requirements moeten voltooid zijn
- `score`: scorebonus voor het voltooien van de missie
- `challenges`: optionele IDs van missiegebonden challenges; challenges zijn
  niet vereist voor missievoltooiing
- `assets`: optionele `image`, `sound` en `text` voor `start`, `during` en
  `completion`. `during` is een lijst voor cues die later aan voortgangsmomenten
  gekoppeld kunnen worden. Gebruik `None` als er nog geen asset is ingesteld.

De score is een missiebonus; `0` betekent dat een missie geen scorebonus geeft.
De waarden in `MISSIONS` zijn content en kunnen per missie worden aangepast.

## Activatie
Bij het starten van een spel wordt Mission 1 geactiveerd.
Generate:
- MISSION_STARTED

## Progressie
Mission voortgang wordt bijgewerkt door:
- SWITCH_PRESSED voor een vereist target
- GROUP_COMPLETED
- SEQUENCE_COMPLETED
- Mission specifieke events
Generate:
- MISSION_PROGRESS_UPDATED

De requirements in `content/missions.py` worden allemaal bijgehouden; pas
wanneer ze allemaal voltooid zijn, slaagt de missie.

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
- ORBIT_LONG

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
