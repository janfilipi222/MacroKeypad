from dataclasses import dataclass
from enum import Enum


class MacroActionType(Enum):
    KEYBIND = "keybind"
    PROGRAM = "program"
    SCRIPT = "script"
    SYSTEM = "system"


@dataclass
class MacroAction:
    type: MacroActionType
    icon: str = None
    params: dict = None