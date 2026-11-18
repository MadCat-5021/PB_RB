# Architecture

## Threads

### InputScanner

Tasks:

- Read 48 switches
- Apply lockout debounce
- Generate input events

Events:

- SWITCH_PRESSED
- SWITCH_RELEASED
- SWITCH_HELD

### RuleEngine

Evaluates events within the current game context.

The RuleEngine updates the Game Model and generates commands for output managers.

### AudioManager

`AudioManager(settings, mixer=None, audio_dir="assets/audio")` uses
`pygame.mixer` by default. During `Game.boot()`, it initializes the mixer if
needed and preloads all `.wav`, `.ogg`, `.mp3` and `.flac` files under
`assets/audio` (including subdirectories) without playing them. It reserves 16
channels:

- `CHANNEL_COUNT`: total channels (`16`)
- `MUSIC_CHANNEL_INDEX`: dedicated music channel (`0`)
- `EFFECT_CHANNEL_INDICES`: effect channels (`1` through `15`)
- `VOLUME_SCALE`: maximum configured volume (`10`)

Public methods:

- `play_effect(sound_path)`: play an effect and return its channel index. If
  that same sound is already playing, restart it on its current channel. If all
  effect channels are busy, stop the oldest effect and use its channel.
- `preload_sounds(audio_dir="assets/audio")`: load supported audio files from
  the directory and its subdirectories; returns the number of newly loaded
  sounds. A missing directory raises `FileNotFoundError`.
- `stop_effect(sound_path=None)`: stop the specified effect, or all effects
  when no path is given.
- `play_music(sound_path, loops=-1)`: play music on the dedicated music
  channel. `loops=-1` repeats indefinitely; `loops=0` plays once.
- `stop_music()`: stop playback on the music channel.
- `stop_all()`: stop music and all effects.
- `set_effects_volume(volume)` and `set_music_volume(volume)`: immediately
  apply a volume from `0` to `10`, in integer steps, and update the setting.
- `save_settings()`: persist the settings through `SettingsManager`.

The corresponding settings are `VOLUME_EFFECTS` and `VOLUME_MUSIC`, both
defaulting to `5` in `content/settings.py`. For example:

```python
audio_manager.play_effect("assets/audio/target_hit.wav")
audio_manager.play_music("assets/audio/background.ogg")
audio_manager.set_effects_volume(7)
audio_manager.save_settings()
```

Sound paths are loaded and cached by the manager. Invalid volume values raise
`ValueError`; playback and file-loading errors from the mixer are not hidden.
The manager currently exposes these methods for direct calls; it is not yet
subscribed to audio request events.

### DisplayManager

Tasks:

- Animated backgrounds
- Foreground masks
- Images
- Videos
- GIFs
- Text layers

### ArduinoManager

Tasks:

- Send JSON messages
- Receive status information

## Event Flow

InputScanner
↓
InputQueue
↓
RuleEngine
↓
AudioQueue
DisplayQueue
ArduinoQueue
↓
Managers

# Design Philosophy

The system is event-driven.

Hardware inputs generate events.

Events are evaluated by the RuleEngine.

The RuleEngine updates the Game Model.

The RuleEngine never directly controls hardware.

The RuleEngine generates commands for specialized managers:

- AudioManager
- DisplayManager
- ArduinoManager

Managers execute commands asynchronously.

Communication between subsystems uses queues.
