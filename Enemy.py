import random
import resources_rc

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF

from main import ONE_GRID, GRID_SIZE, ENEMY_DENSITY, ENEMY_SPEED


class Enemies(QGraphicsItem):
    def __init__(self, enemy_type, parent=None):
        super().__init__(parent)
        self.enemy_type = enemy_type
        self.setZValue(-1)
        if enemy_type == "static":
            self.size = ONE_GRID
            self.color = Qt.darkGray
            self.sprite = QPixmap(":/img/static.png")
        elif enemy_type == "horizontal":
            self.size = ONE_GRID
            self.color = Qt.yellow
            self.speed = ONE_GRID / (2 * ENEMY_SPEED)
            self.sprite = QPixmap(":/img/horizontal_vertical.png")
        elif enemy_type == "vertical":
            self.size = ONE_GRID
            self.color = Qt.lightGray
            self.speed = ONE_GRID / (2 * ENEMY_SPEED)
            self.sprite = QPixmap(":/img/horizontal_vertical.png")
        elif enemy_type == "follow":
            self.size = ONE_GRID
            self.color = Qt.blue
            self.speed = ONE_GRID / ENEMY_SPEED
            self.sprite = QPixmap(":/img/follow.png")

    def boundingRect(self):
        return QRectF(0, 0, ONE_GRID, ONE_GRID)

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, ONE_GRID, ONE_GRID, self.sprite)

    def move_horizontal(self):
        if self.enemy_type == "horizontal":
            current_pos = self.pos()
            new_pos = current_pos + Qt.RightEdge * self.speed
            self.setPos(new_pos)


def generate_enemies(scene):
    enemies_probs = {"static": 0.5, "horizontal": 0.2, "vertical": 0.2, "follow": 0.1}
    for x in range(1, GRID_SIZE - 1):
        for y in range(1, GRID_SIZE - 1):
            if random.random() < ENEMY_DENSITY:
                enemy_type = random.choices(list(enemies_probs.keys()), weights=list(enemies_probs.values()))[0]
                enemy = Enemies(enemy_type)
                enemy.setPos(x * ONE_GRID, y * ONE_GRID)
                scene.addItem(enemy)

