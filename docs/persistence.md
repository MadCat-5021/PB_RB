# Persistence

## Doel
Persistence slaat data op tussen herstarts van het systeem.

## Persistent Data
- Achievements
- Achievement Progress
- Highscores
- Credits
- Settings
- Audit Counters

## Non Persistent Data
- Active Ball
- Current Mission
- Current Challenge
- Current Multiplier
- Current Score

## Save Triggers
- ACHIEVEMENT_COMPLETED
- CREDIT_ADDED
- SETTINGS_UPDATED
- HIGHSCORE_UPDATED
- SYSTEM_SHUTDOWN

## Startup
Bij SYSTEM_START wordt opgeslagen data geladen.

## Shutdown
Bij SYSTEM_SHUTDOWN wordt alle gewijzigde data opgeslagen.
