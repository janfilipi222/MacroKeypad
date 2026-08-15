from application.use_cases.get_profiles_use_case import GetProfilesUseCase

from pathlib import Path

from PySide6.QtCore import QObject

from domain.entities.profile import Profile
from domain.entities.page import Page


class MainViewModel(QObject):
    def __init__(
            self, 
            get_profiles: GetProfilesUseCase
        ):
        super().__init__()
        self._get_profiles = get_profiles

        self.curr_btn = [0, 0]
        self.curr_profile = Profile(
            None,
            "Test Profile",
            None,
            None
        )

        self.curr_page = Page(
            None,
            "default page",
            None
        )

        
        self.curr_icon_paths = [
            [Path("c:/Users/janfi/AppData/Local/CGM/MacroKeypadBackgroundApp/icons/default.png")] * 4 for _ in range(6)
        ]


        self._assets_path = (
            Path(__file__).resolve().parents[2] / "assets"
        )

        print("path", self._assets_path)

        self.system_icons = self._assets_path


    def get_all_profiles(self):
        return ["profile 1", "profile 2", "profile 3"]


    def get_all_pages(self):
        return ["page 1", "page 2", "page 3"]