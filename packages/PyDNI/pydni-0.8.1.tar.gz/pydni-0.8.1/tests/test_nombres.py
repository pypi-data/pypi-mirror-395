from PyDNI.generator import Generator

gen = Generator()

def _extraer_nombre_apellidos(nombre_completo: str):
    """
    Devuelve:
      - nombre (puede tener 1 o varias palabras)
      - apellido1
      - apellido2
    """
    partes = nombre_completo.split()
    ap1 = partes[-2]
    ap2 = partes[-1]
    nombre = " ".join(partes[:-2])
    return nombre, ap1, ap2

def test_generar_nombre_masculino():
    nombre_completo = gen.generar_nombre("masculino")
    nombre, ap1, ap2 = _extraer_nombre_apellidos(nombre_completo)

    primer_nombre = nombre.split()[0]

    assert primer_nombre in Generator.NOMBRES_MASCULINOS
    assert ap1 in Generator.APELLIDOS
    assert ap2 in Generator.APELLIDOS

def test_generar_nombre_femenino():
    nombre_completo = gen.generar_nombre("femenino")
    nombre, ap1, ap2 = _extraer_nombre_apellidos(nombre_completo)

    primer_nombre = nombre.split()[0]

    assert primer_nombre in Generator.NOMBRES_FEMENINOS
    assert ap1 in Generator.APELLIDOS
    assert ap2 in Generator.APELLIDOS

def test_generar_nombre_aleatorio():
    nombre_completo = gen.generar_nombre("aleatorio")
    nombre, ap1, ap2 = _extraer_nombre_apellidos(nombre_completo)

    primer_nombre = nombre.split()[0]

    assert primer_nombre in Generator.NOMBRES_MASCULINOS + Generator.NOMBRES_FEMENINOS
    assert ap1 in Generator.APELLIDOS
    assert ap2 in Generator.APELLIDOS

def test_generar_nombre_sin_parametro_es_aleatorio():
    nombre_completo = gen.generar_nombre()
    nombre, ap1, ap2 = _extraer_nombre_apellidos(nombre_completo)

    primer_nombre = nombre.split()[0]

    assert primer_nombre in Generator.NOMBRES_MASCULINOS + Generator.NOMBRES_FEMENINOS
    assert ap1 in Generator.APELLIDOS
    assert ap2 in Generator.APELLIDOS

def test_generar_nombre_formato_correcto():
    nombre_completo = gen.generar_nombre("masculino")
    # Debe tener mínimo 3 palabras: nombre + 2 apellidos
    assert len(nombre_completo.split()) >= 3

def test_generar_nombre_apellidos_distintos():
    for _ in range(50):
        nombre_completo = gen.generar_nombre("aleatorio")
        _, ap1, ap2 = _extraer_nombre_apellidos(nombre_completo)
        assert ap1 != ap2

def test_generar_nombre_sexo_invalido():
    try:
        gen.generar_nombre("otro")
        assert False, "Debe lanzar ValueError"
    except ValueError:
        assert True