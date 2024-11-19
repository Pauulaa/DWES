from heroe import Heroe
from monstruo import Monstruo
from tesoro import Tesoro


class Mazmorra:
    def __init__(self,heroe):
        self.heroe = heroe  
        self.monstruos = [
              Monstruo("Carlos",40,15,300),
              Monstruo("Iria",30,5,250),
              Monstruo("Rubén",20,10,150),
              Monstruo("Noemí",10,5,140),
              Monstruo("Emilio",5,2,70),
        ]
        self.tesoro = Tesoro()

    def jugar(self):
        print(f"{self.heroe.nombre} entra en la mazmorra")
        for monstruo in self.monstruos:
            print(f"Te has encontrado con un {monstruo.nombre}")
            self.enfrentar_enemigo(monstruo)
            if not self.heroe.esta_vivo():
                print("El héroe ha diso derrotado en la mazmorra")
                return
            self.buscar_tesoro()
        print(f"{self.heroe.nombre} ha derrotado a todos los monstruos y ha conquistado la mazmorra!")


    def enfrentar_enemigo(self,enemigo):
          while self.heroe.esta_vivo() and enemigo.esta_vivo():
                print("¿Qué deseas hacer?")
                print("1.Atacar")
                print("2.Defenderse")
                print("3.Curarse")
                try:
                    accion = int(input("Introduce el número de tu elección"))
                except ValueError:
                    print("Por favor, introduce un número válido")
                    continue
                if accion == 1:
                    self.heroe.atacar(enemigo)
                elif accion == 2:
                    self.heroe.defenderse()
                elif accion == 3:
                    self.heroe.curarse()
                else:
                    print("Opción no válida.")
                    continue

                if enemigo.esta_vivo():
                    enemigo.atacar(self.heroe)

                if self.heroe.usando_defensa:
                    self.heroe.reset_defensa()

    def buscar_tesoro(self):
        print("    Buscando tesoro...    ")
        self.tesoro.encontrar_tesoro(self.heroe)
        print(f"Estado del Héroe Ataque: {self.heroe.ataque} | Defensa: {self.heroe.defensa} | Salud: {self.heroe.salud}")