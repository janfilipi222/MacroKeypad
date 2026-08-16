import json
from dataclasses import asdict
from pathlib import Path

from domain.entities.macro_action import MacroAction
from domain.entities.page import Page
from domain.entities.profile import Profile
from domain.repositories.profile_repository import ProfileRepository


class JsonProfileRepository(ProfileRepository):
    def __init__(self, dir_path: Path):
        self._dir_path = dir_path
        self._dir_path.mkdir(parents=True, exist_ok=True)

    def load_profile(self, id: str) -> Profile | None:
        return self._load(id)

    def load_profile_for_application(self, application: str) -> Profile | None:
        for file_path in self._dir_path.glob("*.json"):
            try:
                with file_path.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                    if data.get("application") == application:
                        return self.load_profile(data["id"])
            except (json.JSONDecodeError, KeyError):
                continue

        return None

    def save_profile(self, profile: Profile):
        self._save(profile)

    def delete_profile(self, id: str):
        file_path = self._dir_path / f"{id}.json"
        if file_path.exists():
            file_path.unlink()

    def profile_names(self) -> dict[str, str]:  # dict[id, name]
        names = {}
        for file_path in self._dir_path.glob("*.json"):
            try:
                with file_path.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                    if "id" in data and "name" in data:
                        names[data["id"]] = data["name"]
            except (json.JSONDecodeError, KeyError):
                continue
        return names

    def load_all_profiles(self) -> list[dict[str, str]]:
        """
        Vrátí seznam všech profilů jako list slovníků:
        [{"name": "Profile 1", "id": "uuid-1"}, ...]
        """
        profiles_list = []
        for file_path in self._dir_path.glob("*.json"):
            try:
                with file_path.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                    if "id" in data and "name" in data:
                        profiles_list.append({
                            "name": data["name"],
                            "id": data["id"]
                        })
            except (json.JSONDecodeError, KeyError):
                continue
        return profiles_list

    def _load(self, profile_id: str) -> Profile | None:
        file_path = self._dir_path / f"{profile_id}.json"

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
            for page in data.get("pages", [])
        ]

        return Profile(
            id=data["id"],
            name=data["name"],
            application=data.get("application", ""),
            pages=pages,
        )

    def _save(self, profile: Profile):
        self._dir_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = self._dir_path / f"{profile.id}.json"

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                asdict(profile),
                file,
                indent=4,
                ensure_ascii=False,
            )