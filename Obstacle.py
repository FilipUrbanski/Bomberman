import random
import resources_rc

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF

from main import ONE_GRID, GRID_SIZE, GRID_SIZE_2, OBSTACLE_DENSITY


class Obstacle(QGraphicsItem):
    def __init__(self, obstacle_type, parent=None):
        super().__init__(parent)
        self.obstacle_type = obstacle_type
        self.setZValue(-1)
        if obstacle_type == "destroyable_one":
            self.size = ONE_GRID
            self.color = Qt.blue
            self.sprite = QPixmap(":/img/murekmocno.png")
        elif obstacle_type == "destroyable_two":
            self.size = ONE_GRID
            self.color = Qt.green
            self.sprite = QPixmap(":/img/murelekkok.png")
        elif obstacle_type == "indestructible":
            self.size = ONE_GRID
            self.color = Qt.darkGray
            self.sprite = QPixmap(":/img/murek.png")

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, ONE_GRID, ONE_GRID, self.sprite)


def generate_obstacles(scene):
    obstacle_probs = {"destroyable_one": 0.7, "destroyable_two": 0.3}
    for x in range(1, GRID_SIZE - 1):
        for y in range(1, GRID_SIZE - 1):
            if random.random() < OBSTACLE_DENSITY:
                obstacle_type = random.choices(list(obstacle_probs.keys()), weights=list(obstacle_probs.values()))[0]
                obstacle = Obstacle(obstacle_type)
                obstacle.setPos(x * ONE_GRID, y * ONE_GRID)
                scene.addItem(obstacle)

    for x in range(1, GRID_SIZE_2):
        for y in range(1, GRID_SIZE_2):
            obstacle_type_perm = "indestructible"
            obstacle_perm = Obstacle(obstacle_type_perm)
            obstacle_perm.setPos((x + x) * ONE_GRID, (y + y) * ONE_GRID)
            scene.addItem(obstacle_perm)
