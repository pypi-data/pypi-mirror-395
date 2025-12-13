import re
from PyDNI.generator import Generator
from PyDNI import (
    verificar_dni,
    verificar_cif,
    verificar_nie,
    verificar_nif
)

gen = Generator()

# DNI
def test_generar_dni_formato():
    dni = gen.generar_dni()
    assert re.match(r"^\d{8}[A-Z]$", dni)


def test_generar_dni_valido():
    dni = gen.generar_dni()
    assert verificar_dni(dni)

# NIE
def test_generar_nie_formato():
    nie = gen.generar_nie()
    assert re.match(r"^[XYZ]\d{7}[A-Z]$", nie)


def test_generar_nie_valido():
    nie = gen.generar_nie()
    assert verificar_nie(nie)

# CIF
def test_generar_cif_formato():
    cif = gen.generar_cif()
    assert re.match(r"^[ABCDEFGHJKLMNPQRSUVW]\d{7}[A-Z0-9]$", cif)


def test_generar_cif_valido():
    cif = gen.generar_cif()
    assert verificar_cif(cif)

# Varios
def test_generar_varios_dni_sin_repetidos():
    docs = gen.generar_varios(100, "DNI")
    assert len(docs) == len(set(docs))  # Sin repetidos
    assert all(verificar_dni(d) for d in docs)


def test_generar_varios_nie_sin_repetidos():
    docs = gen.generar_varios(50, "NIE")
    assert len(docs) == len(set(docs))
    assert all(verificar_nie(d) for d in docs)


def test_generar_varios_cif_sin_repetidos():
    docs = gen.generar_varios(50, "CIF")
    assert len(docs) == len(set(docs))
    assert all(verificar_cif(d) for d in docs)


def test_generar_varios_auto_varios_tipos():
    docs = gen.generar_varios(100, "AUTO")
    assert len(docs) == len(set(docs))

    # Verifica que al menos hay 2 tipos diferentes
    tipos_detectados = {
        "DNI" if re.match(r"^\d{8}[A-Z]$", d) else
        "NIE" if re.match(r"^[XYZ]\d{7}[A-Z]$", d) else
        "CIF"
        for d in docs
    }
    assert len(tipos_detectados) >= 2
