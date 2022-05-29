from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import  QApplication
from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QWidget, QAbstractItemView, QVBoxLayout, QMessageBox, QFormLayout, QTextEdit, QSpinBox
from PySide6.QtMultimedia import QSoundEffect
import sys
class MusicList(QMainWindow):
    def __init__(self):
        super(MusicList, self).__init__()
        