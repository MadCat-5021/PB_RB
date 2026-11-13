# core/state_manager.py
- Replace ATTRACT_TIMEOUT line with ATTRACT_COMPLETED calback fromn the display manager


Next step is to create the launch procedure (when the machine has one). The Lauch sequence consists of a countdown (later with lights and sound) from 5 to 1, from 1 to 0 is a random period between 0.8 and 2 seconds. If the ball launches before 0, no bonus, if the ball launches after 5 seconds, too slow and no bonus. When te ball is launched anywhere between 0 and 5 seconds after countdown, the player get's a bonus (not score but bonus) decreasing from 5000 to 500 in increments of 10 linear to the reaction time