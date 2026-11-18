from pathlib import Path


class AudioManager:
    CHANNEL_COUNT = 16
    MUSIC_CHANNEL_INDEX = 0
    EFFECT_CHANNEL_INDICES = tuple(range(1, CHANNEL_COUNT))
    VOLUME_SCALE = 10
    AUDIO_DIRECTORY = Path("assets/audio")
    SUPPORTED_SOUND_FORMATS = frozenset(
        {".wav", ".ogg", ".mp3", ".flac"}
    )

    def __init__(self, settings, mixer=None, audio_dir=AUDIO_DIRECTORY):
        if mixer is None:
            import pygame

            mixer = pygame.mixer

        self.settings = settings
        self.mixer = mixer
        if self.mixer.get_init() is None:
            self.mixer.init()
        self.mixer.set_num_channels(self.CHANNEL_COUNT)
        self.mixer.set_reserved(1)

        self.music_channel = self.mixer.Channel(self.MUSIC_CHANNEL_INDEX)
        self.effect_channels = {
            index: self.mixer.Channel(index)
            for index in self.EFFECT_CHANNEL_INDICES
        }
        self.sounds = {}
        self.effect_sounds = {}
        self.effect_play_order = {}
        self.next_play_order = 0

        self.set_effects_volume(self.settings.get("VOLUME_EFFECTS"))
        self.set_music_volume(self.settings.get("VOLUME_MUSIC"))
        self.preload_sounds(audio_dir)

    def preload_sounds(self, audio_dir=AUDIO_DIRECTORY):
        audio_dir = Path(audio_dir).expanduser().resolve()
        if not audio_dir.is_dir():
            raise FileNotFoundError(
                f"Audio asset directory does not exist: {audio_dir}"
            )

        loaded_count = 0
        audio_files = sorted(
            path
            for path in audio_dir.rglob("*")
            if (
                path.is_file()
                and path.suffix.lower() in self.SUPPORTED_SOUND_FORMATS
            )
        )
        for sound_path in audio_files:
            sound_key = self._sound_key(sound_path)
            if sound_key not in self.sounds:
                self._get_sound(sound_path)
                loaded_count += 1

        print(f"AUDIO: Preloaded {loaded_count} sounds from {audio_dir}")
        return loaded_count

    def play_effect(self, sound_path):
        sound_key, sound = self._get_sound(sound_path)
        same_sound_channel = next(
            (
                index
                for index, channel in self.effect_channels.items()
                if (
                    channel.get_busy()
                    and self.effect_sounds.get(index) == sound_key
                )
            ),
            None,
        )
        if same_sound_channel is not None:
            channel_index = same_sound_channel
            self.effect_channels[channel_index].stop()
        else:
            channel_index = next(
                (
                    index
                    for index, channel in self.effect_channels.items()
                    if not channel.get_busy()
                ),
                None,
            )
            if channel_index is None:
                if not self.effect_play_order:
                    raise RuntimeError(
                        "All effect channels are busy outside AudioManager"
                    )
                channel_index = min(
                    self.effect_play_order,
                    key=self.effect_play_order.get,
                )
                previous_sound = self.effect_sounds[channel_index]
                print(
                    "AUDIO: Replacing oldest effect "
                    f"'{previous_sound}'"
                )
                self.effect_channels[channel_index].stop()

        self.effect_channels[channel_index].play(sound)
        self.effect_sounds[channel_index] = sound_key
        self._mark_effect_started(channel_index)
        return channel_index

    def stop_effect(self, sound_path=None):
        sound_key = (
            None if sound_path is None else self._sound_key(sound_path)
        )
        for index, channel in self.effect_channels.items():
            if sound_key is None or self.effect_sounds.get(index) == sound_key:
                channel.stop()
                self.effect_sounds.pop(index, None)
                self.effect_play_order.pop(index, None)

    def play_music(self, sound_path, loops=-1):
        _, sound = self._get_sound(sound_path)
        self.music_channel.play(sound, loops=loops)

    def stop_music(self):
        self.music_channel.stop()

    def stop_all(self):
        self.stop_music()
        self.stop_effect()

    def set_effects_volume(self, volume):
        volume = self._validate_volume(volume)
        self.settings.set("VOLUME_EFFECTS", volume)
        mixer_volume = volume / self.VOLUME_SCALE
        for channel in self.effect_channels.values():
            channel.set_volume(mixer_volume)

    def set_music_volume(self, volume):
        volume = self._validate_volume(volume)
        self.settings.set("VOLUME_MUSIC", volume)
        self.music_channel.set_volume(volume / self.VOLUME_SCALE)

    def save_settings(self):
        self.settings.save()

    def _get_sound(self, sound_path):
        sound_key = self._sound_key(sound_path)
        if sound_key not in self.sounds:
            self.sounds[sound_key] = self.mixer.Sound(sound_key)
        return sound_key, self.sounds[sound_key]

    @staticmethod
    def _sound_key(sound_path):
        if not isinstance(sound_path, (str, Path)) or not sound_path:
            raise ValueError("A sound path must be a non-empty path")
        return str(Path(sound_path).expanduser().resolve())

    @classmethod
    def _validate_volume(cls, volume):
        if (
            isinstance(volume, bool)
            or not isinstance(volume, int)
            or not 0 <= volume <= cls.VOLUME_SCALE
        ):
            raise ValueError("Volume must be an integer between 0 and 10")
        return volume

    def _mark_effect_started(self, channel_index):
        self.next_play_order += 1
        self.effect_play_order[channel_index] = self.next_play_order