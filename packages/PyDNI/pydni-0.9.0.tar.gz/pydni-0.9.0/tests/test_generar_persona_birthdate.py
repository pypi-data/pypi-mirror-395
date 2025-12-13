from datetime import date
from PyDNI.generator import Generator


def calcular_edad(nacimiento: date) -> int:
    hoy = date.today()
    edad = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return edad

def test_generar_persona_incluye_fecha_nacimiento():
    gen = Generator()
    persona = gen.generar_persona()

    assert "fecha_nacimiento" in persona

    fecha = date.fromisoformat(persona["fecha_nacimiento"])
    assert isinstance(fecha, date)

def test_generar_persona_menor_de_edad():
    gen = Generator()
    persona = gen.generar_persona(edad="menor")

    fecha = date.fromisoformat(persona["fecha_nacimiento"])
    edad = calcular_edad(fecha)

    assert edad < 18

def test_generar_persona_mayor_de_edad():
    gen = Generator()
    persona = gen.generar_persona(edad="mayor")

    fecha = date.fromisoformat(persona["fecha_nacimiento"])
    edad = calcular_edad(fecha)

    assert edad >= 18

def test_generar_persona_edad_aleatoria():
    gen = Generator()
    persona = gen.generar_persona(edad="aleatorio")

    fecha = date.fromisoformat(persona["fecha_nacimiento"])
    assert isinstance(fecha, date)

def test_generar_persona_edad_random_alias():
    gen = Generator()
    persona = gen.generar_persona(edad="random")

    fecha = date.fromisoformat(persona["fecha_nacimiento"])
    assert isinstance(fecha, date)

def test_generar_persona_con_todos_parametros():
    gen = Generator()
    persona = gen.generar_persona(sexo="masculino", tipo_doc="DNI", edad="mayor")

    assert isinstance(persona["nombre"], str)
    assert persona["sexo"] == "masculino"
    assert persona["tipo_documento"] == "DNI"
    assert isinstance(persona["documento"], str)
    assert "@" in persona["email"]

    fecha = date.fromisoformat(persona["fecha_nacimiento"])
    assert calcular_edad(fecha) >= 18

def test_generar_persona_sin_parametros():
    gen = Generator()
    persona = gen.generar_persona()

    assert isinstance(persona["nombre"], str)
    assert persona["sexo"] in ("masculino", "femenino")
    assert persona["tipo_documento"] in ("DNI", "NIE", "CIF")

    fecha = date.fromisoformat(persona["fecha_nacimiento"])
    assert isinstance(fecha, date)

def test_generar_persona_con_edad_invalida():
    gen = Generator()

    try:
        gen.generar_persona(edad="anciano")
        assert False, "Debe lanzar ValueError para edad desconocida"
    except ValueError:
        assert True

def test_generar_persona_sin_fecha_nula():
    gen = Generator()
    persona = gen.generar_persona()

    assert persona["fecha_nacimiento"] is not None
