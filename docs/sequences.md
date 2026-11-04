# Sequences

## Doel
Sequences zijn verzamelingen van targets waarbij de volgorde belangrijk is.

## Eigenaarschap
Een Sequence bezit:
- Targets
Targets bezitten geen Sequences.

## Voltooiing
Voorbeeld:
A
↓
B
↓
C
Generate:
- SEQUENCE_COMPLETED

## Ongeldige Volgorde
A
A
Generate:
- SEQUENCE_RESET

## Reset
Na een foutieve stap wordt de sequence gereset.
Generate:
- SEQUENCE_RESET

## Reuse
Een target mag onderdeel zijn van meerdere Sequences.
Voorbeeld:
LEFT_ORBIT_ENTRY
Kan gebruikt worden in:
- LEFT_ORBIT_SEQUENCE
- RAMP_RETURN_SEQUENCE
- MISSION_ALPHA_SEQUENCE

## Voorbeeld
LEFT_ORBIT_SEQUENCE
Targets:
- LEFT_ORBIT_ENTRY
- LEFT_ORBIT_MIDDLE
- LEFT_ORBIT_EXIT
Geldig:
ENTRY
MIDDLE
EXIT
Result:

SEQUENCE_COMPLETED
