from PyDNI.phone import PhoneGenerator

def test_generar_movil():
    gen = PhoneGenerator()
    tel = gen.generar_movil()
    assert tel[0] in "67"
    assert len(tel) == 9
    assert tel.isdigit()

def test_generar_fijo():
    gen = PhoneGenerator()
    tel = gen.generar_fijo()
    assert tel[0] in "89"
    assert len(tel) == 9
    assert tel.isdigit()

def test_generar_telefono_auto():
    gen = PhoneGenerator()
    tel = gen.generar_telefono()
    assert len(tel) == 9
