from abc import ABC, abstractmethod
from domain.model.profile import Profile

class ProfileRepository(ABC):

    @abstractmethod
    def load_profile(self, id: str) -> Profile:
        pass

    @abstractmethod
    def load_profile_for_application(self, application: str) -> Profile:
        pass

    @abstractmethod
    def save_profile(self, profile: Profile):
        pass

    @abstractmethod
    def delete_profile(self, id: str):
        pass

    @abstractmethod
    def profile_names(self) -> dict[str, str]:  # dict[id, name]
        pass