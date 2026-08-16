import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths

from PySide6.QtWidgets import QApplication

from presentation.main_window.main_window import MainWindow
from presentation.main_window.main_view_model import MainViewModel

from infrastructure.repositories.json_profile_repository import (
    JsonProfileRepository,
)



def main():
    app = QApplication(sys.argv)
    
    app.setOrganizationName("CGM")
    app.setApplicationName("MacroKeypadBackgroundApp")

    
    app_data = Path(QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation))
    profile_path = app_data / "profiles"

    profile_repository = JsonProfileRepository(profile_path)

    view_model = MainViewModel(
        repo=profile_repository,
        app_data=app_data
    )

    main_window = MainWindow(view_model)
    main_window.show()




    sys.exit(app.exec())


if __name__ == "__main__":
    main()