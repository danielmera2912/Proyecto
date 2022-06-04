import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QTabWidget,
    QSplitter
)

from PySide6.QtCore import QUrl
from PySide6.QtHelp import QHelpEngine
from PySide6.QtWebEngineWidgets import QWebEngineView

class HelpWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Ayuda del programa")
        
        # Creamos una instancia de QHelpEngine con el contenido del archivo de ayuda generado
        self.helpEngine = QHelpEngine("mycollection.qhc")
        # Con setupData cargamos los datos
        self.helpEngine.setupData()

        # Creamos un widget de pestañas en el que añadimos el índice de contenido y el índice de palabras clave
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.helpEngine.contentWidget(), "Contenido")
        self.tabWidget.addTab(self.helpEngine.indexWidget(), "Índice")

        # Creamos el visor web donde se mostrará la ayuda
        self.helpBrowser = QWebEngineView()

        # Cuando se haga doble clic en una palabra clave, se carga la url correspondiente
        self.helpEngine.indexWidget().linkActivated.connect(self.cargarUrl)
        # Cuando se haga doble clic en un capítulo, se carga la url correspondiente
        self.helpEngine.contentWidget().linkActivated.connect(self.cargarUrl)

        # Establecemos el contenido del navegador en la página principal de la ayuda
        self.helpBrowser.setContent(self.helpEngine.fileData(QUrl("qthelp://"+self.helpEngine.registeredDocumentations()[0]+"/doc/index.html")),"text/html")

        # Creamos un separador en el que ponemos las pestañas y el contenido
        self.splitter = QSplitter()
        self.splitter.insertWidget(0, self.tabWidget)
        self.splitter.insertWidget(1, self.helpBrowser)

        layout.addWidget(self.label)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
    
    # Método que recoge la url que emite la señal y la carga en el navegador
    def cargarUrl(self,url):
        self.helpBrowser.setContent(self.helpEngine.fileData(url),"text/html")
        print(url)

class HelpElementWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Ayuda del elemento generaGrafica")
        
        # Creamos una instancia de QHelpEngine con el contenido del archivo de ayuda generado
        self.helpEngine = QHelpEngine("mycollection.qhc")
        # Con setupData cargamos los datos
        self.helpEngine.setupData()

        # Creamos un widget de pestañas en el que añadimos el índice de contenido y el índice de palabras clave
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.helpEngine.contentWidget(), "Contenido")
        self.tabWidget.addTab(self.helpEngine.indexWidget(), "Índice")

        # Creamos el visor web donde se mostrará la ayuda
        self.helpBrowser = QWebEngineView()

        # Cuando se haga doble clic en una palabra clave, se carga la url correspondiente
        self.helpEngine.indexWidget().linkActivated.connect(self.cargarUrl)
        # Cuando se haga doble clic en un capítulo, se carga la url correspondiente
        self.helpEngine.contentWidget().linkActivated.connect(self.cargarUrl)

        

        # Creamos un separador en el que ponemos las pestañas y el contenido
        self.splitter = QSplitter()
        self.splitter.insertWidget(0, self.tabWidget)
        self.splitter.insertWidget(1, self.helpBrowser)

        layout.addWidget(self.label)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
    
    def cargarUrl(self,url):
        self.helpBrowser.setContent(self.helpEngine.fileData(url),"text/html")
        print(url)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = HelpWindow()
        self.h = HelpElementWindow()
        self.button_ayuda = QPushButton("Ayuda completa")
        self.button_ayuda.clicked.connect(self.toggle_helpwindow)

       

        # layout = QVBoxLayout()
        # layout.addWidget(self.button_ayuda)
        # container = QWidget()
        # container.setLayout(layout)

        # self.setCentralWidget(container)

    def toggle_helpwindow(self, checked):
        
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()

    def toggle_elementhelpwindow(self, checked):
        
        if self.h.isVisible():
            self.h.hide()

        else:
            self.h.show()

