import unittest, pytest
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6 import QtWidgets
from simplegames import Estadisticas
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel
db = QSqlDatabase("QSQLITE")
db.setDatabaseName("chinook.sqlite")
db.open()
class introducirDatos (QMainWindow):
    def add(self):
        app=QApplication.instance()
        if app==None:
            app= QApplication([])
        
        window=Estadisticas()
        cont = 0
        listaN= []
        while(cont<=5000):
            query = QSqlQuery("SELECT COUNT(DISTINCT juego) FROM estadisticas",db=db)
            while query.next():
                listaN.append(query.value(0))
            cont = cont+1

        nuevaFila = window.modelo.rowCount()
        total= nuevaFila+1
        
        while(nuevaFila<total):
            window.modelo.insertRow(nuevaFila)
            window.tabla.selectRow(nuevaFila)
            window.modelo.setData(window.modelo.index(nuevaFila, 0), "Ernesto")
            window.modelo.setData(window.modelo.index(nuevaFila, 1), "2")
            window.modelo.setData(window.modelo.index(nuevaFila, 2), "BlackJack")
            nuevaFila= nuevaFila+1
            window.modelo.submit()

    
class QMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        introducirDatos(self).add()
app = QtWidgets.QApplication([])
w = QMainWindow()
w.show()
app.exec()