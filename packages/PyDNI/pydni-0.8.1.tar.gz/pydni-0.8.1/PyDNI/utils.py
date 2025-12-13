# utils.py

from .dni import verificar_dni
from .cif import verificar_cif
from .nie import verificar_nie

def verificar_identificador(valor: str) -> str:
    valor = valor.strip().upper()
    if len(valor) == 9:
        if valor[0] in "XYZ":
            return "NIE válido" if verificar_nie(valor) else "NIE no válido"
        elif valor[0].isalpha():
            return "CIF válido" if verificar_cif(valor) else "CIF no válido"
        elif valor[-1].isalpha():
            return "DNI válido" if verificar_dni(valor) else "DNI no válido"
    return "Formato no reconocido"

