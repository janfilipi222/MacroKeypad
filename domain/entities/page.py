from dataclasses import dataclass
from domain.entities.macro_action import MacroAction

@dataclass
class Page:
    id: str
    name: str
    actions: list[list[MacroAction]]