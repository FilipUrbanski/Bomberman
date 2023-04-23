import resources_rc

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF, QTimer

from Obstacle import ONE_GRID, GRID_SIZE
from Enemy import Enemies
from Obstacle import Obstacle
from Bomb import Bomb

BOMB_COUNT = 3


class Player2(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        #player_moved = pyqtSignal()
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
        if event.key() == Qt.Key_A:
            if self.pos_x > -1:
                if not self.collidesWithObstacleAtPos(self.pos_x - 1, self.pos_y):
                    self.pos_x -= 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)

        elif event.key() == Qt.Key_D:
            if self.pos_x < GRID_SIZE + 1:
                if not self.collidesWithObstacleAtPos(self.pos_x + 1, self.pos_y):
                    self.pos_x += 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)

        elif event.key() == Qt.Key_W:
            if self.pos_y > -1:
                if not self.collidesWithObstacleAtPos(self.pos_x, self.pos_y - 1):
                    self.pos_y -= 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)

        elif event.key() == Qt.Key_S:
            if self.pos_y < GRID_SIZE + 1:
                if not self.collidesWithObstacleAtPos(self.pos_x, self.pos_y + 1):
                    self.pos_y += 1 * self.speed
            self.setPos(self.pos_x * ONE_GRID, self.pos_y * ONE_GRID)

        elif event.key() == Qt.Key_K:
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

