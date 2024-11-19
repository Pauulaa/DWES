# Importar las funciones del archivo operaciones.py
from operaciones import suma, resta, multiplicacion, division

REPETIR = "S"
while REPETIR != "N":
    print("=============================")
    print("         Calculadora         ")
    print("=============================")
    print("     Teclea la opción(1-4)   ")
    print("-----------------------------")
    print("         1-Sumar             ")
    print("         2-Restar            ")
    print("         3-Multiplicar       ")
    print("         4-Dividir           ")
    print("=============================")
   
    # Solicitar la operación
    OPCION = int(input("Operacion ? (1-4): "))
   
    if OPCION not in range(1, 5):
        print("No está en el rango de opciones")
        break
   
    # Solicitar los números
    NUM1 = float(input("Introduce el primer número: "))
    NUM2 = float(input("Introduce el segundo número: "))
   
    # Ejecutar la operación correspondiente e imprimir el resultado
    if OPCION == 1:
        resultado = suma(NUM1, NUM2)
        print(f"Resultado: {resultado}")
    elif OPCION == 2:
        resultado = resta(NUM1, NUM2)
        print(f"Resultado: {resultado}")
    elif OPCION == 3:
        resultado = multiplicacion(NUM1, NUM2)
        print(f"Resultado: {resultado}")
    elif OPCION == 4:
        resultado = division(NUM1, NUM2)
        print(f"Resultado: {resultado}")
       
    # Preguntar si quiere realizar otra operación
    REPETIR = input("¿Quieres realizar otra operación? (S/N): ").upper()