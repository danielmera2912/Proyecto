from PySide6 import QtWidgets
from trabajo import MainWindow
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QPixmap
class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        mainToggle = MainWindow()
        self.setCentralWidget(mainToggle)
stylesheet = """
    MainWindow {
        background-image: url("fondo2.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""
app = QtWidgets.QApplication([])
app.setStyleSheet(stylesheet)
w = Window()
w.showMaximized()
app.exec()


