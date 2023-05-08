import resources_rc
import random
import math

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF, QTimer

from Obstacle import ONE_GRID, GRID_SIZE
from Enemy import Enemies
from Obstacle import Obstacle
from Bomb import Bomb

BOMB_COUNT = 3


class Player2(QGraphicsItem):
    def __init__(self, enemy_coords, parent=None):
        super().__init__(parent)
        self.enemy_coords = enemy_coords
        self.BOMB_COUNT = BOMB_COUNT
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFocus()
        self.pos_x = GRID_SIZE - 1
        self.pos_y = GRID_SIZE - 1
        self.player = QPixmap("img/szczurstoi.png")
        self.player_anim_0 = QPixmap("img/szczuridzie1.png")
        self.player_anim_1 = QPixmap("img/szczuridzie2.png")
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.checkOutOfBounds)
        self.check_timer.start(50)
        self.timer = QTimer()
        self.timer.timeout.connect(self.moveAutomatically)
        self.timer.start(300)  # Change the time interval as needed.
        self.placed_bombs = set()  # Keep track of enemy coords for which the player has already placed a bomb
        self.bomb_timer = QTimer()
        self.bomb_timer.timeout.connect(self.moveAutomatically)
        self.bomb_timer.setSingleShot(True)

    import random

    def moveAutomatically(self):
        # Find the closest enemy
        closest_enemy = min(self.enemy_coords,
                            key=lambda enemy: math.sqrt((enemy[0] - self.pos_x) ** 2 + (enemy[1] - self.pos_y) ** 2))
        dx = closest_enemy[0] - self.pos_x
        dy = closest_enemy[1] - self.pos_y

        if abs(dx) > abs(dy):
            if dx > 0:
                new_x = self.pos_x + 1
            else:
                new_x = self.pos_x - 1
            new_y = self.pos_y
        else:
            if dy > 0:
                new_y = self.pos_y + 1
            else:
                new_y = self.pos_y - 1
            new_x = self.pos_x

        while (new_x < 0 or new_x > GRID_SIZE or
               new_y < 0 or new_y > GRID_SIZE or
               self.collidesWithObstacleAtPos(new_x, new_y)):
            options = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
            direction = random.choice(options)
            new_x = self.pos_x + direction[0]
            new_y = self.pos_y + direction[1]

            if direction == (0, 0):
                if (self.pos_x, self.pos_y) not in self.placed_bombs:
                    bomba = Bomb(self.pos_x, self.pos_y)
                    self.scene().addItem(bomba)
                    self.placed_bombs.add((self.pos_x, self.pos_y))
                    print(f"bomb placed at {self.pos_x, self.pos_y}")
                    self.enemy_coords.remove(closest_enemy)
                return

        if self.collidesWithEnemyAtPos(new_x, new_y):
            if (new_x, new_y) not in self.placed_bombs:
                bomba = Bomb(new_x, new_y)
                self.scene().addItem(bomba)
                self.placed_bombs.add((new_x, new_y))
                print(f"bomb placed at {new_x, new_y}")
                self.enemy_coords.remove(closest_enemy)
            return

        self.pos_x, self.pos_y = new_x, new_y
        self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)

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
