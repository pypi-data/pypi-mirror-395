# nie.py

def verificar_nie(nie: str) -> bool:
    """
    Verifica si un NIE es válido.
    Formato: Letra inicial (X/Y/Z) + 7 dígitos + letra de control.
    """
    if not isinstance(nie, str):
        return False
    nie = nie.upper().strip()
    if len(nie) != 9:
        return False
    if nie[0] not in "XYZ":
        return False
    if not nie[1:-1].isdigit():
        return False

    # Convertir la letra inicial en número
    prefijos = {"X": "0", "Y": "1", "Z": "2"}
    numero = int(prefijos[nie[0]] + nie[1:-1])

    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    letra_correcta = letras[numero % 23]
    return nie[-1] == letra_correcta
