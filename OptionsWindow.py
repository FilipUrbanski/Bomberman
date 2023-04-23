import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QCheckBox, QDialog
from PyQt5.QtCore import Qt
from MainWindow import MainWindow  # assuming you have a MainWindow class defined in MainWindow.py file
from Player import Player


class OptionsWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Game Options")
        self.setFixedSize(400, 300)

        # Grid size selection
        self.grid_size_label = QLabel("Grid Size", self)
        self.grid_size_label.move(20, 20)
        self.grid_size_combo = QComboBox(self)
        self.grid_size_combo.move(120, 20)
        self.grid_size_combo.addItems(["Small (20x20)", "Medium (40x40)", "Large (80x80)"])


        # Number of players selection
        self.players_label = QLabel("Number of Players", self)
        self.players_label.move(20, 100)
        self.players_combo = QComboBox(self)
        self.players_combo.move(120, 100)
        self.players_combo.addItems(["1", "2", "AI"])

        # Save game history options
        self.save_label = QLabel("Save Game History", self)
        self.save_label.move(20, 140)
        self.sqlite_checkbox = QCheckBox("SQLite3", self)
        self.sqlite_checkbox.move(120, 140)
        self.xml_checkbox = QCheckBox("XML", self)
        self.xml_checkbox.move(120, 160)
        self.json_checkbox = QCheckBox("JSON", self)
        self.json_checkbox.move(120, 180)

        # Load game history option
        self.load_label = QLabel("Load Game History", self)
        self.load_label.move(20, 220)
        self.load_button = QPushButton("Load", self)
        self.load_button.move(120, 220)

        # OK and Cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.move(250, 270)
        self.ok_button.clicked.connect(self.open_main_window)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.move(170, 270)
        self.cancel_button.clicked.connect(self.close)


        self.xml_checkbox.stateChanged.connect(self.updateBoolVariables)
        self.sqlite_checkbox.stateChanged.connect(self.updateBoolVariables)
        self.json_checkbox.stateChanged.connect(self.updateBoolVariables)

    def exec_(self):
        super().exec_()
        # Return selected options as a dictionary
        options = {
            "grid_size": self.grid_size_combo.currentText(),
            "zoom": self.zoom_combo.currentText(),
            "num_players": int(self.players_combo.currentText()),
            "save_sqlite": self.sqlite_checkbox.isChecked(),
            "save_xml": self.xml_checkbox.isChecked(),
            "save_json": self.json_checkbox.isChecked(),
            "load_history": False  # Currently not implemented
        }
        return options

    def open_main_window(self):
        #options = self.exec_()
        main_window = MainWindow()
        main_window.show()
        self.close()

    def updateBoolVariables(self):
        # Assuming you have a class named MyClass with boolean variables named xml, sql, and json
        XML = self.xml_checkbox.isChecked()
        SQL = self.sqlite_checkbox.isChecked()
        JSON = self.json_checkbox.isChecked()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    options_window = OptionsWindow()
    options_window.show()
    sys.exit(app.exec_())