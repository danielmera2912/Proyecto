import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout, QMainWindow

class IndexedButtonWidget(QPushButton):
    def __init__(self, text, parent=None):    
        super(IndexedButtonWidget, self).__init__(text,parent=parent)
        self.button_row = 0
        self.button_column = 0

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        layout = QGridLayout()

        self.buttons = {}
        for i in range(10):
            for j in range(10):
                # keep a reference to the buttons
                self.buttons[(i, j)] = IndexedButtonWidget('row %d, col %d' % (i, j))
                # add to the layout
                self.buttons[(i, j)].button_row = i
                self.buttons[(i, j)].button_column = j
                layout.addWidget(self.buttons[(i, j)], i, j)
                # add connection
                self.buttons[(i, j)].clicked.connect(self.handleButtonClicked)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def handleButtonClicked(self):
        button = self.sender()
        print(button.button_row)
        print(button.button_column)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()