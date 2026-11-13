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
1000 * bonus Multiplier
LEFT_ORBIT within 5 seconds
Combo Count = 2
Awarded Score:
2000 * bonus Multiplier
LEFT_ORBIT within 5 seconds
Combo Count = 3
Awarded Score:
3000 * bonus Multiplier

## Sequence Combo Example
Sequence:
LEFT_ORBIT_SEQUENCE
Base Score:
5000
Completion 1
Combo Count = 1
Awarded Score:
5000 * bonus Multiplier
Completion 2 within 5 seconds
Combo Count = 2
Awarded Score:
10000 * bonus Multiplier

## Combo Reset
Een combo wordt gereset wanneer:
- Combo Window expires
Na reset:
Combo Count = 1

## Multiplier Interaction
Combo Scoring wordt direct toegepast op de score
Als de combo afkomstig is van een Target of Sequence:
- Counter word toegepast
- Bonus Multiplier wordt toegepast.

## Bonus Multiplier
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

The launch sequence awards a separate bonus, not regular score:
- The countdown runs from 5 to 1, then waits a random 0.8 to 2 seconds before 0.
- Launches before 0 receive no bonus.
- Launches from 0 through 5 seconds after 0 receive a bonus decreasing linearly
  from 5000 to 500 points in 10-point steps.
- Launches later than 5 seconds after 0 receive no bonus.

## End Of Ball

When the ball drains and no extra ball or shoot again was rewarded

## Game Completed
