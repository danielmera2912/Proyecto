from PySide6 import QtWidgets
from simplegames import MainWindow
from PySide6.QtCore import QUrl, Qt
from PySide6 import QtWidgets, QtGui
import sys, os
from PySide6.QtGui import QPixmap
basedir = os.path.dirname(__file__)
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
w.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'sg.ico')))
w.setWindowIcon(QtGui.QIcon('sg.ico'))
w.setWindowTitle("SimpleGames")
w.showMaximized()
app.exec()


