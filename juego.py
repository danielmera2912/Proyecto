class Juego:
    puntuacion=0
    texto_cerrar = "Cerrar juego. Registrar puntuación"
    def obtener_puntuacion(self):
        return self.puntuacion
    def rejugar(self):
        ...
    def fondo(self):
        stylesheet = """
            QMainWindow {
                background-image: url("fondo/fondo2.png"); 
                background-repeat: no-repeat; 
                background-position: center;
            }
        """
        self.setStyleSheet(stylesheet)