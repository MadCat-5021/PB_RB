# Scoring

## Doel

## Base Scores
- Switches
- Groups
- Sequences

## Mission Scores
- Mission Completion

## Challenge Scores
- Challenge Completion

## Achievement Scores
- Achievement Completion

## Combo Scoring
Combo Scoring beloont herhaalde hits binnen een bepaald tijdsvenster.
Combo Scoring kan gebruikt worden door:
- Targets
- Sequences

## Combo Window
Iedere combo definieert een eigen time window.
Voorbeeld:
5 seconds

## Valid Repeat
Dezelfde target of sequence wordt opnieuw voltooid binnen het combo window.
Andere targets of sequences mogen tussendoor geraakt worden.

## Target Combo Example
Target:
LEFT_ORBIT
Base Score:
1000
Hits:
LEFT_ORBIT
Combo Count = 1
Awarded Score:
1000
LEFT_ORBIT within 5 seconds
Combo Count = 2
Awarded Score:
2000
LEFT_ORBIT within 5 seconds
Combo Count = 3
Awarded Score:
3000

## Sequence Combo Example
Sequence:
LEFT_ORBIT_SEQUENCE
Base Score:
5000
Completion 1
Combo Count = 1
Awarded Score:
5000
Completion 2 within 5 seconds
Combo Count = 2
Awarded Score:
10000

## Combo Reset
Een combo wordt gereset wanneer:
- Combo Window expires
Na reset:
Combo Count = 1

## Multiplier Interaction
Combo Scoring wordt berekend vóór eventuele Mission Multiplier toepassing.
Als de combo afkomstig is van een Target of Sequence:
Mission Multiplier wordt niet toegepast.
Als de combo afkomstig is van een Group:
Mission Multiplier wordt wel toegepast volgens de Group Scoring regels.## Mission Multiplier
1
2
3
5
8
10

## Multiplier Application
Score = Score + Base Score × Bonus Multiplier
Bonus = Bonus + (Bonus x Bonus Multipier
## Ball Bonus

## End Of Ball

## Extra Ball

## Game Completed
