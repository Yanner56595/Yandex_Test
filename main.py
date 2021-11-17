import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow
from PyQt5.QtGui import QPainter, QColor
from random import randint


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.do_paint = False
        self.pushButton.clicked.connect(self.paint)

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw_flag(qp)
            qp.end()

    def paint(self):
        self.do_paint = True
        self.repaint()

    def draw_flag(self, qp):
        for i in range(randint(1, 15)):
            qp.setBrush(QColor(randint(0, 255), randint(0, 255), randint(0, 255)))
            size = randint(50, 500)
            qp.drawEllipse(randint(0, 1000), randint(0, 700), size, size)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())