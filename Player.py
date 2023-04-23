import resources_rc
import xml.etree.ElementTree as ET
import json
import sqlite3
import os

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF, QTimer, QPointF

from Obstacle import ONE_GRID, GRID_SIZE
from Enemy import Enemies
from Obstacle import Obstacle
from Bomb import Bomb
from server import server

BOMB_COUNT = 3

XML = bool(input(print("Save to XML?")))
JSON = bool(input(print("Save to JSON?")))
SQL = bool(input(print("Save to SQLite3?")))



# Create the root element
if XML is True:
    root = ET.Element("player_movements")

if SQL is True:
    # Create a database connection and a cursor object
    conn = sqlite3.connect('movement_data.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS player_movements (
                        id INTEGER PRIMARY KEY,
                        player_id INTEGER,
                        x INTEGER,
                        y INTEGER
                    )''')


class Player(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.BOMB_COUNT = BOMB_COUNT
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFocus()
        self.pos_x = 0
        self.pos_y = 0
        self.player = QPixmap("img/szczurstoi.png")
        self.player_anim_0 = QPixmap("img/szczuridzie1.png")
        self.player_anim_1 = QPixmap("img/szczuridzie2.png")
        self.speed = 1
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.checkOutOfBounds)
        self.check_timer.start(50)
        self.player_moved = 0
        self.player_movement = []
        self.filename = 'player_movements.xml'


        HOST = '192.168.0.100'
        PORT = 5353

        server(HOST, PORT)

        """def movePlayerFromXML(self, filename):
        # Parse the XML file
        tree = ET.parse(filename)
        root = tree.getroot()

        # Iterate over the player_movements elements
        for move in root.iter('player_movements'):
            # Extract the x and y attributes
            x = int(move.attrib['x'])
            y = int(move.attrib['y'])

            # Move the player to the new position
            self.setPos(x * ONE_GRID, y * ONE_GRID)

            # Delay the movement for a short period
            QTimer.singleShot(100, self.update)"""

    def checkOutOfBounds(self):
        if self.pos_x < 0:
            self.pos_x = GRID_SIZE

        elif self.pos_x > GRID_SIZE:
            self.pos_x = 0

        elif self.pos_y < 0:
            self.pos_y = GRID_SIZE

        elif self.pos_y > GRID_SIZE:
            self.pos_y = 0

    def boundingRect(self):
        return QRectF(0, 0, ONE_GRID, ONE_GRID)

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, ONE_GRID, ONE_GRID, self.player)


    def collidesWithObstacleAtPos(self, x, y):
        colliding_items = self.scene().items(QRectF(x * ONE_GRID, y * ONE_GRID, ONE_GRID, ONE_GRID))
        for item in colliding_items:
            if isinstance(item, Obstacle):
                return True
        return False

    def collidesWithEnemyAtPos(self, x, y):
        colliding_items = self.scene().items(QRectF(x * ONE_GRID, y * ONE_GRID, ONE_GRID, ONE_GRID))
        for item in colliding_items:
            if isinstance(item, Enemies):
                return True
        return False

    def keyPressEvent(self, event):
        player_movements = []
        if event.key() == Qt.Key_Left:
            self.player_moved += 1
            if self.pos_x > -1:
                if not self.collidesWithObstacleAtPos(self.pos_x - 1, self.pos_y):
                    self.pos_x -= 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)
            self.player_movement.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})
            player_movements.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})

        elif event.key() == Qt.Key_Right:
            self.player_moved += 1
            if self.pos_x < GRID_SIZE + 1:
                if not self.collidesWithObstacleAtPos(self.pos_x + 1, self.pos_y):
                    self.pos_x += 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)
            self.player_movement.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})
            player_movements.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})

        elif event.key() == Qt.Key_Up:
            self.player_moved += 1
            if self.pos_y > -1:
                if not self.collidesWithObstacleAtPos(self.pos_x, self.pos_y - 1):
                    self.pos_y -= 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)
            self.player_movement.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})
            player_movements.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})

        elif event.key() == Qt.Key_Down:
            self.player_moved += 1
            if self.pos_y < GRID_SIZE + 1:
                if not self.collidesWithObstacleAtPos(self.pos_x, self.pos_y + 1):
                    self.pos_y += 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)
            self.player_movement.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})
            player_movements.append({"player_id": 1, "x": self.pos_x, "y": self.pos_y})

        elif event.key() == Qt.Key_Space:
            if self.BOMB_COUNT:
                bomba = Bomb(self.pos_x, self.pos_y)
                self.scene().addItem(bomba)
                print(f"bomb shown at {self.pos_x, self.pos_y}")
                #BOMB_COUNT = self.BOMB_COUNT - 1
            else:
                print("no bombs")


        #self.player_moved.emit()

        if self.collidesWithEnemyAtPos(self.pos_x, self.pos_y):
            exit()


        if XML is True:
            print(player_movements)
            # Add child elements for each player movement
            for movement in player_movements:
                movement_element = ET.SubElement(root, "movement")
                movement_element.set("player_id", str(movement["player_id"]))
                movement_element.set("x", str(movement["x"]))
                movement_element.set("y", str(movement["y"]))
                movement_element.text = "\n"

            # Create the XML file
            tree = ET.ElementTree(root)
            tree.write("player_movements.xml")


        if JSON is True:
            json_string = json.dumps(self.player_movement)

            with open("player_movements.json", "w") as file:
                file.write(json_string)


        if SQL is True:
            cursor.execute("INSERT INTO player_movements (player_id, x, y) VALUES (?, ?, ?)",
                           (1, self.pos_x, self.pos_y))
            conn.commit()
