# nif.py

from .dni import verificar_dni
from .nie import verificar_nie
from .cif import verificar_cif

def verificar_nif(nif: str) -> str:
    """
    Verifica un NIF genérico (DNI, NIE, CIF).
    Devuelve el tipo y si es válido.
    """
    nif = nif.strip().upper()
    if len(nif) != 9:
        return "Formato no reconocido"

    if nif[0].isdigit() and nif[-1].isalpha():
        return "DNI válido" if verificar_dni(nif) else "DNI no válido"
    elif nif[0] in "XYZ":
        return "NIE válido" if verificar_nie(nif) else "NIE no válido"
    elif nif[0].isalpha():
        return "CIF válido" if verificar_cif(nif) else "CIF no válido"
    else:
        return "Formato no reconocido"
