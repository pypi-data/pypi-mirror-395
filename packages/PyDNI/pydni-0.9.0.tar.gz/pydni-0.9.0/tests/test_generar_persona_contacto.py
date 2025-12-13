from PyDNI import Generator

def test_persona_tiene_telefono_y_direccion():
    gen = Generator()
    persona = gen.generar_persona()

    assert "telefono" in persona
    assert len(persona["telefono"]) == 9

