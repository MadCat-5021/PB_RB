Rapsberry
  Threads
  Inputscanner
    Tasks:
      Polling all connections
      Debounce
      Checking for held switches
    Events:
      Pressed
      Released
      Held
  Rule Engine
  Game engine, evaluate switches and events accordinbgly
  AudioManager
    Tasks:
      Background music
      Soundeffects
      Multiple channels
  Displaymanager
    Tasks:
      Animated background
      Foreground mask
      Images
      Videos
      GIF's
      Textlayer
  Arduinomanager
    Tasks:
      JSON to Arduino
Flows
InputScanner>InputQeue>RuleEngine>AudioQeue>DisplayQeue>ArdinoQeue>Managers
Arduino
  Tasks:
  Arranging lights, lightshows
Design Philosophy
The system is event-driven.
Hardware inputs generate events.
Events are evaluated by the Rule Engine.
The Rule Engine never directly controls hardware.
The Rule Engine generates commands for specialized managers:
AudioManager
DisplayManager
ArduinoManager
Managers execute commands asynchronously.
Communication between subsystems uses queues.
