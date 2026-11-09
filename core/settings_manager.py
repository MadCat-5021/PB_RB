# core/settings_manager.py

import json
from pathlib import Path
from content.settings import FACTORY_DEFAULTS

class SettingsManager:
    def __init__(self):
        self.settings = FACTORY_DEFAULTS.copy()
        config_file = Path(
            "config/settings.json"
        )
        if config_file.exists():
            with open(
                config_file,
                "r",
                encoding="utf-8"
            ) as file:
                custom_settings = json.load(
                    file
                )
            self.settings.update(
                custom_settings
            )

    def get(
        self,
        key
    ):
        return self.settings[key]

    def set(
        self,
        key,
        value
    ):
        self.settings[key] = value

    def save(self):
        with open(
            "config/settings.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.settings,
                file,
                indent=4
            )