from monstruo import *

class Heroe:
    def __init__(self,nombre):
        self.nombre = nombre
        self.ataque = 60    
        self.defensa = 40
        self.defensa_temporal = 5
        self.usando_defensa = False
        self.salud = 100
        self.salud_maxima = 100

    def atacar(self, enemigo):
        daño = self.ataque - enemigo.defensa
        if daño > 0 :
            enemigo.salud -= daño
            print(f"Héroe ataca a {enemigo.nombre}.")
            print(f"El enemigo {enemigo.nombre} ha recibido {daño} puntos de daño.")
        else:
            print(f"El enemigo ha bloqueado el ataque.")

    def curarse(self):
        self.salud += 20
        if self.salud >= self.salud_maxima :
            self.salud = self.salud_maxima
        print(f"Héroe se ha curado. Salud actual: {self.salud}")

    def defenderse(self):
        if not self.usando_defensa:
            self.defensa += self.defensa_temporal
            self.usando_defensa = True
            print(f"El héroe aumenta temporalmente su defensa en 10 puntos para el siguiente ataque.")

    def reset_defensa(self):
        if  self.usando_defensa:
            self.defensa -= self.defensa_temporal
            self.usando_defensa = False
            print(f"La defensa de  {self.nombre} vuelve a la normalidad.")

    def esta_vivo(self):
        vivo = True
        if self.salud <= 0:
            vivo = False
        return vivo