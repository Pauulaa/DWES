# operaciones.py

def suma(a, b):
    """Realiza la suma de dos números"""
    return a + b

def resta(a, b):
    """Realiza la resta de dos números"""
    return a - b

def multiplicacion(a, b):
    """Realiza la multiplicación de dos números"""
    return a * b

def division(a, b):
    """Realiza la división de dos números, controlando división por 0"""
    if b == 0:
        return "Error: No se puede dividir por 0"
    else:
        return a / b

