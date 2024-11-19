from heroe import *
import random

class Tesoro:
    def __init__(self):
        self.tesoro = ["ataque","defensa","vida"]
        self.aumento_ataque = 20
        self.aumento_defensa= 10
    def encontrar_tesoro(self,heroe):
    
        tesoro = random.choice(self.tesoro)
        print(f"Héroe ha encontrado un tesoro: {tesoro} ")
        if tesoro == "ataque":
            heroe.ataque += self.aumento_ataque
            print(f"El ataque de {heroe.nombre} aumenta a {heroe.ataque}")
        elif tesoro == "defensa":
            heroe.defensa += self.aumento_defensa
            print(f"La defensa de {heroe.nombre} aumenta a  {heroe.defensa}")
        elif tesoro == "vida":
            heroe.salud = heroe.salud_maxima
            print(f"La salud de {heroe.nombre} ha sido restaurada a  {heroe.salud}")