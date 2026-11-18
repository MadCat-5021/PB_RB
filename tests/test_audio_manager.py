import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from audio.audio_manager import AudioManager


class Settings:
    def __init__(self):
        self.values = {
            "VOLUME_EFFECTS": 5,
            "VOLUME_MUSIC": 5,
        }
        self.saved = False

    def get(self, name):
        return self.values[name]

    def set(self, name, value):
        self.values[name] = value

    def save(self):
        self.saved = True


class FakeSound:
    def __init__(self, path):
        self.path = path


class FakeChannel:
    def __init__(self, index):
        self.index = index
        self.sound = None
        self.busy = False
        self.volume = None
        self.play_calls = []
        self.stop_calls = 0

    def get_busy(self):
        return self.busy

    def play(self, sound, loops=0):
        self.sound = sound
        self.busy = True
        self.play_calls.append((sound, loops))

    def stop(self):
        self.busy = False
        self.stop_calls += 1

    def set_volume(self, volume):
        self.volume = volume


class FakeMixer:
    def __init__(self):
        self.channels = {}
        self.channel_count = None
        self.reserved = None
        self.loaded_sounds = []

    def get_init(self):
        return (44100, -16, 2)

    def init(self):
        raise AssertionError("Initialized an already initialized mixer")

    def set_num_channels(self, count):
        self.channel_count = count

    def set_reserved(self, count):
        self.reserved = count

    def Channel(self, index):
        return self.channels.setdefault(index, FakeChannel(index))

    def Sound(self, path):
        self.loaded_sounds.append(path)
        return FakeSound(path)


class AudioManagerTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.mixer = FakeMixer()
        self.audio_directory = TemporaryDirectory()
        self.manager = AudioManager(
            self.settings,
            mixer=self.mixer,
            audio_dir=self.audio_directory.name,
        )

    def tearDown(self):
        self.audio_directory.cleanup()

    def test_reserves_one_music_and_fifteen_effect_channels(self):
        self.assertEqual(self.mixer.channel_count, 16)
        self.assertEqual(self.mixer.reserved, 1)
        self.assertEqual(self.manager.music_channel.index, 0)
        self.assertEqual(len(self.manager.effect_channels), 15)
        self.assertNotIn(0, self.manager.effect_channels)

    def test_replaying_active_effect_restarts_it_in_its_channel(self):
        first_channel = self.manager.play_effect("sounds/hit.wav")
        second_channel = self.manager.play_effect("sounds/hit.wav")

        self.assertEqual(first_channel, second_channel)
        self.assertEqual(len(self.mixer.channels[first_channel].play_calls), 2)
        self.assertEqual(self.mixer.channels[first_channel].stop_calls, 1)
        self.assertEqual(
            sum(channel.busy for channel in self.manager.effect_channels.values()),
            1,
        )

    def test_full_effect_pool_replaces_oldest_effect(self):
        channel_indices = [
            self.manager.play_effect(f"sounds/effect-{index}.wav")
            for index in range(15)
        ]

        replacement = self.manager.play_effect("sounds/new-effect.wav")

        self.assertEqual(replacement, channel_indices[0])
        self.assertEqual(self.mixer.channels[replacement].stop_calls, 1)
        self.assertEqual(len(self.manager.effect_sounds), 15)

    def test_music_and_effects_have_independent_volume_and_stop_controls(self):
        self.manager.set_effects_volume(8)
        self.manager.set_music_volume(3)
        effect_channel = self.manager.play_effect("sounds/hit.wav")
        self.manager.play_music("sounds/theme.ogg")

        self.assertEqual(self.settings.get("VOLUME_EFFECTS"), 8)
        self.assertEqual(self.settings.get("VOLUME_MUSIC"), 3)
        self.assertEqual(self.manager.effect_channels[effect_channel].volume, 0.8)
        self.assertEqual(self.manager.music_channel.volume, 0.3)

        self.manager.stop_music()
        self.manager.stop_effect("sounds/hit.wav")

        self.assertFalse(self.manager.music_channel.busy)
        self.assertFalse(self.manager.effect_channels[effect_channel].busy)

    def test_volume_accepts_only_integer_steps_from_zero_to_ten(self):
        for invalid_volume in (-1, 11, 1.5, True):
            with self.subTest(volume=invalid_volume):
                with self.assertRaises(ValueError):
                    self.manager.set_music_volume(invalid_volume)

    def test_volume_settings_can_be_saved(self):
        self.manager.set_effects_volume(0)
        self.manager.set_music_volume(10)

        self.manager.save_settings()

        self.assertTrue(self.settings.saved)
        self.assertEqual(self.settings.values["VOLUME_EFFECTS"], 0)
        self.assertEqual(self.settings.values["VOLUME_MUSIC"], 10)

    def test_preloads_supported_sounds_recursively_without_playing(self):
        audio_root = Path(self.audio_directory.name)
        (audio_root / "effects").mkdir()
        sound_files = [
            audio_root / "effects" / "hit.wav",
            audio_root / "music.ogg",
        ]
        for sound_file in sound_files:
            sound_file.touch()
        (audio_root / "notes.txt").touch()

        loaded_count = self.manager.preload_sounds(audio_root)

        self.assertEqual(loaded_count, 2)
        self.assertEqual(
            set(self.mixer.loaded_sounds),
            {str(path.resolve()) for path in sound_files},
        )
        self.assertFalse(
            any(channel.busy for channel in self.mixer.channels.values())
        )

    def test_preload_does_not_reload_sounds_already_cached(self):
        audio_root = Path(self.audio_directory.name)
        sound_file = audio_root / "hit.wav"
        sound_file.touch()

        self.assertEqual(self.manager.preload_sounds(audio_root), 1)
        self.assertEqual(self.manager.preload_sounds(audio_root), 0)
        self.assertEqual(len(self.mixer.loaded_sounds), 1)

    def test_preload_requires_an_existing_audio_directory(self):
        missing_directory = Path(self.audio_directory.name) / "missing"

        with self.assertRaises(FileNotFoundError):
            self.manager.preload_sounds(missing_directory)


if __name__ == "__main__":
    unittest.main()
