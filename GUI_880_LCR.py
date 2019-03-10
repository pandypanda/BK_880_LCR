 
import sys
from itertools import product
from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWidget
#from PyQt5.QtCore import pyqtSlot



class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent=parent)
        self.layoutUI()


    def layoutUI(self):
        self.setStyleSheet("background-color: purple;")

        self.principalLayout = QHBoxLayout(self)

        self.rightFrame = QFrame(self)
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.rightFrame)
        self.gridLayout = QGridLayout()

        btns = {(0, 0): "L", (0, 1): "C", (0, 2): "R", (0, 3): "Z", (0, 4): "DCR",
                (1, 0): "D", (1, 1): "Q", (1, 3): "THETA", (1, 4): "ESR",
                (2, 0): "100Hz", (2, 1): "120Hz", (2, 2): "1kHz", (2, 3): "10kHz", (2, 4): "100kHz",
                (3, 0): "0,3v", (3, 1): "0,6v", (3, 2): "1v", (3, 3): "SER", (3, 4): "PAL",
                (4, 0): "TOL", (4, 1): "1%", (4, 2): "5%", (4, 3): "10%", (4, 4): "20%",
                (5, 0): "LLO", (5, 1): "GTL", (5, 3): "REC", (5, 4): "TRG"}
        for pos, name in btns.items():
            x, y = pos
            btn = QPushButton(self.rightFrame)
            btn.setText(name)
            self.gridLayout.addWidget(btn, x, y)
            # When btn is clicked, send his 'name' to 'make_callfunction'
            btn.clicked.connect(self.make_callfunction(name))
        self.verticalLayout.addLayout(self.gridLayout)
        self.principalLayout.addWidget(self.rightFrame)

    # Print the 'name' of the clicked btn inthe console
    def make_callfunction(self, name):
            def callfunction():
                print(name)
            return callfunction


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
