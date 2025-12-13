from PyDNI.birthdates import BirthDateGenerator
from datetime import date


def calcular_edad(nacimiento: date) -> int:
    hoy = date.today()
    edad = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return edad


def test_menor_de_edad():
    gen = BirthDateGenerator()
    fecha = gen.menor_de_edad()
    assert calcular_edad(fecha) < 18


def test_mayor_de_edad():
    gen = BirthDateGenerator()
    fecha = gen.mayor_de_edad()
    assert calcular_edad(fecha) >= 18


def test_generar_menor():
    gen = BirthDateGenerator()
    fecha = gen.generar("menor")
    assert calcular_edad(fecha) < 18


def test_generar_mayor():
    gen = BirthDateGenerator()
    fecha = gen.generar("mayor")
    assert calcular_edad(fecha) >= 18


def test_generar_aleatorio():
    gen = BirthDateGenerator()
    fecha = gen.generar("aleatorio")
    assert isinstance(fecha, date)


def test_rango_personalizado():
    gen = BirthDateGenerator()
    fecha = gen.rango(edad_min=20, edad_max=30)
    edad = calcular_edad(fecha)
    assert 20 <= edad <= 30


def test_tipo_invalido():
    gen = BirthDateGenerator()
    try:
        gen.generar("inexistente")
        assert False, "Debe lanzar ValueError"
    except ValueError:
        assert True