import resources_rc

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtCore import QTimer, QRectF, Qt, QMutex

from main import ONE_GRID
from Obstacle import Obstacle
from Enemy import Enemies


class Bomb(QGraphicsItem):
    def __init__(self, x, y, parent=None):
        super().__init__(parent)
        self.crack = QPixmap(":/img/murekmocno.png")
        self.pos_x = x
        self.mutex = QMutex()
        self.pos_y = y
        self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)
        self.timer = QTimer()
        self.timer.timeout.connect(self.explode)
        self.timer.start(3000)
        self.explosion = None

    def boundingRect(self):
        return QRectF(0, 0, ONE_GRID, ONE_GRID)

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(Qt.darkGray))
        painter.drawEllipse(0, 0, ONE_GRID, ONE_GRID)

    def show(self):
        self.setVisible(True)

    def explode(self):
        radius = 1
        self.hide()
        to_remove = set()

        for x in range(self.pos_x - radius, self.pos_x + radius + 1):
            for y in range(self.pos_y - radius, self.pos_y + radius + 1):

                items = self.scene().items(QRectF(x * ONE_GRID, y * ONE_GRID, ONE_GRID, ONE_GRID))

                for item in items:
                    if isinstance(item, Obstacle):
                        if item.obstacle_type.startswith("destroyable_one"):
                            to_remove.add(item)
                        elif item.obstacle_type.startswith("destroyable_two"):
                            item.obstacle_type = "destroyable_one"
                           # painter.drawPixmap(0, 0, ONE_GRID, ONE_GRID, self.crack)
                    elif isinstance(item, Enemies):
                        if item.enemy_type.startswith(("horizontal", "vertical", "static", "follow")):
                            to_remove.add(item)

        for item in to_remove:
            self.scene().removeItem(item)


        self.explosion = QGraphicsEllipseItem(self.pos_x * ONE_GRID - radius*ONE_GRID, self.pos_y * ONE_GRID - radius*ONE_GRID,
                                               2*radius * ONE_GRID + ONE_GRID, 2*radius * ONE_GRID + ONE_GRID)
        self.explosion.setBrush(QBrush(QColor(255, 255, 0, 127)))
        self.scene().addItem(self.explosion)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.scene().removeItem(self.explosion))
        self.timer.start(1000)

