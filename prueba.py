import random
from PySide6 import QtWidgets
from trabajo import MainWindow

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        while(True):
            print(random.randint(0, 2))
    def multiply(self):
        print('The product of two numbers is: ')
app = QtWidgets.QApplication([])
w = Window()
w.show()
app.exec()