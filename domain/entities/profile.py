from dataclasses import dataclass
from domain.entities.macro_action import MacroAction
from domain.entities.page import Page

@dataclass
class Profile:
    id: str
    name: str
    application: str | None
    pages: list[Page]



