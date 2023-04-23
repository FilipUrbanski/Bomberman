import sys
import json
from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtCore import QThread
import socket
from server import server

SETTINGS_FILE = "settings.json"


def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        return None


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)


class ServerThread(QThread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        server(self.host, self.port)


settings = load_settings()
if settings is not None:
    ZOOM = settings["zoom"]
    GRID_SIZE = settings["grid_size"]
else:
    print("No settings file found. Using default values.")
    ZOOM = 800
    GRID_SIZE = 20

GRID_SIZE_2 = int(GRID_SIZE / 2)
ONE_GRID = int(ZOOM / GRID_SIZE)
OBSTACLE_DENSITY = 0.15
ENEMY_DENSITY = 0.05
ENEMY_SPEED = 2

if __name__ == "__main__":
    app = QApplication(sys.argv)

    from MainWindow import MainWindow

    window = MainWindow()
    window.show()

    result = QInputDialog.getText(window, "Change Settings", "Do you want to change the game settings? (Y/N)")
    if result[0].lower() == "y":
        zoom, ok1 = QInputDialog.getInt(window, "Change Settings", "Enter new value for zoom (recommended values: 800, 1600, 3200):", ZOOM, min=1)
        grid_size, ok2 = QInputDialog.getInt(window, "Change Settings", "Enter new value for grid size (recommended values: any even number between 10 and 80):", GRID_SIZE, min=2)
        if ok1 and ok2:
            ZOOM = zoom
            GRID_SIZE = grid_size
            GRID_SIZE_2 = int(GRID_SIZE / 2)
            ONE_GRID = int(ZOOM / GRID_SIZE)

            settings = {"zoom": ZOOM, "grid_size": GRID_SIZE}
            save_settings(settings)

    HOST = '192.168.0.100'
    PORT = 5353

    server_thread = ServerThread(HOST, PORT)
    server_thread.start()




    sys.exit(app.exec_())
