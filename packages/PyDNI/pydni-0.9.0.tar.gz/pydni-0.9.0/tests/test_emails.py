from PyDNI.emails import EmailGenerator
from PyDNI.generator import Generator


def test_email_aleatorio_basico():
    eg = EmailGenerator()
    email = eg.generar_email_aleatorio()

    assert "@" in email
    usuario, dominio = email.split("@")

    assert len(usuario) >= 8
    assert dominio in EmailGenerator.DOMINIOS_POR_DEFECTO


def test_email_aleatorio_con_dominio_personalizado():
    eg = EmailGenerator()
    email = eg.generar_email_aleatorio("midominio.com")

    assert email.endswith("@midominio.com")


def test_email_nombre_simple():
    eg = EmailGenerator()
    email = eg.generar_email_nombre("Carlos Ruiz Gómez", "empresa.com")

    assert email == "cruiz@empresa.com"


def test_email_nombre_con_acentos_y_mayusculas():
    eg = EmailGenerator()
    email = eg.generar_email_nombre("María López García", "test.com")

    # María → m ; López → lopez
    assert email == "mlopez@test.com"


def test_email_nombre_compuesto():
    eg = EmailGenerator()
    email = eg.generar_email_nombre("Ana María Pérez López", "test.com")

    assert email == "aperez@test.com"


def test_email_generico_con_nombre():
    eg = EmailGenerator()
    email = eg.generar_email("Luis García Fernández")

    usuario, dominio = email.split("@")
    assert usuario == "lgarcia"
    assert dominio in EmailGenerator.DOMINIOS_POR_DEFECTO


def test_email_generico_sin_nombre():
    eg = EmailGenerator()
    email = eg.generar_email()

    assert "@" in email
    assert len(email.split("@")[0]) >= 8


def test_error_nombre_incompleto():
    eg = EmailGenerator()
    try:
        eg.generar_email_nombre("Carlos Ruiz", "dom.com")
        assert False, "Debe lanzar ValueError por nombre incompleto"
    except ValueError:
        assert True
