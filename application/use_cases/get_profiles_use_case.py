from infrastructure.repositories.json_profile_repository import JsonProfileRepository


class GetProfilesUseCase:

    def __init__(self, repo: JsonProfileRepository):
        self._repo = repo

    def execute(self):
        pass

