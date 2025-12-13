from faker import Faker
from PyDNI import PyDNIFakerProvider

def test_faker_dni():
    fake = Faker("es_ES")
    fake.add_provider(PyDNIFakerProvider)

    dni = fake.dni()
    assert isinstance(dni, str)
    assert len(dni) == 9

def test_faker_nie():
    fake = Faker("es_ES")
    fake.add_provider(PyDNIFakerProvider)

    nie = fake.nie()
    assert isinstance(nie, str)

def test_faker_persona():
    fake = Faker("es_ES")
    fake.add_provider(PyDNIFakerProvider)

    persona = fake.persona()

    assert "nombre" in persona
    assert "documento" in persona
    assert "email" in persona
    assert "telefono" in persona
    assert "fecha_nacimiento" in persona

def test_faker_email_persona():
    fake = Faker("es_ES")
    fake.add_provider(PyDNIFakerProvider)

    email = fake.email_persona("empresa.com")
    assert email.endswith("@empresa.com")

def test_faker_telefono():
    fake = Faker("es_ES")
    fake.add_provider(PyDNIFakerProvider)

    tel = fake.telefono()
    assert tel.isdigit()
