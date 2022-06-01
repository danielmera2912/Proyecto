import random
from PySide6 import QtWidgets
from trabajo import MainWindow

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        lol= input()
        lol=lol.replace('"','')
        lol=lol.replace(';','')
        lol=lol.replace("'","")
        lol=lol.replace('?','')
        lol=lol.replace('-','')
        lol=lol.replace('!','')
        print(lol)
app = QtWidgets.QApplication([])
w = Window()
w.show()
app.exec()