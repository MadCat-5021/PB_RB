# core/state_manager.py
- Replace ATTRACT_TIMEOUT line with ATTRACT_COMPLETED calback fromn the display manager


Launch procedure implemented: a countdown from 5 to 1 is followed by a random 0.8-2 second pause before 0. Launches in the next 5 seconds earn a separate bonus that decreases linearly from 5000 to 500 in 10-point steps; launches outside that window earn no launch bonus.

Shoot-again procedure implemented: the first launch of a turn and an extra-ball award each activate the shoot-again window, which expires after `SHOOT_AGAIN_TIMEOUT`.