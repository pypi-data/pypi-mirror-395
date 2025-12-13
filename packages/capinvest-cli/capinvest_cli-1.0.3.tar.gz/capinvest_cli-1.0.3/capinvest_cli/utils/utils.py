"""CapInvest Platform CLI utilities."""

import json
from pathlib import Path

HOME_DIRECTORY = Path.home()
CAPINVEST_PLATFORM_DIRECTORY = Path(HOME_DIRECTORY, ".capinvest_platform")
SYSTEM_SETTINGS_PATH = Path(CAPINVEST_PLATFORM_DIRECTORY, "system_settings.json")


def change_logging_sub_app() -> str:
    """Build CapInvest Platform setting files."""
    with open(SYSTEM_SETTINGS_PATH) as file:
        system_settings = json.load(file)

    initial_logging_sub_app = system_settings.get("logging_sub_app", "")

    system_settings["logging_sub_app"] = "cli"

    with open(SYSTEM_SETTINGS_PATH, "w") as file:
        json.dump(system_settings, file, indent=4)

    return initial_logging_sub_app


def reset_logging_sub_app(initial_logging_sub_app: str):
    """Reset CapInvest Platform setting files."""
    with open(SYSTEM_SETTINGS_PATH) as file:
        system_settings = json.load(file)

    system_settings["logging_sub_app"] = initial_logging_sub_app

    with open(SYSTEM_SETTINGS_PATH, "w") as file:
        json.dump(system_settings, file, indent=4)
