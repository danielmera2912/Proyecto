from datetime import datetime
from pathlib import Path
import random
import sys, os
import textwrap
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QWidget, QAbstractItemView, QVBoxLayout, QMessageBox, QFormLayout, QTextEdit, QSpinBox
from Qt import QtGui
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel
from design import Ui_MainWindow
import pyqtgraph as pg
import pyqtgraph.exporters
from PySide6 import QtWidgets, QtGui


db = QSqlDatabase("QSQLITE")
db.setDatabaseName("chinook.sqlite")

db.open()

class AnotherWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setupUi(self)
        self.modelo = QSqlRelationalTableModel(db=db)
        self.modelo.setTable("estadisticas")
        self.modelo.select()
        self.modelo.setHeaderData(0, Qt.Horizontal, "nombre")
        self.modelo.setHeaderData(1, Qt.Horizontal, "dificultad")
        self.modelo.setHeaderData(2, Qt.Horizontal, "score")
        self.modelo.setHeaderData(3, Qt.Horizontal, "tiempo")
        self.modelo.setHeaderData(4, Qt.Horizontal, "juego")
        self.tabla.setModel(self.modelo)
        self.tabla.resizeColumnsToContents()
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.selectionModel().selectionChanged.connect(self.seleccion)
        self.actionModificar.triggered.connect(self.modificar)
        self.actionInsertar.triggered.connect(self.nueva)
        self.actionEliminar.triggered.connect(self.borrar)
        self.fila = -1




        self.setLayout(layout)
    def seleccion(self, seleccion):
    # Recuerda que indexes almacena los índices de la selección
        if seleccion.indexes():
            # Nos quedamos con la fila del primer índice (solo se puede seleccionar una fila)
            self.fila = seleccion.indexes()[0].row()
            # Obtenemos los valores del modelo en esa fila
            nombre = self.modelo.index(self.fila, 0).data()
            dificultad = self.modelo.index(self.fila, 1).data()
            score = self.modelo.index(self.fila, 2).data()
            tiempo = self.modelo.index(self.fila, 3).data()
            juego = self.modelo.index(self.fila, 4).data()
            # Modificamos los campos del formulario para establecer esos valores
            self.nombreText.setText(str(nombre))
            self.dificultadText.setText(str(dificultad))
            self.scoreText.setText(str(score))
            self.tiempoText.setText(str(tiempo))
            self.juegoText.setText(str(juego))
        else:
            # Si no hay selección,  ponemos la fila inicial a un valor que indica que no está seleccionada ninguna fila
            self.fila = -1

    def modificar(self):
        # Si es una fila válida la seleccionada
        if self.fila >= 0:
            # Obtenemos los valores de los campos del formulario
            nombre = self.nombreText.text()
            dificultad = self.dificultadText.text()
            score = self.scoreText.text()
            tiempo = self.tiempoText.text()
            juego = self.juegoText.text()
            # Actualizamos los campos en el modelo
            self.modelo.setData(self.modelo.index(self.fila, 0), nombre)
            self.modelo.setData(self.modelo.index(self.fila, 1), dificultad)
            self.modelo.setData(self.modelo.index(self.fila, 2), score)
            self.modelo.setData(self.modelo.index(self.fila, 3), tiempo)
            self.modelo.setData(self.modelo.index(self.fila, 4), juego)
            # Ejecutamos los cambios en el modelo
            self.modelo.submit()

    def nueva(self):
        # Guardamos en la variable nuevaFila el número de filas del modelo
        nuevaFila = self.modelo.rowCount()
        # Insertamos una nueva fila en el modelo en la posición de ese valor
        self.modelo.insertRow(nuevaFila)
        # Seleccionamos la fila nueva
        self.tabla.selectRow(nuevaFila)
        # Ponemos en blanco el texto la dificultad en el formulario
        self.dificultadText.setText("")

        # Establecemos en blanco los valores de esa nueva fila
        self.modelo.setData(self.modelo.index(nuevaFila, 1), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 2), 0)
        # Ejecutamos los cambios en el modelo
        self.modelo.submit()

    def borrar(self):
        # Si es una fila válida la seleccionada
        if self.fila >= 0:
            # Borramos la fila en el modelo
            self.modelo.removeRow(self.fila)
            # Actualizamos la tabla
            self.modelo.select()
            # Y ponemos la fila actual a -1
            self.fila = -1
            # Reseteamos los valores en los campos del formulario
            self.nombreText.setText("")
            self.dificultadText.setText("")
            self.scoreText.setText("")
            self.tiempoText.setText("")
            self.juegoText.setText("")