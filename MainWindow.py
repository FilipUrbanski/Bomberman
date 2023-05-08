import json
import sys
import random
import resources_rc
import datetime
import xml.etree.ElementTree as ET
import socket

from PyQt5.QtWidgets import QLineEdit, QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QGraphicsPixmapItem, \
    QLabel, QGraphicsTextItem
from PyQt5.QtGui import QColor, QBrush, QPen, QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF, QTimer, pyqtSignal, QThread

from Player import Player, BOMB_COUNT
from Player2 import Player2, BOMB_COUNT
from Obstacle import generate_obstacles
from Enemy import generate_enemies, Enemies
from main import GRID_SIZE, ONE_GRID, GRID_SIZE_2
from client import client, HOST, PORT


"""class ClientThread(QThread):
    def __init__(self, host, port, x, y):
        super().__init__()
        self.host = HOST
        self.port = PORT
        self.x = x
        self.y = y
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        # client(self.host, self.port, self.x, self.y)
        self.s.connect((HOST, PORT))
        print("Connected to server")

        current_pos = (self.x, self.y)

        print("Disconnected from server")

    def send_player_position(self, pos_x, pos_y):
        # Send message to server
        message = {"message": "player_position", "pos_y": pos_y, "pos_x": pos_x}

        message_json = json.dumps(message)
        self.s.sendall(message_json.encode())

        # Receive response from server
        response = self.s.recv(1024)
        print(f"Received response: {response.decode()}")"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.PORT = PORT
        self.HOST = HOST

        self.bg_item = QGraphicsPixmapItem(
            QPixmap(":/img/bg.png").scaled(GRID_SIZE * ONE_GRID + ONE_GRID, GRID_SIZE * ONE_GRID + ONE_GRID))

        self.bg_item.setPos(0, 0)
        self.bg_item.setZValue(-1)
        self.setWindowTitle("Bomberman")
        self.setGeometry(100, 100, 1920, 1080)

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.scene.addItem(self.bg_item)

        self.player = Player()
        self.player.setPos(0, 0)
        self.scene.addItem(self.player)



        self.keyPressEvent = self.handle_keypress

        self.scene, self.enemie_coords = generate_enemies(self.scene)
        generate_obstacles(self.scene)

        self.player2 = Player2(self.enemie_coords)
        self.player2.setPos(GRID_SIZE * ONE_GRID, GRID_SIZE * ONE_GRID)
        self.scene.addItem(self.player2)

        self.setCentralWidget(self.view)

        self.showMaximized()

        # print(options("grid_size"))

        #self.client_thread = ClientThread(self.HOST, self.PORT, self.player.pos_x, self.player.pos_y)
        #self.client_thread.start()
        # client(self.HOST, self.PORT, self.player.pos_x, self.player.pos_y)


    def handle_keypress(self, event):
        self.player.keyPressEvent(event)
        self.player2.keyPressEvent(event)

    def save_player_data(self, name, position, time):
        # Create a new XML element for the player
        player = ET.Element("player")

        # Add attributes for the player element
        player.set("name", name)
        player.set("position", position)
        player.set("time", time)
        player.set("date", str(datetime.date.today()))

        # Load the existing data from the XML file
        try:
            root = ET.parse("player_data.xml").getroot()
        except:
            root = ET.Element("players")

        # Add the new player element to the root
        root.append(player)

        # Save the updated XML data to the file
        tree = ET.ElementTree(root)
        tree.write("player_data.xml")
