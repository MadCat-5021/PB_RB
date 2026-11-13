# Configuration

## Doel
Configuration bevat alle instelbare spelparameters.
Configuratie bepaalt gedrag zonder codewijzigingen.

## General
Configureerbaar:
- Game Name
- Version
- Free Play
- Max Players
- Balls Per Game

## Scoring
Configureerbaar:
- Target Scores
- Group Scores
- Sequence Scores
- Mission Bonuses
- Challenge Bonuses
- Achievement Bonuses

## Mission Multiplier
Configureerbaar:
Multiplier Levels:
- 1
- 2
- 3
- 5
- 8
- 10
Maximum Multiplier:
- 10

## Combo Scoring
Configureerbaar:
- Combo Enabled
- Combo Window
- Combo Base Score
- Combo Multiplier

## Groups
Per Group configureerbaar:
- Name
- Targets
- Score
- Reset Behaviour

## Sequences
Per Sequence configureerbaar:
- Name
- Targets
- Score
- Reset Behaviour

## Missions
Per Mission configureerbaar:
- Name
- Description
- Groups
- Sequences
- Completion Bonus
- Available Challenges

## Challenges
Per Challenge configureerbaar:
- Name
- Description
- Requirements
- Time Limit
- Reward

## Achievements
Per Achievement configureerbaar:
- Name
- Description
- Requirement Type
- Requirement Value
- Reward

## Audio
Configureerbaar:
- Master Volume
- Music Volume
- Effect Volume
- Voice Volume

## Display
Configureerbaar:
- Brightness
- Attract Mode Timeout
- Score Display Options
- Animation Options

## Coils
Configureerbaar:
- Enable At Startup
- Admin Switch Required

## Credits
Configureerbaar:
- Credits Per Coin
- Max Credits
- Free Play

## Shoot Again
Configureerbaar:
- Shoot Again Timeout

## Tilting
Configureerbaar:
- Tilt Warnings
- Tilt Sensitivity
- Slam Tilt Enabled

## Persistence
Opgeslagen configuratie moet behouden blijven tussen herstarts.
Configuratiewijzigingen worden opgeslagen na:
- CONFIG_UPDATED
- SYSTEM_SHUTDOWN

## Defaults
Bij ontbreken van configuratie:
- Gebruik standaardwaarden
- Start systeem normaal op

## Validation
Alle configuratiewaarden moeten worden gevalideerd bij laden.
Ongeldige waarden worden vervangen door standaardwaarden.
