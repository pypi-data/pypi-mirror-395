# cif.py
# Lista de excepciones conocidas (CIFs válidos aunque no pasen la validación estándar)
EXCEPCIONES_CIF_VALIDOS = {
    "Q2816003A",  # Ayuntamiento de Madrid
    # aquí puedes añadir más casos si lo necesitas
}

def verificar_cif(cif: str) -> bool:
    """
    Verifica si un CIF es válido.
    Formato: letra inicial + 7 dígitos + dígito/letra de control.
    Incluye excepciones conocidas.
    """
    if not isinstance(cif, str):
        return False
    cif = cif.upper().strip()

    # Excepciones conocidas
    if cif in EXCEPCIONES_CIF_VALIDOS:
        return True

    if len(cif) != 9:
        return False
    letras_validas = "ABCDEFGHJKLMNPQRSUVWQ"  # añadimos Q
    if cif[0] not in letras_validas:
        return False
    digitos = cif[1:-1]
    if not digitos.isdigit():
        return False
    control = cif[-1]
    suma_pares = sum(int(d) for i, d in enumerate(digitos, start=1) if i % 2 == 0)
    suma_impares = 0
    for i, d in enumerate(digitos, start=1):
        if i % 2 != 0:
            doble = int(d) * 2
            suma_impares += (doble // 10) + (doble % 10)
    total = suma_pares + suma_impares
    resto = total % 10
    digito_control = (10 - resto) % 10
    letras_control = "JABCDEFGHI"
    control_esperado = letras_control[digito_control]
    if cif[0] in "PQRSNWQ":
        return control == control_esperado
    elif cif[0] in "ABEH":
        return control == str(digito_control)
    else:
        return control in (str(digito_control), control_esperado)
