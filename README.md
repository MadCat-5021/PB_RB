# PB_RB
A complete pinball system including hardware based of a Raspberry Pi 4B 8Gb

# Targets
The system will evaluate all events based on switches in the machine
  - Play sounds
  - Drive a display
  - Background(s)
  - Foregoundmask(s)
  - Images
  - GIF's
  - Video's
  - JSON communication over USB with a Arduino Giga

# Hardware
Planned Hardware
-  1x    Raspberry Pi 4B 8Gb
- 1x    Arduino Giga 1R WiFi
- 3x    CD74HC4067 multiplexer
- 48+   Switches (Tactile, micro, leaf, induction, custom built)
- 3x    12V Hesschen Coils
- 3x    Pop bumper assemblies
- 2x    Flipper assemblies
- 2x    Slingshot assemblies
- 150x  WS2811/WS2812 LED RGB

# Software architecture
  - Input scanner
  - Rule engine
  - Audiomanager
  - Displaymanager
  - Arduinomanager
  - Arduinosketch lightshow

  # Status
  - Hardware Cabinet in progress, playfield ready
  - Software Version 20 where all logic is transferred to the Raspberry, Giga is lightshow only
  - Designfase
