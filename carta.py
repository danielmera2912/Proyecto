class Carta():
    def __init__(self, numero, palo):
        super().__init__()
        self.numero=numero
        self.palo=palo
        self.paloT= ""
    def infoCarta(self):
        if(self.palo=="O"):
            self.paloT="Oro"
        elif(self.palo=="C"):
            self.paloT="Copas"
        elif(self.palo=="E"):
            self.paloT="Espadas"
        elif(self.palo=="B"):
            self.paloT="Bastos"
        print(str(self.numero)+" de "+self.paloT)