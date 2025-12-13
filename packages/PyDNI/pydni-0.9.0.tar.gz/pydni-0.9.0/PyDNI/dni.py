# dni.py

def verificar_dni(dni: str) -> bool:
    dni = dni.upper().strip()
    if len(dni) != 9 or not dni[:-1].isdigit():
        return False
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    numero = int(dni[:-1])
    letra_correcta = letras[numero % 23]
    return dni[-1] == letra_correcta
