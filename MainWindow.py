import sys
import random
import resources_rc
import datetime
import xml.etree.ElementTree as ET
import socket

from PyQt5.QtWidgets import QLineEdit, QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QGraphicsPixmapItem, QLabel, QGraphicsTextItem
from PyQt5.QtGui import QColor, QBrush, QPen, QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF, QTimer, pyqtSignal

from Player import Player, BOMB_COUNT
from Player2 import Player2, BOMB_COUNT
from Obstacle import generate_obstacles
from Enemy import generate_enemies, Enemies
from main import GRID_SIZE, ONE_GRID, GRID_SIZE_2



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bg_item = QGraphicsPixmapItem(QPixmap(":/img/bg.png").scaled(GRID_SIZE * ONE_GRID + ONE_GRID, GRID_SIZE * ONE_GRID + ONE_GRID))

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

        self.player2 = Player2()
        self.player2.setPos(GRID_SIZE * ONE_GRID, GRID_SIZE * ONE_GRID)
        self.scene.addItem(self.player2)

        self.keyPressEvent = self.handle_keypress

        generate_enemies(self.scene)
        generate_obstacles(self.scene)

        self.setCentralWidget(self.view)

        self.showMaximized()
        #print(options("grid_size"))

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