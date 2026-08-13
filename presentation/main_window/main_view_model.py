from application.use_cases.get_profiles_use_case import GetProfilesUseCase




class MainViewModel:
    def __init__(
            self, 
            get_profiles: GetProfilesUseCase
        ):
        self._get_profiles = get_profiles