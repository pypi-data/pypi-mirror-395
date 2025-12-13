from PyDNI.generator import Generator
from PyDNI import (
    verificar_dni,
    verificar_nie,
    verificar_cif,
)

gen = Generator()

def test_generar_persona_estructura():
    persona = gen.generar_persona()
    assert "nombre" in persona
    assert "sexo" in persona
    assert "tipo_documento" in persona
    assert "documento" in persona

def test_generar_persona_nombre_valido():
    persona = gen.generar_persona()
    partes = persona["nombre"].split()

    ap1 = partes[-2]
    ap2 = partes[-1]
    nombre = " ".join(partes[:-2])

    # El primer token del nombre indica el género base
    primer_nombre = nombre.split()[0]

    assert primer_nombre in Generator.NOMBRES_MASCULINOS + Generator.NOMBRES_FEMENINOS
    assert ap1 in Generator.APELLIDOS
    assert ap2 in Generator.APELLIDOS

def test_generar_persona_documento_valido():
    persona = gen.generar_persona()
    tipo = persona["tipo_documento"]
    doc = persona["documento"]

    if tipo == "DNI":
        assert verificar_dni(doc)
    elif tipo == "NIE":
        assert verificar_nie(doc)
    elif tipo == "CIF":
        assert verificar_cif(doc)
    else:
        assert False, f"Tipo de documento inesperado: {tipo}"

def test_generar_persona_masculina():
    persona = gen.generar_persona(sexo="masculino")
    nombre = persona["nombre"].split()[0]

    assert nombre in Generator.NOMBRES_MASCULINOS
    assert persona["sexo"] == "masculino"

def test_generar_persona_femenina():
    persona = gen.generar_persona(sexo="femenino")
    nombre = persona["nombre"].split()[0]

    assert nombre in Generator.NOMBRES_FEMENINOS
    assert persona["sexo"] == "femenino"

def test_generar_persona_con_dni():
    persona = gen.generar_persona(tipo_doc="DNI")
    assert persona["tipo_documento"] == "DNI"
    assert verificar_dni(persona["documento"])

def test_generar_persona_con_nie():
    persona = gen.generar_persona(tipo_doc="NIE")
    assert persona["tipo_documento"] == "NIE"
    assert verificar_nie(persona["documento"])

def test_generar_persona_con_cif():
    persona = gen.generar_persona(tipo_doc="CIF")
    assert persona["tipo_documento"] == "CIF"
    assert verificar_cif(persona["documento"])

def test_generar_persona_sexo_aleatorio():
    sexos = {gen.generar_persona(sexo="aleatorio")["sexo"] for _ in range(20)}
    assert sexos.issubset({"masculino", "femenino"})
    assert len(sexos) >= 1  # debería haber al menos 1 sexo generado

def test_generar_persona_tipo_aleatorio():
    tipos = {gen.generar_persona(tipo_doc="aleatorio")["tipo_documento"] for _ in range(30)}
    assert tipos.issubset({"DNI", "NIE", "CIF"})
    assert len(tipos) >= 1

def test_generar_persona_sexo_invalido():
    try:
        gen.generar_persona(sexo="robot")
        assert False, "Debe lanzar ValueError"
    except ValueError:
        assert True

def test_generar_persona_tipo_documento_invalido():
    try:
        gen.generar_persona(tipo_doc="PASAPORTE")
        assert False, "Debe lanzar ValueError"
    except ValueError:
        assert True
