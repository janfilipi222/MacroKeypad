
from pathlib import Path

from PySide6.QtCore import QObject

from domain.entities.profile import Profile
from domain.entities.page import Page
from domain.entities.macro_action import MacroAction
from infrastructure.repositories.json_profile_repository import JsonProfileRepository

class MainViewModel(QObject):
    def __init__(
            self, 
            repo: JsonProfileRepository,
            app_data: Path
        ):
        super().__init__()
        self._repo = repo
        self._app_data = app_data

        self._default_icon = self._app_data / "icons" / "default.png"

        self.curr_icon = [0, 0]
        self.curr_profile: Profile = self._repo.load_profile("default")
        self.curr_page: Page = self.get_page_by_id("default")
        self.curr_page_id = "default"
        self.curr_icon_paths = self._set_curr_icon_paths()
        self.curr_action: MacroAction = self.curr_page.actions[self.curr_icon[0]][self.curr_icon[1]]


        self._all_profiles: dict = {}


        self._assets_path = (
            Path(__file__).resolve().parents[2] / "assets"
        )

        self.system_icons = self._assets_path


    def save_curr(self):
        print("saving")
        self._repo.save_profile(self.curr_profile)


    def select_new_action(self, id: int):
        action = self.curr_page.actions[self.curr_icon[0]][self.curr_icon[1]]
        if action == None:
            if id == 4:
                return
            action = MacroAction(None, None, {})

        match id:
            case 0: action.type = "keybind"
            case 1: action.type = "program"
            case 2: action.type = "script"
            case 3: action.type = "system"
            case 4: action = None

        self.curr_page.actions[self.curr_icon[0]][self.curr_icon[1]] = action

    def select_new_params(self, param: str):
        action = self.curr_page.actions[self.curr_icon[0]][self.curr_icon[1]]
        if action == None:
            return

        type = action.type
        match type:
            case "keybind": action.params["keys"] = param
            case "program": action.params["path"] = param
            case "script": action.params["name"] = param
            case "system": action.params["action"] = param

    def select_new_icon_path(self, path):
        action = self.curr_page.actions[self.curr_icon[0]][self.curr_icon[1]]
        if action == None:
            return
        action.icon = path


    def select_new_profile(self, profile: str):
        id = next((d["id"] for d in self._all_profiles if d["name"] == profile))
        self.curr_profile = self._repo.load_profile(id)
        self.curr_page_id = "default"
        self.curr_page = self.get_page_by_id(self.curr_page_id)
        self.curr_icon = [0, 0]
        self.curr_icon_paths = self._set_curr_icon_paths()

    def select_new_page(self, page: str):
        id = next((p.id for p in self.curr_profile.pages if p.name == page), None)
        self.curr_page_id = id
        self.curr_page = self.get_page_by_id(self.curr_page_id)
        self.curr_icon = [0, 0]
        self.curr_icon_paths = self._set_curr_icon_paths()


    def select_new_icon(self, row: int, col: int):
        self.curr_icon = [row, col]
        self.curr_action = self.curr_page.actions[self.curr_icon[0]][self.curr_icon[1]]

    def get_curr_icon_paths(self):
        self.curr_icon_paths = self._set_curr_icon_paths()
        return self.curr_icon_paths

   
    def _set_curr_icon_paths(self):
        icon_path = self._app_data / "icons" / self.curr_profile.id
        paths = []
        for row in self.curr_page.actions:
            r = []
            for action in row:
                if action == None or action.icon == None:
                    r.append(self._default_icon)
                else:
                    r.append(icon_path / action.icon)
            paths.append(r)

        print("paths: ", paths)
        return paths



    def get_all_profiles(self) -> list[str]:
        profiles = self._repo.load_all_profiles()
        self._all_profiles = profiles
        return [p['name'] for p in profiles]


    def get_all_pages(self):

        return [p.name for p in self.curr_profile.pages]


    def get_page_list_id_by_id(self, page_id: str) -> int | None:
        if not self.curr_profile:
            return None
        for i, page in enumerate(self.curr_profile.pages):
            if page.id == page_id:
                return i
        return None



    def get_page_by_id(self, page_id: str) -> Page | None:
        if not self.curr_profile:
            return None
        for page in self.curr_profile.pages:
            if page.id == page_id:
                return page
        return None
