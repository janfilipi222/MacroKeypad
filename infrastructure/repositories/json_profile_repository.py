from domain.repositories.profile_repository import ProfileRepository
from domain.entities.profile import Profile
from domain.entities.macro_action import MacroAction
import json
from pathlib import Path
from dataclasses import asdict
from domain.entities.page import Page

class JsonProfileRepository(ProfileRepository):
    def __init__(self, file_path: Path):
        self._file_path = file_path
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._file_path.write_text("[]", encoding="utf-8")



    def load_profile(self, id: str) -> Profile:
        return self._load(id)

    def load_profile_for_application(self, application: str) -> Profile | None:
         for file_path in self._file_path.glob("*.json"):
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if data["application"] == application:
                return self.load_profile(data["id"])


    def save_profile(self, profile: Profile):   
        self._save(profile)

    def delete_profile(self, id: str):
        # Implement deleting profile from JSON file
        pass

    def profile_names(self) -> dict[str, str]:  # dict[id, name]
        # Implement getting all profiles from JSON file
        pass


    def _load(self, profile_id: str) -> Profile | None:
        file_path = self._file_path / f"{profile_id}.json"

        if not file_path.exists():
            return None

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        pages = [
            Page(
                id=page["id"],
                name=page["name"],
                actions=[
                    [
                        MacroAction(**action) if action is not None else None
                        for action in column
                    ]
                    for column in page["actions"]
                ],
            )
            for page in data["pages"]
        ]

        return Profile(
            id=data["id"],
            name=data["name"],
            application=data["application"],
            pages=pages,
        )



    def _save(self, profile: Profile):

        self._file_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = self._file_path / f"{profile.id}.json"

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                asdict(profile),
                file,
                indent=4,
                ensure_ascii=False,
            )