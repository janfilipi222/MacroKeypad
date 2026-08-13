import sys

from PySide6.QtWidgets import QApplication

from presentation.main_window.main_window import MainWindow
from presentation.main_window.main_view_model import MainViewModel

from infrastructure.repositories.json_profile_repository import (
    JsonProfileRepository,
)

from application.use_cases.get_profiles import GetProfiles


def main():
    app = QApplication(sys.argv)

    # Infrastructure
    profile_repository = JsonProfileRepository()

    # Application
    get_profiles = GetProfiles(profile_repository)

    # Presentation
    view_model = MainViewModel(
        get_profiles=get_profiles,
    )

    main_window = MainWindow(view_model)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()