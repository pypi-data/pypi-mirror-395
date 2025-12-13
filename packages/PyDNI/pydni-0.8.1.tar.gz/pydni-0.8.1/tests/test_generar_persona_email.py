from PyDNI.generator import Generator
from PyDNI.emails import EmailGenerator


def test_persona_incluye_email():
    gen = Generator()
    persona = gen.generar_persona()

    assert "email" in persona
    assert "@" in persona["email"]


def test_email_persona_formato_correcto():
    gen = Generator()
    persona = gen.generar_persona()

    usuario, dominio = persona["email"].split("@")

    assert len(usuario) >= 2  # mínimo: inicial + apellido
    assert len(dominio) >= 3  # dominio razonable


def test_email_persona_coincide_con_nombre():
    gen = Generator()
    persona = gen.generar_persona()

    nombre = persona["nombre"]
    email = persona["email"]

    partes = nombre.split()
    inicial = partes[0][0].lower()

    eg = EmailGenerator()
    apellido = eg._limpiar(partes[-2])  # ← limpieza necesaria

    assert email.startswith(inicial + apellido)


def test_email_persona_con_nombres_compuestos():
    gen = Generator()
    eg = EmailGenerator()

    compuesto = False

    for _ in range(50):
        persona = gen.generar_persona()
        nombre = persona["nombre"]

        partes = nombre.split()
        if len(partes) > 3:  # nombre compuesto
            compuesto = True

            inicial = partes[0][0].lower()
            apellido = eg._limpiar(partes[-2])  # limpieza igual que el generador

            assert persona["email"].startswith(inicial + apellido)

    assert compuesto, "No se generó ningún nombre compuesto en 50 intentos"
